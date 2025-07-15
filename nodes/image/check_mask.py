"""
Check Mask Node
~~~~~~~~~~~~~~

Check if a mask is valid and provide information about it.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import cv2
import numpy as np
import torch
from PIL import Image

from ..tools.logging_utils import log
from .image_converters import pil2tensor, tensor2pil


def mask_white_area(mask, white_point):
    """Calculate the percentage of white area in mask"""
    if mask is None:
        return 0.0
    mask_array = np.array(mask)
    white_pixels = np.sum(mask_array > white_point)
    total_pixels = mask_array.size
    return white_pixels / total_pixels if total_pixels > 0 else 0


class CheckMask_UTK:
    CATEGORY = "UniversalToolkit/Image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),  #
                "white_point": (
                    "INT",
                    {"default": 1, "min": 1, "max": 254, "step": 1},
                ),  # 用于判断mask是否有效的白点值，高于此值被计入有效
                "area_percent": (
                    "INT",
                    {"default": 1, "min": 1, "max": 99, "step": 1},
                ),  # 区域百分比，低于此则mask判定无效
            },
            "optional": {},  #
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("bool",)
    FUNCTION = "check_mask"

    def check_mask(
        self,
        mask,
        white_point,
        area_percent,
    ):

        if mask is None:
            log("CheckMask_UTK: mask is None", message_type="warning")
            return (False,)

        if mask.dim() == 2:
            mask = torch.unsqueeze(mask, 0)

        mask_pil = tensor2pil(mask[0])
        if mask_pil is None:
            log("CheckMask_UTK: Failed to convert mask to PIL", message_type="warning")
            return (False,)

        if mask_pil.width * mask_pil.height > 262144:
            target_width = 512
            target_height = int(target_width * mask_pil.height / mask_pil.width)
            mask_pil = mask_pil.resize((target_width, target_height), Image.LANCZOS)

        ret = mask_white_area(mask_pil, white_point) * 100 > area_percent
        log(f"CheckMask_UTK:{ret}", message_type="finish")
        return (ret,)


# Node mappings
NODE_CLASS_MAPPINGS = {
    "CheckMask_UTK": CheckMask_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CheckMask_UTK": "Check Mask (UTK)",
}
