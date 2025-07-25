"""
Image Scale By Aspect Ratio Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scales images to specific aspect ratios with various fitting modes.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import math

import torch
from PIL import Image

from ..image_utils import (fit_resize_image, image2mask, is_valid_mask, log,
                           num_round_up_to_multiple, pil2tensor, tensor2pil)


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


def num_round_up_to_multiple(num, multiple):
    """Round up to the nearest multiple"""
    return ((num + multiple - 1) // multiple) * multiple


def fit_resize_image(
    image, target_width, target_height, fit_mode, resize_sampler, background_color
):
    """Resize image according to fit mode"""
    if fit_mode == "letterbox":
        # Calculate scaling factor to fit within target dimensions
        scale = min(target_width / image.width, target_height / image.height)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)

        # Resize image
        resized = image.resize((new_width, new_height), resize_sampler)

        # Create new image with target dimensions and paste resized image
        result = Image.new(image.mode, (target_width, target_height), background_color)
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        result.paste(resized, (paste_x, paste_y))
        return result

    elif fit_mode == "crop":
        # Calculate scaling factor to cover target dimensions
        scale = max(target_width / image.width, target_height / image.height)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)

        # Resize image
        resized = image.resize((new_width, new_height), resize_sampler)

        # Crop to target dimensions
        crop_x = (new_width - target_width) // 2
        crop_y = (new_height - target_height) // 2
        return resized.crop(
            (crop_x, crop_y, crop_x + target_width, crop_y + target_height)
        )

    else:  # fill
        # Simple resize to target dimensions
        return image.resize((target_width, target_height), resize_sampler)


class ImageScaleByAspectRatio_UTK:
    CATEGORY = "UniversalToolkit/Image"

    @classmethod
    def INPUT_TYPES(cls):
        ratio_list = [
            "original",
            "custom",
            "1:1",
            "3:2",
            "4:3",
            "16:9",
            "2:3",
            "3:4",
            "9:16",
        ]
        fit_mode = ["letterbox", "crop", "fill"]
        method_mode = ["lanczos", "bicubic", "hamming", "bilinear", "box", "nearest"]
        multiple_list = ["8", "16", "32", "64", "128", "256", "512", "None"]
        scale_to_list = [
            "None",
            "longest",
            "shortest",
            "width",
            "height",
            "total_pixel(kilo pixel)",
        ]
        return {
            "required": {
                "aspect_ratio": (ratio_list,),
                "proportional_width": (
                    "INT",
                    {"default": 1, "min": 1, "max": 1e8, "step": 1},
                ),
                "proportional_height": (
                    "INT",
                    {"default": 1, "min": 1, "max": 1e8, "step": 1},
                ),
                "fit": (fit_mode,),
                "method": (method_mode,),
                "round_to_multiple": (multiple_list,),
                "scale_to_side": (scale_to_list,),
                "scale_to_length": (
                    "INT",
                    {"default": 1024, "min": 4, "max": 1e8, "step": 1},
                ),
                "background_color": ("STRING", {"default": "#000000"}),
            },
            "optional": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
            },
        }

    RETURN_TYPES = (
        "IMAGE",
        "MASK",
        "BOX",
        "INT",
        "INT",
    )
    RETURN_NAMES = (
        "image",
        "mask",
        "original_size",
        "width",
        "height",
    )
    FUNCTION = "image_scale_by_aspect_ratio"

    def image_scale_by_aspect_ratio(
        self,
        aspect_ratio,
        proportional_width,
        proportional_height,
        fit,
        method,
        round_to_multiple,
        scale_to_side,
        scale_to_length,
        background_color,
        image=None,
        mask=None,
    ):
        orig_images = []
        orig_masks = []
        orig_width = 0
        orig_height = 0
        target_width = 0
        target_height = 0
        ratio = 1.0
        ret_images = []
        ret_masks = []
        if image is not None:
            for i in image:
                i = torch.unsqueeze(i, 0)
                orig_images.append(i)
            orig_width, orig_height = tensor2pil(orig_images[0]).size
        if mask is not None:
            if mask.dim() == 2:
                mask = torch.unsqueeze(mask, 0)
            for m in mask:
                m = torch.unsqueeze(m, 0)
                if not is_valid_mask(m) and m.shape == torch.Size([1, 64, 64]):
                    log(
                        f"Warning: ImageScaleByAspectRatio_UTK input mask is empty, ignore it.",
                        message_type="warning",
                    )
                else:
                    orig_masks.append(m)
            if len(orig_masks) > 0:
                _width, _height = tensor2pil(orig_masks[0]).size
                if (orig_width > 0 and orig_width != _width) or (
                    orig_height > 0 and orig_height != _height
                ):
                    log(
                        f"Error: ImageScaleByAspectRatio_UTK execute failed, because the mask is does'nt match image.",
                        message_type="error",
                    )
                    return (
                        None,
                        None,
                        None,
                        0,
                        0,
                    )
                elif orig_width + orig_height == 0:
                    orig_width = _width
                    orig_height = _height

        if orig_width + orig_height == 0:
            log(
                f"Error: ImageScaleByAspectRatio_UTK execute failed, because the image or mask at least one must be input.",
                message_type="error",
            )
            return (
                None,
                None,
                None,
                0,
                0,
            )

        if aspect_ratio == "original":
            ratio = orig_width / orig_height
        elif aspect_ratio == "custom":
            ratio = proportional_width / proportional_height
        else:
            s = aspect_ratio.split(":")
            ratio = int(s[0]) / int(s[1])

        # calculate target width and height
        if ratio > 1:
            if scale_to_side == "longest":
                target_width = scale_to_length
                target_height = int(target_width / ratio)
            elif scale_to_side == "shortest":
                target_height = scale_to_length
                target_width = int(target_height * ratio)
            elif scale_to_side == "width":
                target_width = scale_to_length
                target_height = int(target_width / ratio)
            elif scale_to_side == "height":
                target_height = scale_to_length
                target_width = int(target_height * ratio)
            elif scale_to_side == "total_pixel(kilo pixel)":
                target_width = math.sqrt(ratio * scale_to_length * 1000)
                target_height = target_width / ratio
                target_width = int(target_width)
                target_height = int(target_height)
            else:
                target_width = orig_width
                target_height = int(target_width / ratio)
        else:
            if scale_to_side == "longest":
                target_height = scale_to_length
                target_width = int(target_height * ratio)
            elif scale_to_side == "shortest":
                target_width = scale_to_length
                target_height = int(target_width / ratio)
            elif scale_to_side == "width":
                target_width = scale_to_length
                target_height = int(target_width / ratio)
            elif scale_to_side == "height":
                target_height = scale_to_length
                target_width = int(target_height * ratio)
            elif scale_to_side == "total_pixel(kilo pixel)":
                target_width = math.sqrt(ratio * scale_to_length * 1000)
                target_height = target_width / ratio
                target_width = int(target_width)
                target_height = int(target_height)
            else:
                target_height = orig_height
                target_width = int(target_height * ratio)

        if round_to_multiple != "None":
            multiple = int(round_to_multiple)
            target_width = num_round_up_to_multiple(target_width, multiple)
            target_height = num_round_up_to_multiple(target_height, multiple)

        _mask = Image.new("L", size=(target_width, target_height), color="black")
        _image = Image.new("RGB", size=(target_width, target_height), color="black")

        resize_sampler = Image.LANCZOS
        if method == "bicubic":
            resize_sampler = Image.BICUBIC
        elif method == "hamming":
            resize_sampler = Image.HAMMING
        elif method == "bilinear":
            resize_sampler = Image.BILINEAR
        elif method == "box":
            resize_sampler = Image.BOX
        elif method == "nearest":
            resize_sampler = Image.NEAREST

        if len(orig_images) > 0:
            for i in orig_images:
                _image = tensor2pil(i).convert("RGB")
                _image = fit_resize_image(
                    _image,
                    target_width,
                    target_height,
                    fit,
                    resize_sampler,
                    background_color,
                )
                ret_images.append(pil2tensor(_image))
        if len(orig_masks) > 0:
            for m in orig_masks:
                _mask = tensor2pil(m).convert("L")
                _mask = fit_resize_image(
                    _mask,
                    target_width,
                    target_height,
                    fit,
                    resize_sampler,
                    background_color,
                ).convert("L")
                ret_masks.append(image2mask(_mask))
        if len(ret_images) > 0 and len(ret_masks) > 0:
            log(
                f"ImageScaleByAspectRatio_UTK Processed {len(ret_images)} image(s).",
                message_type="finish",
            )
            return (
                torch.cat(ret_images, dim=0),
                torch.cat(ret_masks, dim=0),
                [orig_width, orig_height],
                target_width,
                target_height,
            )
        elif len(ret_images) > 0 and len(ret_masks) == 0:
            log(
                f"ImageScaleByAspectRatio_UTK Processed {len(ret_images)} image(s).",
                message_type="finish",
            )
            return (
                torch.cat(ret_images, dim=0),
                None,
                [orig_width, orig_height],
                target_width,
                target_height,
            )
        elif len(ret_images) == 0 and len(ret_masks) > 0:
            log(
                f"ImageScaleByAspectRatio_UTK Processed {len(ret_masks)} image(s).",
                message_type="finish",
            )
            return (
                None,
                torch.cat(ret_masks, dim=0),
                [orig_width, orig_height],
                target_width,
                target_height,
            )
        else:
            log(
                f"Error: ImageScaleByAspectRatio_UTK skipped, because the available image or mask is not found.",
                message_type="error",
            )
            return (
                None,
                None,
                None,
                0,
                0,
            )


# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImageScaleByAspectRatio_UTK": ImageScaleByAspectRatio_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageScaleByAspectRatio_UTK": "Image Scale By Aspect Ratio (UTK)",
}
