"""
Image Combine Alpha Node
~~~~~~~~~~~~~~~~~~~~~~~

Combines RGB image with mask to create RGBA image.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
from PIL import Image

from ..image_utils import pil2tensor, tensor2pil


def log(message, message_type="info"):
    """简单的日志函数"""
    if message_type == "error":
        print(f"❌ Error: {message}")
    elif message_type == "warning":
        print(f"⚠️ Warning: {message}")
    elif message_type == "finish":
        print(f"✅ {message}")
    else:
        print(f"ℹ️ {message}")


def image_channel_split(image, mode):
    """Split image into channels"""
    if mode == "RGB":
        return image.split()
    elif mode == "RGBA":
        return image.split()
    else:
        return image.split()


def image_channel_merge(channels, mode):
    """Merge channels into image"""
    if mode == "RGBA":
        return Image.merge("RGBA", channels)
    elif mode == "RGB":
        return Image.merge("RGB", channels)
    else:
        return Image.merge(mode, channels)


class ImageCombineAlpha_UTK:
    CATEGORY = "UniversalToolkit/Image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "RGB_image": ("IMAGE",),  #
                "mask": ("MASK",),  #
            },
            "optional": {},
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("RGBA_image",)
    FUNCTION = "image_combine_alpha"

    def image_combine_alpha(self, RGB_image, mask):

        ret_images = []
        input_images = []
        input_masks = []

        for i in RGB_image:
            input_images.append(torch.unsqueeze(i, 0))
        if mask.dim() == 2:
            mask = torch.unsqueeze(mask, 0)
        for m in mask:
            input_masks.append(torch.unsqueeze(m, 0))

        max_batch = max(len(input_images), len(input_masks))
        for i in range(max_batch):
            _image = input_images[i] if i < len(input_images) else input_images[-1]
            _mask = input_masks[i] if i < len(input_masks) else input_masks[-1]
            r, g, b = image_channel_split(tensor2pil(_image).convert("RGB"), "RGB")
            ret_image = image_channel_merge(
                (r, g, b, tensor2pil(_mask).convert("L")), "RGBA"
            )

            ret_images.append(pil2tensor(ret_image))

        log(
            f"ImageCombineAlpha_UTK Processed {len(ret_images)} image(s).",
            message_type="finish",
        )
        return (torch.cat(ret_images, dim=0),)


# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImageCombineAlpha_UTK": ImageCombineAlpha_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageCombineAlpha_UTK": "Image Combine Alpha (UTK)",
}
