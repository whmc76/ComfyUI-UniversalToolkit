"""
Purge VRAM Node
~~~~~~~~~~~~~~

Purge GPU memory to free up VRAM.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import gc
from .logging_utils import log
from .any_type import AnyType

# 创建 AnyType 实例
any = AnyType("*")

def clear_memory():
    """Clear GPU memory"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

class PurgeVRAM_UTK:
    CATEGORY = "UniversalToolkit/Tools"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "anything": (any, {}),
                "purge_cache": ("BOOLEAN", {"default": True}),
                "purge_models": ("BOOLEAN", {"default": True}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("anything",)
    FUNCTION = "purge_vram"
    OUTPUT_NODE = True

    def purge_vram(self, anything, purge_cache, purge_models):
        clear_memory()
        if purge_models:
            try:
                import comfy.model_management
                comfy.model_management.unload_all_models()
                comfy.model_management.soft_empty_cache()
            except ImportError:
                log("ComfyUI model management not available", message_type="warning")
        log("VRAM purged successfully", message_type="finish")
        return (anything,)

# Node mappings
NODE_CLASS_MAPPINGS = {
    "PurgeVRAM_UTK": PurgeVRAM_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PurgeVRAM_UTK": "Purge VRAM (UTK)",
} 