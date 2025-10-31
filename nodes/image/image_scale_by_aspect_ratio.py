"""
Image Scale By Aspect Ratio Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scales images to specific aspect ratios with various fitting modes.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import math

import torch
from PIL import Image, ImageFilter

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
    image,
    target_width,
    target_height,
    fit_mode,
    resize_sampler,
    background_color,
    crop_position="center",
):
    """Resize image according to fit mode"""
    if fit_mode == "resize":
        # resize: 只等比缩放，不填充，直接返回缩放后的图像
        scale = min(target_width / image.width, target_height / image.height)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        return image.resize((new_width, new_height), resize_sampler)
    
    if fit_mode in ["letterbox", "pad", "pad_edge", "pad_edge_pixel", "pillarbox_blur"]:
        # Calculate scaling factor to fit within target dimensions
        scale = min(target_width / image.width, target_height / image.height)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)

        # Resize image
        resized = image.resize((new_width, new_height), resize_sampler)

        # Create background
        if fit_mode == "pillarbox_blur":
            scale_fill = max(target_width / max(1, image.width), target_height / max(1, image.height))
            bg_w = max(1, int(round(image.width * scale_fill)))
            bg_h = max(1, int(round(image.height * scale_fill)))
            bg = image.resize((bg_w, bg_h), Image.BILINEAR)
            x0 = max(0, (bg_w - target_width) // 2)
            y0 = max(0, (bg_h - target_height) // 2)
            bg = bg.crop((x0, y0, x0 + target_width, y0 + target_height))
            sigma = max(1.0, 0.006 * float(min(target_width, target_height)))
            bg = bg.filter(ImageFilter.GaussianBlur(radius=sigma))
            if bg.mode == "RGB":
                r, g, b = bg.split()
                l = r.point(lambda v: int(0.2126 * v))
                l = Image.merge("RGB", (l, l, l))
                bg = Image.blend(bg, l, 0.2)
            bg = bg.point(lambda v: int(v * 0.35))
            result = bg
        else:
            result = Image.new(image.mode, (target_width, target_height), background_color)

        # paste position
        if crop_position == "center":
            paste_x = (target_width - new_width) // 2
            paste_y = (target_height - new_height) // 2
        elif crop_position == "top":
            paste_x = (target_width - new_width) // 2
            paste_y = 0
        elif crop_position == "bottom":
            paste_x = (target_width - new_width) // 2
            paste_y = target_height - new_height
        elif crop_position == "left":
            paste_x = 0
            paste_y = (target_height - new_height) // 2
        elif crop_position == "right":
            paste_x = target_width - new_width
            paste_y = (target_height - new_height) // 2
        else:
            paste_x = (target_width - new_width) // 2
            paste_y = (target_height - new_height) // 2

        # Apply pad_edge / pad_edge_pixel stripes
        if fit_mode in ["pad_edge", "pad_edge_pixel"]:
            left_pad = paste_x
            right_pad = target_width - (paste_x + new_width)
            top_pad = paste_y
            bottom_pad = target_height - (paste_y + new_height)

            if left_pad > 0:
                col = resized.crop((0, 0, 1, new_height))
                if fit_mode == "pad_edge_pixel":
                    result.paste(col.resize((left_pad, new_height), Image.NEAREST), (0, paste_y))
                else:
                    if col.mode == "RGB":
                        pixels = list(col.getdata())
                        r = sum(p[0] for p in pixels) // len(pixels)
                        g = sum(p[1] for p in pixels) // len(pixels)
                        b = sum(p[2] for p in pixels) // len(pixels)
                        fill = (r, g, b)
                    else:
                        v = sum(col.getdata()) // len(col.getdata())
                        fill = v
                    Image.Image.paste(result, Image.new(result.mode, (left_pad, new_height), fill), (0, paste_y))
            if right_pad > 0:
                col = resized.crop((new_width - 1, 0, new_width, new_height))
                if fit_mode == "pad_edge_pixel":
                    result.paste(col.resize((right_pad, new_height), Image.NEAREST), (paste_x + new_width, paste_y))
                else:
                    if col.mode == "RGB":
                        pixels = list(col.getdata())
                        r = sum(p[0] for p in pixels) // len(pixels)
                        g = sum(p[1] for p in pixels) // len(pixels)
                        b = sum(p[2] for p in pixels) // len(pixels)
                        fill = (r, g, b)
                    else:
                        v = sum(col.getdata()) // len(col.getdata())
                        fill = v
                    Image.Image.paste(result, Image.new(result.mode, (right_pad, new_height), fill), (paste_x + new_width, paste_y))
            if top_pad > 0:
                row = resized.crop((0, 0, new_width, 1))
                if fit_mode == "pad_edge_pixel":
                    result.paste(row.resize((new_width, top_pad), Image.NEAREST), (paste_x, 0))
                    if left_pad > 0:
                        c = resized.getpixel((0, 0))
                        Image.Image.paste(result, Image.new(result.mode, (left_pad, top_pad), c), (0, 0))
                    if right_pad > 0:
                        c = resized.getpixel((new_width - 1, 0))
                        Image.Image.paste(result, Image.new(result.mode, (right_pad, top_pad), c), (paste_x + new_width, 0))
                else:
                    if row.mode == "RGB":
                        pixels = list(row.getdata())
                        r = sum(p[0] for p in pixels) // len(pixels)
                        g = sum(p[1] for p in pixels) // len(pixels)
                        b = sum(p[2] for p in pixels) // len(pixels)
                        fill = (r, g, b)
                    else:
                        v = sum(row.getdata()) // len(row.getdata())
                        fill = v
                    Image.Image.paste(result, Image.new(result.mode, (target_width, top_pad), fill), (0, 0))
            if bottom_pad > 0:
                row = resized.crop((0, new_height - 1, new_width, new_height))
                if fit_mode == "pad_edge_pixel":
                    result.paste(row.resize((new_width, bottom_pad), Image.NEAREST), (paste_x, paste_y + new_height))
                    if left_pad > 0:
                        c = resized.getpixel((0, new_height - 1))
                        Image.Image.paste(result, Image.new(result.mode, (left_pad, bottom_pad), c), (0, paste_y + new_height))
                    if right_pad > 0:
                        c = resized.getpixel((new_width - 1, new_height - 1))
                        Image.Image.paste(result, Image.new(result.mode, (right_pad, bottom_pad), c), (paste_x + new_width, paste_y + new_height))
                else:
                    if row.mode == "RGB":
                        pixels = list(row.getdata())
                        r = sum(p[0] for p in pixels) // len(pixels)
                        g = sum(p[1] for p in pixels) // len(pixels)
                        b = sum(p[2] for p in pixels) // len(pixels)
                        fill = (r, g, b)
                    else:
                        v = sum(row.getdata()) // len(row.getdata())
                        fill = v
                    Image.Image.paste(result, Image.new(result.mode, (target_width, bottom_pad), fill), (0, paste_y + new_height))

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
        if crop_position == "center":
            crop_x = (new_width - target_width) // 2
            crop_y = (new_height - target_height) // 2
        elif crop_position == "top":
            crop_x = (new_width - target_width) // 2
            crop_y = 0
        elif crop_position == "bottom":
            crop_x = (new_width - target_width) // 2
            crop_y = new_height - target_height
        elif crop_position == "left":
            crop_x = 0
            crop_y = (new_height - target_height) // 2
        elif crop_position == "right":
            crop_x = new_width - target_width
            crop_y = (new_height - target_height) // 2
        else:
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
        fit_mode = [
            "stretch",
            "resize",
            "pad",
            "pad_edge",
            "pad_edge_pixel",
            "crop",
            "pillarbox_blur",
        ]
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
                "background_color": ([
                    "black",
                    "white",
                    "gray",
                    "red",
                    "green",
                    "blue",
                    "yellow",
                    "cyan",
                    "magenta",
                ], {"default": "black"}),
                "crop_position": (["center", "top", "bottom", "left", "right"], {"default": "center"}),
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
        "INT",
    )
    RETURN_NAMES = (
        "image",
        "mask",
        "original_size",
        "width",
        "height",
        "batch_count",
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
        crop_position,
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

        output_width = target_width
        output_height = target_height
        
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
                    crop_position,
                )
                # For resize mode, use actual image size instead of target size
                if fit == "resize":
                    output_width, output_height = _image.size
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
                    "black",
                    crop_position,
                ).convert("L")
                # For resize mode, use actual mask size instead of target size
                if fit == "resize":
                    output_width, output_height = _mask.size
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
                output_width,
                output_height,
                len(ret_images),
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
                output_width,
                output_height,
                len(ret_images),
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
                output_width,
                output_height,
                len(ret_masks),
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
                0,
            )


# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImageScaleByAspectRatio_UTK": ImageScaleByAspectRatio_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageScaleByAspectRatio_UTK": "Image Scale By Aspect Ratio (UTK)",
}
