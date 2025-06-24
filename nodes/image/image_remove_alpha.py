"""
Image Remove Alpha Node
~~~~~~~~~~~~~~~~~~~~~~

Removes alpha channel from RGBA images with optional background filling.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
from PIL import Image
from ...common_utils import log, tensor2pil, pil2tensor

class ImageRemoveAlpha_UTK:
    CATEGORY = "UniversalToolkit/Image"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "RGBA_image": ("IMAGE", ),  #
                "fill_background": ("BOOLEAN", {"default": False}),
                "background_color": ("STRING", {"default": "#000000"}),
            },
            "optional": {
                "mask": ("MASK",),  #
            }
        }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("RGB_image", )
    FUNCTION = 'image_remove_alpha'

    def image_remove_alpha(self, RGBA_image, fill_background, background_color, mask=None):

        ret_images = []

        for index, img in enumerate(RGBA_image):
            _image = tensor2pil(img)

            if fill_background:
                if mask is not None:
                    m = mask[index].unsqueeze(0) if index < len(mask) else mask[-1].unsqueeze(0)
                    alpha = tensor2pil(m).convert('L')
                elif _image.mode == "RGBA":
                    alpha = _image.split()[-1]
                else:
                    log(f"Error: ImageRemoveAlpha_UTK skipped, because the input image is not RGBA and mask is None.",
                        message_type='error')
                    return (RGBA_image,)
                ret_image = Image.new('RGB', size=_image.size, color=background_color)
                ret_image.paste(_image, mask=alpha)
                ret_images.append(pil2tensor(ret_image))

            else:
                ret_images.append(pil2tensor(tensor2pil(img).convert('RGB')))

        log(f"ImageRemoveAlpha_UTK Processed {len(ret_images)} image(s).", message_type='finish')
        return (torch.cat(ret_images, dim=0), )

# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImageRemoveAlpha_UTK": ImageRemoveAlpha_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageRemoveAlpha_UTK": "Image Remove Alpha (UTK)",
} 