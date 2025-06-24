"""
Imitation Hue Node
~~~~~~~~~~~~~~~~~

Performs color transfer and imitation between images with skin protection.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import numpy as np
import cv2

from .color_utils import color_transfer
from .image_converters import tensor2cv2

class ImitationHueNode_UTK:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "imitation_image": ("IMAGE",),
                "target_image": ("IMAGE",),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 1.0, "step": 0.1}),
                "skin_protection": ("FLOAT", {"default": 0.2, "min": 0, "max": 1.0, "step": 0.1}),
                "auto_brightness": ("BOOLEAN", {"default": True}),
                "brightness_range": ("FLOAT", {"default": 0.5, "min": 0.1, "max": 1.0, "step": 0.1}),
                "auto_contrast": ("BOOLEAN", {"default": False}),
                "contrast_range": ("FLOAT", {"default": 0.5, "min": 0.1, "max": 1.0, "step": 0.1}),
                "auto_saturation": ("BOOLEAN", {"default": False}),
                "saturation_range": ("FLOAT", {"default": 0.5, "min": 0.1, "max": 1.0, "step": 0.1}),
                "auto_tone": ("BOOLEAN", {"default": False}),
                "tone_strength": ("FLOAT", {"default": 0.5, "min": 0.1, "max": 1.0, "step": 0.1}),
            },
            "optional": {
                "mask": ("MASK", {"default": None}),
            },
        }

    CATEGORY = "UniversalToolkit/Image"

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "imitation_hue"
    DESCRIPTION = """
Performs color transfer and imitation between images with skin protection.
"""

    def imitation_hue(self, imitation_image, target_image, strength, skin_protection, auto_brightness, brightness_range,
                     auto_contrast, contrast_range, auto_saturation, saturation_range, auto_tone, tone_strength,
                     mask=None):
        # Convert tensors to OpenCV format
        imitation_cv2 = tensor2cv2(imitation_image)
        target_cv2 = tensor2cv2(target_image)
        
        # Convert mask if provided
        mask_cv2 = None
        if mask is not None:
            mask_cv2 = (mask.cpu().numpy() * 255).astype(np.uint8)
        
        # Perform color transfer
        result = color_transfer(
            source=imitation_cv2,
            target=target_cv2,
            mask=mask_cv2,
            strength=strength,
            skin_protection=skin_protection,
            auto_brightness=auto_brightness,
            brightness_range=brightness_range,
            auto_contrast=auto_contrast,
            contrast_range=contrast_range,
            auto_saturation=auto_saturation,
            saturation_range=saturation_range,
            auto_tone=auto_tone,
            tone_strength=tone_strength
        )
        
        # Convert back to tensor
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result_tensor = torch.from_numpy(result_rgb.astype(np.float32) / 255.0)
        
        return (result_tensor,)

# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImitationHueNode_UTK": ImitationHueNode_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImitationHueNode_UTK": "Imitation Hue Node (UTK)",
} 