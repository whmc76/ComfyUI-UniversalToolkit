"""
Show Nodes
~~~~~~~~~

Display and preview nodes for various data types.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch


class Show_UTK:
    CATEGORY = "UniversalToolkit/Tools"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("STRING", "INT", "FLOAT", "LIST", "MASK", "IMAGE", "LATENT")
            }
        }

    RETURN_TYPES = ("STRING", "INT", "FLOAT", "LIST", "MASK", "IMAGE", "LATENT")
    RETURN_NAMES = ("string", "int", "float", "list", "mask", "image", "latent")
    FUNCTION = "show"
    IS_PREVIEW = True

    def show(self, input):
        outs = [None] * 7
        if isinstance(input, str):
            outs[0] = input
        elif isinstance(input, int):
            outs[1] = input
        elif isinstance(input, float):
            outs[2] = input
        elif isinstance(input, list):
            outs[3] = input
        elif hasattr(input, "shape") and len(input.shape) == 4 and input.shape[1] == 1:
            outs[4] = input  # MASK
        elif hasattr(input, "shape") and len(input.shape) == 4 and input.shape[1] == 3:
            outs[5] = input  # IMAGE
        elif isinstance(input, dict) and "samples" in input:
            outs[6] = input  # LATENT
        return tuple(outs)


# Node mappings
NODE_CLASS_MAPPINGS = {
    "Show_UTK": Show_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Show_UTK": "Show (UTK)",
}
