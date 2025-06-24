"""
Image Pad For Outpaint Masked Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Expands image with padding and generates corresponding mask for outpainting.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import torch.nn.functional as F

MAX_RESOLUTION = 8192

class ImagePadForOutpaintMasked_UTK:
    CATEGORY = "UniversalToolkit/Image"

    @classmethod
    def INPUT_TYPES(cls):
        color_options = ["gray", "white", "black", "red", "green", "blue", "yellow", "cyan", "magenta"]
        return {
            "required": {
                "image": ("IMAGE",),
                "data_mode": (["pixel", "percent"], {"default": "pixel"}),
                "left": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
                "top": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
                "right": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
                "bottom": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
                "feathering": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                "background_color": (color_options, {"default": "gray"}),
            },
            "optional": {
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "expand_image"

    def expand_image(self, image, data_mode, left, top, right, bottom, feathering, background_color, mask=None):
        B, H, W, C = image.size()
        # 处理 pad 参数
        if data_mode == "percent":
            left = int(W * left / 100)
            right = int(W * right / 100)
            top = int(H * top / 100)
            bottom = int(H * bottom / 100)
        # 背景色映射
        color_map = {
            "gray": [0.5, 0.5, 0.5],
            "white": [1.0, 1.0, 1.0],
            "black": [0.0, 0.0, 0.0],
            "red": [1.0, 0.0, 0.0],
            "green": [0.0, 1.0, 0.0],
            "blue": [0.0, 0.0, 1.0],
            "yellow": [1.0, 1.0, 0.0],
            "cyan": [0.0, 1.0, 1.0],
            "magenta": [1.0, 0.0, 1.0],
        }
        bg_rgb = color_map.get(background_color, [0.5, 0.5, 0.5])
        # 新图像
        new_image = torch.ones((B, H + top + bottom, W + left + right, C), dtype=torch.float32) 
        for i in range(C):
            new_image[:, :, :, i] = bg_rgb[i]
        new_image[:, top:top + H, left:left + W, :] = image
        # 掩码逻辑与原实现一致
        if mask is not None:
            if torch.allclose(mask, torch.zeros_like(mask)):
                print("Warning: The incoming mask is fully black. Handling it as None.")
                mask = None
        if mask is None:
            new_mask = torch.ones((B, H + top + bottom, W + left + right), dtype=torch.float32)
            t = torch.zeros((B, H, W), dtype=torch.float32)
        else:
            mask = F.pad(mask, (left, right, top, bottom), mode='constant', value=0)
            mask = 1 - mask
            t = torch.zeros_like(mask)
        if feathering > 0 and feathering * 2 < H and feathering * 2 < W:
            for i in range(H):
                for j in range(W):
                    dt = i if top != 0 else H
                    db = H - i if bottom != 0 else H
                    dl = j if left != 0 else W
                    dr = W - j if right != 0 else W
                    d = min(dt, db, dl, dr)
                    if d >= feathering:
                        continue
                    v = (feathering - d) / feathering
                    if mask is None:
                        t[:, i, j] = v * v
                    else:
                        t[:, top + i, left + j] = v * v
        if mask is None:
            new_mask[:, top:top + H, left:left + W] = t
            return (new_image, new_mask,)
        else:
            return (new_image, mask,)

# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImagePadForOutpaintMasked_UTK": ImagePadForOutpaintMasked_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImagePadForOutpaintMasked_UTK": "Image Pad For Outpaint Masked (UTK)",
} 