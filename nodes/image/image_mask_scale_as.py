"""
Image Mask Scale As Node
~~~~~~~~~~~~~~~~~~~~~~~

Scales images and masks to match the dimensions of a reference image.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
from PIL import Image, ImageFilter

from ..image_utils import image2mask, pil2tensor, tensor2pil


def log(message, message_type="info"):
    """简单的日志函数"""
    if message_type == "error":
        print(f"❌ Error: {message}")
    elif message_type == "warning":
        print(f"⚠️ Warning: {message}")
    elif message_type == "finish":
        print(f"✅ {message}")
    else:
        print(f"ℹ️ {message}")


def fit_resize_image(
    image,
    target_width,
    target_height,
    fit_mode,
    resize_sampler,
    background_color="black",
    crop_position="center",
):
    """Resize image according to fit mode"""
    if fit_mode == "resize":
        # resize: 只等比缩放，不填充，直接返回缩放后的图像
        scale = min(target_width / image.width, target_height / image.height)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        return image.resize((new_width, new_height), resize_sampler)
    
    if fit_mode in ["letterbox", "pad", "pad_edge", "pad_edge_pixel", "pillarbox_blur"]:
        # Calculate scaling factor to fit within target dimensions
        scale = min(target_width / image.width, target_height / image.height)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)

        # Resize image
        resized = image.resize((new_width, new_height), resize_sampler)

        # Create background
        if fit_mode == "pillarbox_blur":
            # create scaled background then blur and dim
            scale_fill = max(target_width / max(1, image.width), target_height / max(1, image.height))
            bg_w = max(1, int(round(image.width * scale_fill)))
            bg_h = max(1, int(round(image.height * scale_fill)))
            bg = image.resize((bg_w, bg_h), Image.BILINEAR)
            # center crop to canvas
            x0 = max(0, (bg_w - target_width) // 2)
            y0 = max(0, (bg_h - target_height) // 2)
            bg = bg.crop((x0, y0, x0 + target_width, y0 + target_height))
            sigma = max(1.0, 0.006 * float(min(target_width, target_height)))
            bg = bg.filter(ImageFilter.GaussianBlur(radius=sigma))
            # desaturate slightly if RGB
            if bg.mode == "RGB":
                r, g, b = bg.split()
                # simple luminance
                l = r.point(lambda v: int(0.2126 * v))
                l = Image.merge("RGB", (l, l, l))
                def mix(a, b, t=0.2):
                    return Image.blend(a, b, t)
                bg = mix(bg, l)
            # dim
            bg = bg.point(lambda v: int(v * 0.35))
            result = bg
        elif fit_mode in ["pad_edge", "pad_edge_pixel"]:
            # start with empty canvas
            result = Image.new("RGB" if image.mode == "RGB" else "L", (target_width, target_height))
        else:
            if image.mode == "RGB":
                # preset color names
                preset_colors = {
                    "black": "#000000",
                    "white": "#FFFFFF",
                    "gray": "#808080",
                    "red": "#FF0000",
                    "green": "#00FF00",
                    "blue": "#0000FF",
                    "yellow": "#FFFF00",
                    "cyan": "#00FFFF",
                    "magenta": "#FF00FF",
                }
                fill_color = preset_colors.get(str(background_color).lower(), background_color)
                result = Image.new("RGB", (target_width, target_height), fill_color)
            else:
                result = Image.new("L", (target_width, target_height), 0)

        # paste location
        if crop_position == "center":
            paste_x = (target_width - new_width) // 2
            paste_y = (target_height - new_height) // 2
        elif crop_position == "top":
            paste_x = (target_width - new_width) // 2
            paste_y = 0
        elif crop_position == "bottom":
            paste_x = (target_width - new_width) // 2
            paste_y = target_height - new_height
        elif crop_position == "left":
            paste_x = 0
            paste_y = (target_height - new_height) // 2
        elif crop_position == "right":
            paste_x = target_width - new_width
            paste_y = (target_height - new_height) // 2
        else:
            paste_x = (target_width - new_width) // 2
            paste_y = (target_height - new_height) // 2
        # specialized edge padding behaviors
        if fit_mode == "pad_edge" or fit_mode == "pad_edge_pixel":
            left_pad = paste_x
            right_pad = target_width - (paste_x + new_width)
            top_pad = paste_y
            bottom_pad = target_height - (paste_y + new_height)

            # left/right stripes from image columns
            if left_pad > 0:
                col = resized.crop((0, 0, 1, new_height))
                if fit_mode == "pad_edge_pixel":
                    col = col.resize((left_pad, new_height), Image.NEAREST)
                    result.paste(col, (0, paste_y))
                else:
                    # mean color of left edge
                    if col.mode == "RGB":
                        pixels = list(col.getdata())
                        r = sum(p[0] for p in pixels) // len(pixels)
                        g = sum(p[1] for p in pixels) // len(pixels)
                        b = sum(p[2] for p in pixels) // len(pixels)
                        fill = (r, g, b)
                    else:
                        v = sum(col.getdata()) // len(col.getdata())
                        fill = v
                    Image.Image.paste(result, Image.new(result.mode, (left_pad, new_height), fill), (0, paste_y))

            if right_pad > 0:
                col = resized.crop((new_width - 1, 0, new_width, new_height))
                if fit_mode == "pad_edge_pixel":
                    col = col.resize((right_pad, new_height), Image.NEAREST)
                    result.paste(col, (paste_x + new_width, paste_y))
                else:
                    if col.mode == "RGB":
                        pixels = list(col.getdata())
                        r = sum(p[0] for p in pixels) // len(pixels)
                        g = sum(p[1] for p in pixels) // len(pixels)
                        b = sum(p[2] for p in pixels) // len(pixels)
                        fill = (r, g, b)
                    else:
                        v = sum(col.getdata()) // len(col.getdata())
                        fill = v
                    Image.Image.paste(result, Image.new(result.mode, (right_pad, new_height), fill), (paste_x + new_width, paste_y))

            # top/bottom stripes from image rows
            if top_pad > 0:
                row = resized.crop((0, 0, new_width, 1))
                if fit_mode == "pad_edge_pixel":
                    row = row.resize((new_width, top_pad), Image.NEAREST)
                    result.paste(row, (paste_x, 0))
                    # corners by corner pixels
                    if left_pad > 0:
                        c = resized.getpixel((0, 0))
                        Image.Image.paste(result, Image.new(result.mode, (left_pad, top_pad), c), (0, 0))
                    if right_pad > 0:
                        c = resized.getpixel((new_width - 1, 0))
                        Image.Image.paste(result, Image.new(result.mode, (right_pad, top_pad), c), (paste_x + new_width, 0))
                else:
                    if row.mode == "RGB":
                        pixels = list(row.getdata())
                        r = sum(p[0] for p in pixels) // len(pixels)
                        g = sum(p[1] for p in pixels) // len(pixels)
                        b = sum(p[2] for p in pixels) // len(pixels)
                        fill = (r, g, b)
                    else:
                        v = sum(row.getdata()) // len(row.getdata())
                        fill = v
                    Image.Image.paste(result, Image.new(result.mode, (target_width, top_pad), fill), (0, 0))

            if bottom_pad > 0:
                row = resized.crop((0, new_height - 1, new_width, new_height))
                if fit_mode == "pad_edge_pixel":
                    row = row.resize((new_width, bottom_pad), Image.NEAREST)
                    result.paste(row, (paste_x, paste_y + new_height))
                    if left_pad > 0:
                        c = resized.getpixel((0, new_height - 1))
                        Image.Image.paste(result, Image.new(result.mode, (left_pad, bottom_pad), c), (0, paste_y + new_height))
                    if right_pad > 0:
                        c = resized.getpixel((new_width - 1, new_height - 1))
                        Image.Image.paste(result, Image.new(result.mode, (right_pad, bottom_pad), c), (paste_x + new_width, paste_y + new_height))
                else:
                    if row.mode == "RGB":
                        pixels = list(row.getdata())
                        r = sum(p[0] for p in pixels) // len(pixels)
                        g = sum(p[1] for p in pixels) // len(pixels)
                        b = sum(p[2] for p in pixels) // len(pixels)
                        fill = (r, g, b)
                    else:
                        v = sum(row.getdata()) // len(row.getdata())
                        fill = v
                    Image.Image.paste(result, Image.new(result.mode, (target_width, bottom_pad), fill), (0, paste_y + new_height))

        # finally paste the resized content
        result.paste(resized, (paste_x, paste_y))
        return result

    elif fit_mode == "crop":
        # Calculate scaling factor to cover target dimensions
        scale = max(target_width / image.width, target_height / image.height)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)

        # Resize image
        resized = image.resize((new_width, new_height), resize_sampler)

        # Crop to target dimensions
        if crop_position == "center":
            crop_x = (new_width - target_width) // 2
            crop_y = (new_height - target_height) // 2
        elif crop_position == "top":
            crop_x = (new_width - target_width) // 2
            crop_y = 0
        elif crop_position == "bottom":
            crop_x = (new_width - target_width) // 2
            crop_y = new_height - target_height
        elif crop_position == "left":
            crop_x = 0
            crop_y = (new_height - target_height) // 2
        elif crop_position == "right":
            crop_x = new_width - target_width
            crop_y = (new_height - target_height) // 2
        else:
            crop_x = (new_width - target_width) // 2
            crop_y = (new_height - target_height) // 2
        return resized.crop(
            (crop_x, crop_y, crop_x + target_width, crop_y + target_height)
        )

    else:  # stretch/fill
        # Simple resize to target dimensions
        return image.resize((target_width, target_height), resize_sampler)


class ImageMaskScaleAs_UTK:
    CATEGORY = "UniversalToolkit/Image"

    @classmethod
    def INPUT_TYPES(cls):
        fit_mode = [
            "stretch",
            "resize",
            "pad",
            "pad_edge",
            "pad_edge_pixel",
            "crop",
            "pillarbox_blur",
        ]
        method_mode = ["lanczos", "bicubic", "hamming", "bilinear", "box", "nearest"]

        return {
            "required": {
                "scale_as": ("IMAGE",),
                "fit": (fit_mode,),
                "method": (method_mode,),
            },
            "optional": {
                "image": ("IMAGE",),  #
                "mask": ("MASK",),  #
                "pad_color": ([
                    "black",
                    "white",
                    "gray",
                    "red",
                    "green",
                    "blue",
                    "yellow",
                    "cyan",
                    "magenta",
                ], {"default": "black"}),
                "crop_position": (["center", "top", "bottom", "left", "right"], {"default": "center"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "BOX", "INT", "INT")
    RETURN_NAMES = (
        "image",
        "mask",
        "original_size",
        "width",
        "height",
    )
    FUNCTION = "image_mask_scale_as"

    def image_mask_scale_as(
        self,
        scale_as,
        fit,
        method,
        image=None,
        mask=None,
        pad_color="black",
        crop_position="center",
    ):
        if scale_as.shape[0] > 0:
            _asimage = tensor2pil(scale_as[0])
        else:
            _asimage = tensor2pil(scale_as)
        target_width, target_height = _asimage.size
        _mask = Image.new("L", size=_asimage.size, color="black")
        _image = Image.new("RGB", size=_asimage.size, color="black")
        orig_width = 4
        orig_height = 4
        resize_sampler = Image.LANCZOS
        if method == "bicubic":
            resize_sampler = Image.BICUBIC
        elif method == "hamming":
            resize_sampler = Image.HAMMING
        elif method == "bilinear":
            resize_sampler = Image.BILINEAR
        elif method == "box":
            resize_sampler = Image.BOX
        elif method == "nearest":
            resize_sampler = Image.NEAREST

        ret_images = []
        ret_masks = []

        output_width = target_width
        output_height = target_height
        
        if image is not None:
            for i in image:
                i = torch.unsqueeze(i, 0)
                _image = tensor2pil(i).convert("RGB")
                orig_width, orig_height = _image.size
                _image = fit_resize_image(
                    _image, target_width, target_height, fit, resize_sampler, pad_color, crop_position
                )
                # For resize mode, use actual image size instead of target size
                if fit == "resize":
                    output_width, output_height = _image.size
                ret_images.append(pil2tensor(_image))
        if mask is not None:
            if mask.dim() == 2:
                mask = torch.unsqueeze(mask, 0)
            for m in mask:
                m = torch.unsqueeze(m, 0)
                _mask = tensor2pil(m).convert("L")
                orig_width, orig_height = _mask.size
                # Mask padding背景始终为黑
                _mask = fit_resize_image(
                    _mask, target_width, target_height, fit, resize_sampler, "#000000", crop_position
                ).convert("L")
                # For resize mode, use actual mask size instead of target size
                if fit == "resize":
                    output_width, output_height = _mask.size
                ret_masks.append(image2mask(_mask))
        if len(ret_images) > 0 and len(ret_masks) > 0:
            log(
                f"ImageMaskScaleAs_UTK Processed {len(ret_images)} image(s).",
                message_type="finish",
            )
            return (
                torch.cat(ret_images, dim=0),
                torch.cat(ret_masks, dim=0),
                [orig_width, orig_height],
                output_width,
                output_height,
            )
        elif len(ret_images) > 0 and len(ret_masks) == 0:
            log(
                f"ImageMaskScaleAs_UTK Processed {len(ret_images)} image(s).",
                message_type="finish",
            )
            return (
                torch.cat(ret_images, dim=0),
                None,
                [orig_width, orig_height],
                output_width,
                output_height,
            )
        elif len(ret_images) == 0 and len(ret_masks) > 0:
            log(
                f"ImageMaskScaleAs_UTK Processed {len(ret_masks)} image(s).",
                message_type="finish",
            )
            return (
                None,
                torch.cat(ret_masks, dim=0),
                [orig_width, orig_height],
                output_width,
                output_height,
            )
        else:
            log(
                f"Error: ImageMaskScaleAs_UTK skipped, because the available image or mask is not found.",
                message_type="error",
            )
            return (
                None,
                None,
                [orig_width, orig_height],
                0,
                0,
            )


# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImageMaskScaleAs_UTK": ImageMaskScaleAs_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageMaskScaleAs_UTK": "Image Mask Scale As (UTK)",
}
