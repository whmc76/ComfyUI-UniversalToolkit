import math
import torch
import torch.nn.functional as F

from comfy import model_management
from comfy.utils import common_upscale


class ResizeImageVerKJ_UTK:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 512, "min": 0, "max": 16384, "step": 1}),
                "height": ("INT", {"default": 512, "min": 0, "max": 16384, "step": 1}),
                "upscale_method": (cls.upscale_methods,),
                "keep_proportion": (
                    [
                        "stretch",
                        "resize",
                        "pad",
                        "pad_edge",
                        "pad_edge_pixel",
                        "crop",
                        "pillarbox_blur",
                        "total_pixels",
                    ],
                    {"default": "resize"},
                ),
                "pad_color": ("STRING", {"default": "0, 0, 0"}),
                "crop_position": ("STRING", {"default": "center"}),
                "divisible_by": ("INT", {"default": 2, "min": 0, "max": 512, "step": 1}),
            },
            "optional": {
                "mask": ("MASK",),
                "device": (["cpu", "gpu"], {"default": "cpu"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "MASK")
    RETURN_NAMES = ("IMAGE", "width", "height", "mask")
    FUNCTION = "resize"
    CATEGORY = "UniversalToolkit/Image"

    def _parse_color(self, s: str, dtype, device):
        try:
            vals = [int(x.strip()) for x in s.split(",")]
        except Exception:
            vals = [0, 0, 0]
        if len(vals) == 1:
            vals = vals * 3
        vals = [max(0, min(255, v)) / 255.0 for v in vals[:3]]
        return torch.tensor(vals, dtype=dtype, device=device)

    def _compute_crop_rect(self, old_w, old_h, target_w, target_h, position: str):
        old_aspect = old_w / old_h
        new_aspect = target_w / target_h
        if old_aspect > new_aspect:
            crop_w = round(old_h * new_aspect)
            crop_h = old_h
        else:
            crop_w = old_w
            crop_h = round(old_w / new_aspect)
        if position == "center":
            x = (old_w - crop_w) // 2
            y = (old_h - crop_h) // 2
        elif position == "top":
            x, y = (old_w - crop_w) // 2, 0
        elif position == "bottom":
            x, y = (old_w - crop_w) // 2, old_h - crop_h
        elif position == "left":
            x, y = 0, (old_h - crop_h) // 2
        elif position == "right":
            x, y = old_w - crop_w, (old_h - crop_h) // 2
        else:
            x, y = (old_w - crop_w) // 2, (old_h - crop_h) // 2
        return x, y, crop_w, crop_h

    def resize(self, image: torch.Tensor, width: int, height: int, keep_proportion: str, upscale_method: str,
               divisible_by: int, pad_color: str, crop_position: str, device: str = "cpu", mask: torch.Tensor = None):
        B, H, W, C = image.shape

        if device == "gpu":
            if upscale_method == "lanczos":
                raise Exception("Lanczos is not supported on the GPU")
            torch_device = model_management.get_torch_device()
        else:
            torch_device = torch.device("cpu")

        pillarbox_blur = keep_proportion == "pillarbox_blur"

        pad_left = pad_right = pad_top = pad_bottom = 0

        if keep_proportion in ["resize", "total_pixels", "pad", "pad_edge", "pad_edge_pixel", "pillarbox_blur"]:
            if keep_proportion == "total_pixels":
                total_pixels = max(1, width * height)
                aspect_ratio = W / H if H != 0 else 1.0
                new_h = int(math.sqrt(total_pixels / aspect_ratio))
                new_w = int(math.sqrt(total_pixels * aspect_ratio))
            elif width == 0 and height == 0:
                new_w, new_h = W, H
            elif width == 0 and height != 0:
                ratio = height / H if H != 0 else 1.0
                new_w, new_h = round(W * ratio), height
            elif height == 0 and width != 0:
                ratio = width / W if W != 0 else 1.0
                new_w, new_h = width, round(H * ratio)
            else:
                ratio = min(width / W if W != 0 else 1.0, height / H if H != 0 else 1.0)
                new_w, new_h = max(1, round(W * ratio)), max(1, round(H * ratio))

            if keep_proportion in ["pad", "pad_edge", "pad_edge_pixel", "pillarbox_blur"]:
                if crop_position == "center":
                    pad_left = (width - new_w) // 2
                    pad_right = width - new_w - pad_left
                    pad_top = (height - new_h) // 2
                    pad_bottom = height - new_h - pad_top
                elif crop_position == "top":
                    pad_left = (width - new_w) // 2
                    pad_right = width - new_w - pad_left
                    pad_top = 0
                    pad_bottom = height - new_h
                elif crop_position == "bottom":
                    pad_left = (width - new_w) // 2
                    pad_right = width - new_w - pad_left
                    pad_top = height - new_h
                    pad_bottom = 0
                elif crop_position == "left":
                    pad_left = 0
                    pad_right = width - new_w
                    pad_top = (height - new_h) // 2
                    pad_bottom = height - new_h - pad_top
                elif crop_position == "right":
                    pad_left = width - new_w
                    pad_right = 0
                    pad_top = (height - new_h) // 2
                    pad_bottom = height - new_h - pad_top

            width, height = new_w, new_h
        else:
            # stretch or crop path keeps requested width/height directly
            if width == 0:
                width = W
            if height == 0:
                height = H

        if divisible_by > 1:
            width = width - (width % divisible_by)
            height = height - (height % divisible_by)

        # Crop prior to resizing
        x_in = image if image.device == torch_device else image.to(torch_device)
        m_in = None if mask is None else (mask if mask.device == torch_device else mask.to(torch_device))

        if keep_proportion == "crop":
            x, y, cw, ch = self._compute_crop_rect(W, H, width, height, crop_position)
            x_in = x_in.narrow(-2, x, cw).narrow(-3, y, ch)
            if m_in is not None:
                m_in = m_in.narrow(-1, x, cw).narrow(-2, y, ch)

        # Resize image and optional mask
        out_img = common_upscale(x_in.movedim(-1, 1), width, height, upscale_method, crop="disabled").movedim(1, -1)
        out_m = None
        if m_in is not None:
            if upscale_method == "lanczos":
                out_m = common_upscale(m_in.unsqueeze(1).repeat(1, 3, 1, 1), width, height, upscale_method, crop="disabled").movedim(1, -1)[:, :, :, 0]
            else:
                out_m = common_upscale(m_in.unsqueeze(1), width, height, upscale_method, crop="disabled").squeeze(1)

        # resize mode: just return the resized image, no padding
        if keep_proportion == "resize":
            return (out_img.cpu(), out_img.shape[2], out_img.shape[1], out_m.cpu() if out_m is not None else torch.zeros(64, 64))
        
        # Padding if requested
        if (keep_proportion in ["pad", "pad_edge", "pad_edge_pixel", "pillarbox_blur"]) and (pad_left > 0 or pad_right > 0 or pad_top > 0 or pad_bottom > 0):
            padded_w = width + pad_left + pad_right
            padded_h = height + pad_top + pad_bottom
            if divisible_by > 1:
                w_rem = padded_w % divisible_by
                h_rem = padded_h % divisible_by
                if w_rem > 0:
                    pad_right += divisible_by - w_rem
                if h_rem > 0:
                    pad_bottom += divisible_by - h_rem
                padded_w = width + pad_left + pad_right
                padded_h = height + pad_top + pad_bottom

            if keep_proportion == "pad_edge" or keep_proportion == "pad_edge_pixel":
                # Build canvas and apply edge/edge_pixel logic similar to KJ implementation
                canvas = torch.zeros((B, padded_h, padded_w, C), dtype=out_img.dtype, device=out_img.device)
                for b in range(B):
                    # content
                    canvas[b, pad_top:pad_top+height, pad_left:pad_left+width, :] = out_img[b]
                    if keep_proportion == "pad_edge":
                        # mean color along edges
                        top_edge = out_img[b, 0, :, :]
                        bottom_edge = out_img[b, height-1, :, :]
                        left_edge = out_img[b, :, 0, :]
                        right_edge = out_img[b, :, width-1, :]
                        if pad_top > 0:
                            canvas[b, :pad_top, :, :] = top_edge.mean(dim=0)
                        if pad_bottom > 0:
                            canvas[b, pad_top+height:, :, :] = bottom_edge.mean(dim=0)
                        if pad_left > 0:
                            canvas[b, :, :pad_left, :] = left_edge.mean(dim=0)
                        if pad_right > 0:
                            canvas[b, :, pad_left+width:, :] = right_edge.mean(dim=0)
                    else:
                        # edge_pixel: extend exact edge rows/columns
                        if pad_top > 0:
                            row = out_img[b, 0:1, :, :].expand(pad_top, width, C)
                            canvas[b, :pad_top, pad_left:pad_left+width, :] = row
                            # corners
                            if pad_left > 0:
                                tl = out_img[b, 0, 0, :]
                                canvas[b, :pad_top, :pad_left, :] = tl
                            if pad_right > 0:
                                tr = out_img[b, 0, width-1, :]
                                canvas[b, :pad_top, pad_left+width:, :] = tr
                        if pad_bottom > 0:
                            row = out_img[b, height-1:height, :, :].expand(pad_bottom, width, C)
                            canvas[b, pad_top+height:, pad_left:pad_left+width, :] = row
                            if pad_left > 0:
                                bl = out_img[b, height-1, 0, :]
                                canvas[b, pad_top+height:, :pad_left, :] = bl
                            if pad_right > 0:
                                br = out_img[b, height-1, width-1, :]
                                canvas[b, pad_top+height:, pad_left+width:, :] = br
                        if pad_left > 0:
                            col = out_img[b, :, 0:1, :].expand(height, pad_left, C)
                            canvas[b, pad_top:pad_top+height, :pad_left, :] = col
                        if pad_right > 0:
                            col = out_img[b, :, width-1:width, :].expand(height, pad_right, C)
                            canvas[b, pad_top:pad_top+height, pad_left+width:, :] = col
                out_img = canvas
                if out_m is not None:
                    # replicate for mask to keep crisp edges
                    out_m = F.pad(out_m.unsqueeze(1), (pad_left, pad_right, pad_top, pad_bottom), mode="replicate").squeeze(1)
            else:
                # color padding
                bg = self._parse_color(pad_color, out_img.dtype, out_img.device)
                canvas = torch.zeros((B, padded_h, padded_w, C), dtype=out_img.dtype, device=out_img.device)
                canvas[:, :, :, 0] = bg[0]
                if C > 1:
                    canvas[:, :, :, 1] = bg[1]
                if C > 2:
                    canvas[:, :, :, 2] = bg[2]
                canvas[:, pad_top:pad_top+height, pad_left:pad_left+width, :] = out_img
                out_img = canvas
                if out_m is not None:
                    mcanvas = torch.zeros((B, padded_h, padded_w), dtype=out_img.dtype, device=out_img.device)
                    mcanvas[:, pad_top:pad_top+height, pad_left:pad_left+width] = out_m
                    out_m = mcanvas

        return (out_img.cpu(), out_img.shape[2], out_img.shape[1], out_m.cpu() if out_m is not None else torch.zeros(64, 64))


NODE_CLASS_MAPPINGS = {"ResizeImageVerKJ_UTK": ResizeImageVerKJ_UTK}
NODE_DISPLAY_NAME_MAPPINGS = {"ResizeImageVerKJ_UTK": "Resize Image ver KJ (UTK)"}


