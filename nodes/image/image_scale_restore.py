"""
Image Scale Restore Node
~~~~~~~~~~~~~~~~~~~~~~~

Restores images to original size or scales them with specified parameters.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
from PIL import Image
from ..image_utils import tensor2pil, pil2tensor, image2mask

def log(message, message_type='info'):
    """简单的日志函数"""
    if message_type == 'error':
        print(f"❌ Error: {message}")
    elif message_type == 'warning':
        print(f"⚠️ Warning: {message}")
    elif message_type == 'finish':
        print(f"✅ {message}")
    else:
        print(f"ℹ️ {message}")

class ImageScaleRestore_UTK:
    CATEGORY = "UniversalToolkit/Image"
    
    @classmethod
    def INPUT_TYPES(cls):
        method_mode = ['lanczos', 'bicubic', 'hamming', 'bilinear', 'box', 'nearest']
        scale_to_list = ['None', 'longest', 'shortest', 'width', 'height', 'total_pixel(kilo pixel)']
        multiple_list = ['8', '16', '32', '64', '128', '256', '512', 'None']
        return {
            "required": {
                "image": ("IMAGE", ),
                "scale": ("FLOAT", {"default": 1, "min": 0.01, "max": 100, "step": 0.01}),
                "method": (method_mode,),
                "scale_to_side": (scale_to_list,),
                "scale_to_length": ("INT", {"default": 1024, "min": 4, "max": 1e8, "step": 1}),
                "round_to_multiple": (multiple_list,),
            },
            "optional": {
                "mask": ("MASK",),
                "original_size": ("BOX",),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "BOX", "INT", "INT")
    RETURN_NAMES = ("image", "mask", "original_size", "width", "height",)
    FUNCTION = 'image_scale_restore'

    def image_scale_restore(self, image, scale, method,
                            scale_to_side, scale_to_length, round_to_multiple,
                            mask=None, original_size=None):
        import math
        l_images = []
        l_masks = []
        ret_images = []
        ret_masks = []
        for l in image:
            l_images.append(torch.unsqueeze(l, 0))
            m = tensor2pil(l)
            if m.mode == 'RGBA':
                l_masks.append(m.split()[-1])

        if mask is not None:
            if mask.dim() == 2:
                mask = torch.unsqueeze(mask, 0)
            l_masks = []
            for m in mask:
                l_masks.append(tensor2pil(torch.unsqueeze(m, 0)).convert('L'))

        max_batch = max(len(l_images), len(l_masks))

        orig_width, orig_height = tensor2pil(l_images[0]).size
        # 计算目标宽高
        if original_size is not None:
            target_width = original_size[0]
            target_height = original_size[1]
        else:
            # 参考 image scale by aspect 的逻辑
            ratio = orig_width / orig_height if orig_height != 0 else 1.0
            if scale_to_side == 'longest':
                if orig_width >= orig_height:
                    target_width = scale_to_length
                    target_height = int(target_width / ratio)
                else:
                    target_height = scale_to_length
                    target_width = int(target_height * ratio)
            elif scale_to_side == 'shortest':
                if orig_width <= orig_height:
                    target_width = scale_to_length
                    target_height = int(target_width / ratio)
                else:
                    target_height = scale_to_length
                    target_width = int(target_height * ratio)
            elif scale_to_side == 'width':
                target_width = scale_to_length
                target_height = int(target_width / ratio)
            elif scale_to_side == 'height':
                target_height = scale_to_length
                target_width = int(target_height * ratio)
            elif scale_to_side == 'total_pixel(kilo pixel)':
                target_width = math.sqrt(ratio * scale_to_length * 1000)
                target_height = target_width / ratio
                target_width = int(target_width)
                target_height = int(target_height)
            else:
                target_width = int(orig_width * scale)
                target_height = int(orig_height * scale)

            # 对齐到倍数
            if round_to_multiple != 'None':
                multiple = int(round_to_multiple)
                def num_round_up_to_multiple(num, multiple):
                    return ((num + multiple - 1) // multiple) * multiple
                target_width = num_round_up_to_multiple(target_width, multiple)
                target_height = num_round_up_to_multiple(target_height, multiple)

        if target_width < 4:
            target_width = 4
        if target_height < 4:
            target_height = 4
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

        for i in range(max_batch):
            _image = l_images[i] if i < len(l_images) else l_images[-1]
            _canvas = tensor2pil(_image).convert('RGB')
            ret_image = _canvas.resize((target_width, target_height), resize_sampler)
            ret_mask = Image.new('L', size=ret_image.size, color='white')
            if mask is not None:
                _mask = l_masks[i] if i < len(l_masks) else l_masks[-1]
                ret_mask = _mask.resize((target_width, target_height), resize_sampler)
            ret_images.append(pil2tensor(ret_image))
            ret_masks.append(image2mask(ret_mask))

        log(f"ImageScaleRestore_UTK Processed {len(ret_images)} image(s).", message_type='finish')
        return (torch.cat(ret_images, dim=0), torch.cat(ret_masks, dim=0), [orig_width, orig_height], target_width, target_height,)

# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImageScaleRestore_UTK": ImageScaleRestore_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageScaleRestore_UTK": "Image Scale Restore (UTK)",
} 