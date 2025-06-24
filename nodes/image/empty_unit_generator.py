"""
Empty Unit Generator Node
~~~~~~~~~~~~~~~~~~~~~~~~~

Generate empty units for testing and development.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import numpy as np
import re
from PIL import Image
import cv2

from ..tools.logging_utils import log

class EmptyUnitGenerator_UTK:
    CATEGORY = "UniversalToolkit/Image"
    
    @classmethod
    def INPUT_TYPES(cls):
        ratio_options = [
            "custom",
            "SD1.5 - 1:1 square 512x512",
            "SD1.5 - 2:3 portrait 512x768",
            "SD1.5 - 3:4 portrait 512x682",
            "SD1.5 - 3:2 landscape 768x512",
            "SD1.5 - 4:3 landscape 682x512",
            "SD1.5 - 16:9 cinema 910x512",
            "SD1.5 - 1.85:1 cinema 952x512",
            "SD1.5 - 2:1 cinema 1024x512",
            "SDXL - 1:1 square 1024x1024",
            "SDXL - 3:4 portrait 896x1152",
            "SDXL - 5:8 portrait 832x1216",
            "SDXL - 9:16 portrait 768x1344",
            "SDXL - 9:21 portrait 640x1536",
            "SDXL - 4:3 landscape 1152x896",
            "SDXL - 3:2 landscape 1216x832",
            "SDXL - 16:9 landscape 1344x768",
            "SDXL - 21:9 landscape 1536x640",
        ]
        latent_type_options = ["standard", "sd3", "hunyuan", "ltx"]
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 4096, "step": 8, "label": "Width (custom only)"}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 4096, "step": 8, "label": "Height (custom only)"}),
                "ratio": (ratio_options, {"default": ratio_options[9], "label": "Resolution/Ratio"}),
                "scale": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 8.0, "step": 0.1, "label": "Scale (放大倍数)"}),
                "divisor": ("INT", {"default": 8, "min": 1, "max": 512, "step": 1, "label": "Divisor (整除裁切)"}),
                "image_color": (["white", "black", "gray", "red", "green", "blue"], {"default": "white"}),
                "batch": ("INT", {"default": 1, "min": 1, "max": 16, "label": "Batch 数量"}),
                "latent_type": (latent_type_options, {"default": "standard", "label": "Latent类型"}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("IMAGE", "MASK", "LATENT", "INT", "INT")
    RETURN_NAMES = ("image", "mask", "latent", "width", "height")
    FUNCTION = "generate"

    def generate(self, width, height, ratio, scale, divisor, image_color, batch, latent_type):
        if ratio == "custom":
            w = width
            h = height
        else:
            m = re.search(r"(\d+)x(\d+)", ratio)
            if m:
                w, h = int(m.group(1)), int(m.group(2))
            else:
                w, h = 1024, 1024
        w = max(1, int(round(w * scale)))
        h = max(1, int(round(h * scale)))
        if divisor > 1:
            w = (w // divisor) * divisor
            h = (h // divisor) * divisor
        COLOR_OPTIONS = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "gray": (128, 128, 128),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
        }
        color_rgb = COLOR_OPTIONS[image_color]
        images = []
        for _ in range(batch):
            img = torch.from_numpy(np.array(Image.new("RGB", (w, h), color_rgb))).float() / 255.0
            img = img.permute(2, 0, 1)
            images.append(img)
        images = torch.stack(images, dim=0).permute(0, 2, 3, 1)
        mask_value = color_rgb[0] / 255.0
        masks = torch.ones([batch, 1, h, w], dtype=torch.float32) * mask_value
        latent_channels = {
            "standard": 4,
            "sd3": 8,
            "hunyuan": 8,
            "ltx": 16,
        }.get(latent_type, 4)
        latent = {
            "samples": torch.zeros([batch, latent_channels, h // 8, w // 8], dtype=torch.float32),
            "batch_index_list": None
        }
        return images, masks, latent, w, h

# Node mappings
NODE_CLASS_MAPPINGS = {
    "EmptyUnitGenerator_UTK": EmptyUnitGenerator_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmptyUnitGenerator_UTK": "Empty Unit Generator (UTK)",
} 