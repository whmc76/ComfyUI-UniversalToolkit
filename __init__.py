from .nodes import (
    EmptyUnitGenerator_UTK,
    ImageRatioDetector_UTK,
    ShowInt_UTK,
    ShowFloat_UTK,
    ShowList_UTK,
    ShowText_UTK,
    PreviewMask_UTK,
)

NODE_CLASS_MAPPINGS = {
    "EmptyUnitGenerator_UTK": EmptyUnitGenerator_UTK,
    "ImageRatioDetector_UTK": ImageRatioDetector_UTK,
    "ShowInt_UTK": ShowInt_UTK,
    "ShowFloat_UTK": ShowFloat_UTK,
    "ShowList_UTK": ShowList_UTK,
    "ShowText_UTK": ShowText_UTK,
    "PreviewMask_UTK": PreviewMask_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmptyUnitGenerator_UTK": "Empty Unit Generator (UTK)",
    "ImageRatioDetector_UTK": "Image Ratio Detector (UTK)",
    "ShowInt_UTK": "Show Int (UTK)",
    "ShowFloat_UTK": "Show Float (UTK)",
    "ShowList_UTK": "Show List (UTK)",
    "ShowText_UTK": "Show Text (UTK)",
    "PreviewMask_UTK": "Preview Mask (UTK)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"] 