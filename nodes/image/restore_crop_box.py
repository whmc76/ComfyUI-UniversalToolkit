"""
Restore Crop Box Node
~~~~~~~~~~~~~~~~~~~

Restores cropped images back to their original background.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
from PIL import Image

from ..image_utils import image2mask, pil2tensor, tensor2pil


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


class RestoreCropBox_UTK:
    CATEGORY = "UniversalToolkit/Image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "background_image": ("IMAGE",),
                "croped_image": ("IMAGE",),
                "invert_mask": ("BOOLEAN", {"default": False}),  # 反转mask#
                "crop_box": ("BOX",),
            },
            "optional": {
                "croped_mask": ("MASK",),
            },
        }

    RETURN_TYPES = (
        "IMAGE",
        "MASK",
    )
    RETURN_NAMES = (
        "image",
        "mask",
    )
    FUNCTION = "restore_crop_box"

    def restore_crop_box(
        self, background_image, croped_image, invert_mask, crop_box, croped_mask=None
    ):

        b_images = []
        l_images = []
        l_masks = []
        ret_images = []
        ret_masks = []
        for b in background_image:
            b_images.append(torch.unsqueeze(b, 0))
        for l in croped_image:
            l_images.append(torch.unsqueeze(l, 0))
            m = tensor2pil(l)
            if m.mode == "RGBA":
                l_masks.append(m.split()[-1])
            else:
                l_masks.append(Image.new("L", size=m.size, color="white"))
        if croped_mask is not None:
            if croped_mask.dim() == 2:
                croped_mask = torch.unsqueeze(croped_mask, 0)
            l_masks = []
            for m in croped_mask:
                if invert_mask:
                    m = 1 - m
                l_masks.append(tensor2pil(torch.unsqueeze(m, 0)).convert("L"))

        max_batch = max(len(b_images), len(l_images), len(l_masks))
        for i in range(max_batch):
            background_image = b_images[i] if i < len(b_images) else b_images[-1]
            croped_image = l_images[i] if i < len(l_images) else l_images[-1]
            _mask = l_masks[i] if i < len(l_masks) else l_masks[-1]

            _canvas = tensor2pil(background_image).convert("RGB")
            _layer = tensor2pil(croped_image).convert("RGB")

            ret_mask = Image.new("L", size=_canvas.size, color="black")
            _canvas.paste(_layer, box=tuple(crop_box), mask=_mask)
            ret_mask.paste(_mask, box=tuple(crop_box))
            ret_images.append(pil2tensor(_canvas))
            ret_masks.append(image2mask(ret_mask))

        log(
            f"RestoreCropBox_UTK Processed {len(ret_images)} image(s).",
            message_type="finish",
        )
        return (
            torch.cat(ret_images, dim=0),
            torch.cat(ret_masks, dim=0),
        )


# Node mappings
NODE_CLASS_MAPPINGS = {
    "RestoreCropBox_UTK": RestoreCropBox_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RestoreCropBox_UTK": "Restore Crop Box (UTK)",
}
