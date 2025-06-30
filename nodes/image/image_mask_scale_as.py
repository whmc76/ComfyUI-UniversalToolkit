"""
Image Mask Scale As Node
~~~~~~~~~~~~~~~~~~~~~~~

Scales images and masks to match the dimensions of a reference image.

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

def fit_resize_image(image, target_width, target_height, fit_mode, resize_sampler, background_color="#000000"):
    """Resize image according to fit mode"""
    if fit_mode == 'letterbox':
        # Calculate scaling factor to fit within target dimensions
        scale = min(target_width / image.width, target_height / image.height)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        
        # Resize image
        resized = image.resize((new_width, new_height), resize_sampler)
        
        # Create new image with target dimensions and paste resized image
        if image.mode == 'RGB':
            result = Image.new('RGB', (target_width, target_height), background_color)
        else:
            result = Image.new('L', (target_width, target_height), 0)
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        result.paste(resized, (paste_x, paste_y))
        return result
        
    elif fit_mode == 'crop':
        # Calculate scaling factor to cover target dimensions
        scale = max(target_width / image.width, target_height / image.height)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        
        # Resize image
        resized = image.resize((new_width, new_height), resize_sampler)
        
        # Crop to target dimensions
        crop_x = (new_width - target_width) // 2
        crop_y = (new_height - target_height) // 2
        return resized.crop((crop_x, crop_y, crop_x + target_width, crop_y + target_height))
        
    else:  # fill
        # Simple resize to target dimensions
        return image.resize((target_width, target_height), resize_sampler)

class ImageMaskScaleAs_UTK:
    CATEGORY = "UniversalToolkit/Image"
    
    @classmethod
    def INPUT_TYPES(cls):
        fit_mode = ['letterbox', 'crop', 'fill']
        method_mode = ['lanczos', 'bicubic', 'hamming', 'bilinear', 'box', 'nearest']

        return {
            "required": {
                "scale_as": ("IMAGE",),
                "fit": (fit_mode,),
                "method": (method_mode,),
            },
            "optional": {
                "image": ("IMAGE",),  #
                "mask": ("MASK",),  #
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "BOX", "INT", "INT")
    RETURN_NAMES = ("image", "mask", "original_size", "width", "height",)
    FUNCTION = 'image_mask_scale_as'

    def image_mask_scale_as(self, scale_as, fit, method,
                            image=None, mask = None,
                            ):
        if scale_as.shape[0] > 0:
            _asimage = tensor2pil(scale_as[0])
        else:
            _asimage = tensor2pil(scale_as)
        target_width, target_height = _asimage.size
        _mask = Image.new('L', size=_asimage.size, color='black')
        _image = Image.new('RGB', size=_asimage.size, color='black')
        orig_width = 4
        orig_height = 4
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

        ret_images = []
        ret_masks = []
        
        if image is not None:
            for i in image:
                i = torch.unsqueeze(i, 0)
                _image = tensor2pil(i).convert('RGB')
                orig_width, orig_height = _image.size
                _image = fit_resize_image(_image, target_width, target_height, fit, resize_sampler)
                ret_images.append(pil2tensor(_image))
        if mask is not None:
            if mask.dim() == 2:
                mask = torch.unsqueeze(mask, 0)
            for m in mask:
                m = torch.unsqueeze(m, 0)
                _mask = tensor2pil(m).convert('L')
                orig_width, orig_height = _mask.size
                _mask = fit_resize_image(_mask, target_width, target_height, fit, resize_sampler).convert('L')
                ret_masks.append(image2mask(_mask))
        if len(ret_images) > 0 and len(ret_masks) >0:
            log(f"ImageMaskScaleAs_UTK Processed {len(ret_images)} image(s).", message_type='finish')
            return (torch.cat(ret_images, dim=0), torch.cat(ret_masks, dim=0), [orig_width, orig_height],target_width, target_height,)
        elif len(ret_images) > 0 and len(ret_masks) == 0:
            log(f"ImageMaskScaleAs_UTK Processed {len(ret_images)} image(s).", message_type='finish')
            return (torch.cat(ret_images, dim=0), None, [orig_width, orig_height],target_width, target_height,)
        elif len(ret_images) == 0 and len(ret_masks) > 0:
            log(f"ImageMaskScaleAs_UTK Processed {len(ret_masks)} image(s).", message_type='finish')
            return (None, torch.cat(ret_masks, dim=0), [orig_width, orig_height], target_width, target_height,)
        else:
            log(f"Error: ImageMaskScaleAs_UTK skipped, because the available image or mask is not found.", message_type='error')
            return (None, None, [orig_width, orig_height], 0, 0,)

# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImageMaskScaleAs_UTK": ImageMaskScaleAs_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageMaskScaleAs_UTK": "Image Mask Scale As (UTK)",
} 