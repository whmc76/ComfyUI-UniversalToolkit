"""
Check Mask Node
~~~~~~~~~~~~~~

Checks if a mask is valid based on white area percentage.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
from PIL import Image
import numpy as np
from ...common_utils import log, tensor2pil, pil2tensor

def mask_white_area(mask, white_point):
    """Calculate the percentage of white area in mask"""
    mask_array = np.array(mask)
    white_pixels = np.sum(mask_array > white_point)
    total_pixels = mask_array.size
    return white_pixels / total_pixels if total_pixels > 0 else 0

class CheckMask_UTK:
    CATEGORY = "UniversalToolkit"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),  #
                "white_point": ("INT", {"default": 1, "min": 1, "max": 254, "step": 1}), # 用于判断mask是否有效的白点值，高于此值被计入有效
                "area_percent": ("INT", {"default": 1, "min": 1, "max": 99, "step": 1}), # 区域百分比，低于此则mask判定无效
            },
            "optional": { #
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ('bool',)
    FUNCTION = 'check_mask'

    def check_mask(self, mask, white_point, area_percent,):

        if mask.dim() == 2:
            mask = torch.unsqueeze(mask, 0)
        mask = tensor2pil(mask[0])
        if mask.width * mask.height > 262144:
            target_width = 512
            target_height = int(target_width * mask.height / mask.width)
            mask = mask.resize((target_width, target_height), Image.LANCZOS)
        ret = mask_white_area(mask, white_point) * 100 > area_percent
        log(f"CheckMask_UTK:{ret}", message_type="finish")
        return (ret,)

# Node mappings
NODE_CLASS_MAPPINGS = {
    "CheckMask_UTK": CheckMask_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CheckMask_UTK": "Check Mask (UTK)",
} 