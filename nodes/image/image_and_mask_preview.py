"""
Image And Mask Preview Node
~~~~~~~~~~~~~~~~~~~~~~~~~~

Preview an image or a mask, when both inputs are used composites the mask on top of the image.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import random
from nodes import SaveImage
import folder_paths

# 导入本地的 ImageCompositeMasked 实现
from .image_composite_masked import ImageCompositeMasked

class ImageAndMaskPreview_UTK(SaveImage):
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "white", "black"]
        return {
            "required": {
                "mask_opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "mask_color": (colors, {"default": "red"}),
                "pass_through": ("BOOLEAN", {"default": False}),
             },
            "optional": {
                "image": ("IMAGE",),
                "mask": ("MASK",),                
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("composite",)
    FUNCTION = "execute"
    CATEGORY = "UniversalToolkit/Image"
    DESCRIPTION = """
Preview an image or a mask, when both inputs are used  
composites the mask on top of the image.
with pass_through on the preview is disabled and the  
composite is returned from the composite slot instead,  
this allows for the preview to be passed for video combine  
nodes for example.
"""

    def execute(self, mask_opacity, mask_color, pass_through, filename_prefix="ComfyUI", image=None, mask=None, prompt=None, extra_pnginfo=None):
        if mask is not None and image is None:
            preview = mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3)
        elif mask is None and image is not None:
            preview = image
        elif mask is not None and image is not None:
            mask_adjusted = mask * mask_opacity
            mask_image = mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3).clone()

            color_map = {
                "red": [255, 0, 0], "green": [0, 255, 0], "blue": [0, 0, 255],
                "yellow": [255, 255, 0], "cyan": [0, 255, 255], "magenta": [255, 0, 255],
                "white": [255, 255, 255], "black": [0, 0, 0]
            }
            color_list = color_map.get(mask_color, [255, 0, 0])
            
            mask_image[:, :, :, 0] = color_list[0] / 255 # Red channel
            mask_image[:, :, :, 1] = color_list[1] / 255 # Green channel
            mask_image[:, :, :, 2] = color_list[2] / 255 # Blue channel
            
            preview, = ImageCompositeMasked.composite(self, image, mask_image, 0, 0, True, mask_adjusted)
        if pass_through:
            return (preview, )
        return(self.save_images(preview, filename_prefix, prompt, extra_pnginfo))

# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImageAndMaskPreview_UTK": ImageAndMaskPreview_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageAndMaskPreview_UTK": "Image And Mask Preview (UTK)",
} 