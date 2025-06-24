"""
Image Ratio Detector Node
~~~~~~~~~~~~~~~~~~~~~~~~

Detect the aspect ratio of an image.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import math

from ..tools.logging_utils import log

class ImageRatioDetector_UTK:
    CATEGORY = "UniversalToolkit/Image"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"image": ("IMAGE",)}}
    
    RETURN_TYPES = ("STRING", "INT", "INT", "STRING")
    RETURN_NAMES = ("ratio_str", "width", "height", "approx_ratio_str")
    FUNCTION = "detect"
    
    def detect(self, image):
        if hasattr(image, 'dim') and image.dim() == 4:
            img = image[0]
        else:
            img = image
        shape = img.shape
        if len(shape) == 3:
            if shape[0] <= 4:
                _, h, w = shape
            else:
                h, w, _ = shape
        elif len(shape) == 2:
            h, w = shape
        else:
            return "?", 0, 0, "N/A"
        h = int(h)
        w = int(w)
        if w == 0 or h == 0:
            ratio_str = "0:0"
            approx_ratio_str = "N/A"
            return ratio_str, w, h, approx_ratio_str
        gcd = math.gcd(w, h)
        ratio_str = f"{w//gcd}:{h//gcd}"
        std_ratios = {
            "1:1": 1.0,
            "16:9": 16/9,
            "4:3": 4/3,
            "3:2": 3/2,
            "2:3": 2/3,
            "3:4": 3/4,
            "9:16": 9/16,
            "5:4": 5/4,
            "7:5": 7/5,
            "21:9": 21/9,
            "5:3": 5/3,
            "3:1": 3/1,
            "1:2": 1/2,
            "2:1": 2/1,
            "1:1.85": 1/1.85,
            "1:2.35": 1/2.35,
        }
        wh_ratio = float(w) / float(h)
        approx_ratio_str = min(std_ratios.keys(), key=lambda k: abs(std_ratios[k] - wh_ratio))
        return ratio_str, w, h, approx_ratio_str

# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImageRatioDetector_UTK": ImageRatioDetector_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageRatioDetector_UTK": "Image Ratio Detector (UTK)",
} 