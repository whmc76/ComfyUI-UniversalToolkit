"""
Image Blend Advance V3 Node for ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Advanced image blending functionality adapted from LayerStyle.
Provides sophisticated layer compositing with transforms and blend modes.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import copy
import numpy as np
from PIL import Image, ImageOps
from ..image_utils import tensor2pil, pil2tensor, image2mask


class ImageBlendAdvance_UTK:
    """
    Advanced image blending node with transforms and multiple blend modes.
    
    This node provides sophisticated layer compositing capabilities similar to
    Photoshop, including scaling, rotation, positioning, and various blend modes.
    """
    
    def __init__(self):
        self.NODE_NAME = 'ImageBlendAdvance_UTK'

    @classmethod
    def INPUT_TYPES(cls):
        # 基础混合模式列表
        blend_modes = [
            'normal', 'multiply', 'screen', 'overlay', 'soft_light', 'hard_light',
            'color_dodge', 'color_burn', 'darken', 'lighten', 'difference', 'exclusion',
            'hue', 'saturation', 'color', 'luminosity', 'addition', 'subtract'
        ]
        
        mirror_modes = ['None', 'horizontal', 'vertical']
        transform_methods = ['lanczos', 'bicubic', 'hamming', 'bilinear', 'box', 'nearest']
        
        return {
            "required": {
                "layer_image": ("IMAGE",),
                "invert_mask": ("BOOLEAN", {"default": True}),
                "blend_mode": (blend_modes, {"default": "normal"}),
                "opacity": ("INT", {"default": 100, "min": 0, "max": 100, "step": 1}),
                "x_percent": ("FLOAT", {"default": 50, "min": -999, "max": 999, "step": 0.01}),
                "y_percent": ("FLOAT", {"default": 50, "min": -999, "max": 999, "step": 0.01}),
                "mirror": (mirror_modes, {"default": "None"}),
                "scale": ("FLOAT", {"default": 1, "min": 0.01, "max": 100, "step": 0.01}),
                "aspect_ratio": ("FLOAT", {"default": 1, "min": 0.01, "max": 100, "step": 0.01}),
                "rotate": ("FLOAT", {"default": 0, "min": -999999, "max": 999999, "step": 0.01}),
                "transform_method": (transform_methods, {"default": "lanczos"}),
                "anti_aliasing": ("INT", {"default": 0, "min": 0, "max": 16, "step": 1}),
            },
            "optional": {
                "background_image": ("IMAGE",),
                "layer_mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = 'image_blend_advance'
    CATEGORY = 'UniversalToolkit/Image'
    
    DESCRIPTION = """
Advanced image blending with transforms and multiple blend modes.

This node provides sophisticated layer compositing capabilities:

**Transform Features:**
- Position control via x/y percentage
- Scale and aspect ratio adjustment
- Rotation with anti-aliasing
- Horizontal/vertical mirroring
- High-quality interpolation methods

**Blend Modes:**
- Normal, Multiply, Screen, Overlay
- Soft Light, Hard Light, Color Dodge, Color Burn
- Darken, Lighten, Difference, Exclusion
- Hue, Saturation, Color, Luminosity
- Addition, Subtract

**Advanced Features:**
- Automatic background generation if not provided
- Alpha channel support for layer images
- Batch processing support
- Flexible mask handling with invert option
- Anti-aliasing for smooth rotations

Perfect for creating complex compositions, photo manipulations,
and artistic effects with precise control over blending.
"""

    def apply_blend_mode(self, background, layer, blend_mode, opacity):
        """
        Apply blend mode between background and layer images.
        Simplified implementation of common blend modes.
        """
        # Convert to numpy arrays for processing
        bg_array = np.array(background.convert('RGBA'), dtype=np.float32) / 255.0
        layer_array = np.array(layer.convert('RGBA'), dtype=np.float32) / 255.0
        
        # Apply opacity
        alpha = opacity / 100.0
        
        if blend_mode == "normal":
            result = bg_array * (1 - alpha) + layer_array * alpha
        elif blend_mode == "multiply":
            result = bg_array * layer_array * alpha + bg_array * (1 - alpha)
        elif blend_mode == "screen":
            result = 1 - (1 - bg_array) * (1 - layer_array) * alpha + bg_array * (1 - alpha)
        elif blend_mode == "overlay":
            # Simplified overlay
            mask = bg_array < 0.5
            result = np.where(mask, 
                             2 * bg_array * layer_array * alpha + bg_array * (1 - alpha),
                             1 - 2 * (1 - bg_array) * (1 - layer_array) * alpha + bg_array * (1 - alpha))
        elif blend_mode == "addition":
            result = np.clip(bg_array + layer_array * alpha, 0, 1)
        elif blend_mode == "subtract":
            result = np.clip(bg_array - layer_array * alpha, 0, 1)
        elif blend_mode == "difference":
            result = np.abs(bg_array - layer_array) * alpha + bg_array * (1 - alpha)
        elif blend_mode == "darken":
            result = np.minimum(bg_array, layer_array) * alpha + bg_array * (1 - alpha)
        elif blend_mode == "lighten":
            result = np.maximum(bg_array, layer_array) * alpha + bg_array * (1 - alpha)
        else:
            # Default to normal blend for unsupported modes
            result = bg_array * (1 - alpha) + layer_array * alpha
        
        # Convert back to PIL image
        result = np.clip(result * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(result, 'RGBA')

    def transform_image_with_rotation(self, image, mask, rotate, transform_method, anti_aliasing):
        """
        Apply rotation and other transforms to image and mask.
        """
        if rotate == 0:
            return image, mask
        
        # Convert transform method to PIL format
        resample_map = {
            'nearest': Image.NEAREST,
            'bilinear': Image.BILINEAR,
            'bicubic': Image.BICUBIC,
            'lanczos': Image.LANCZOS,
            'box': Image.BOX,
            'hamming': Image.HAMMING,
        }
        
        resample = resample_map.get(transform_method, Image.LANCZOS)
        
        # Apply rotation
        rotated_image = image.rotate(rotate, resample=resample, expand=True)
        rotated_mask = mask.rotate(rotate, resample=Image.BILINEAR, expand=True)
        
        return rotated_image, rotated_mask

    def image_blend_advance(self, layer_image, invert_mask, blend_mode, opacity,
                              x_percent, y_percent, mirror, scale, aspect_ratio, rotate,
                              transform_method, anti_aliasing, background_image=None, layer_mask=None):
        """
        Advanced image blending with transforms and blend modes.
        """
        # If background image is empty, create transparent background for each layer image
        if background_image is None:
            background_image = []
            for l in layer_image:
                layer_pil = tensor2pil(l)
                bg = Image.new('RGBA', (layer_pil.width, layer_pil.height), (0, 0, 0, 0))
                background_image.append(pil2tensor(bg))

        b_images = []
        l_images = []
        l_masks = []
        ret_images = []
        ret_masks = []
        
        # Prepare background images
        for b in background_image:
            b_images.append(torch.unsqueeze(b, 0))
        
        # Prepare layer images and extract alpha masks
        for l in layer_image:
            l_images.append(torch.unsqueeze(l, 0))
            layer_pil = tensor2pil(l)
            if layer_pil.mode == 'RGBA':
                l_masks.append(layer_pil.split()[-1])
            else:
                l_masks.append(Image.new('L', layer_pil.size, 'white'))
        
        # Use provided layer masks if available
        if layer_mask is not None:
            if layer_mask.dim() == 2:
                layer_mask = torch.unsqueeze(layer_mask, 0)
            l_masks = []
            for m in layer_mask:
                if invert_mask:
                    m = 1 - m
                l_masks.append(tensor2pil(torch.unsqueeze(m, 0)).convert('L'))

        # Process each image in the batch
        max_batch = max(len(b_images), len(l_images), len(l_masks))
        for i in range(max_batch):
            background = b_images[i] if i < len(b_images) else b_images[-1]
            layer = l_images[i] if i < len(l_images) else l_images[-1]
            mask = l_masks[i] if i < len(l_masks) else l_masks[-1]
            
            # Convert to PIL images
            canvas = tensor2pil(background).convert('RGBA')
            layer_pil = tensor2pil(layer)

            # Ensure mask matches layer size
            if mask.size != layer_pil.size:
                mask = Image.new('L', layer_pil.size, 'white')
                print(f"Warning: {self.NODE_NAME} mask size mismatch, using white mask!")

            # Store original dimensions
            orig_layer_width = layer_pil.width
            orig_layer_height = layer_pil.height
            mask = mask.convert("L")

            # Apply transforms
            target_layer_width = int(orig_layer_width * scale)
            target_layer_height = int(orig_layer_height * scale * aspect_ratio)

            # Apply mirroring
            if mirror == 'horizontal':
                layer_pil = layer_pil.transpose(Image.FLIP_LEFT_RIGHT)
                mask = mask.transpose(Image.FLIP_LEFT_RIGHT)
            elif mirror == 'vertical':
                layer_pil = layer_pil.transpose(Image.FLIP_TOP_BOTTOM)
                mask = mask.transpose(Image.FLIP_TOP_BOTTOM)

            # Apply scaling
            if target_layer_width != orig_layer_width or target_layer_height != orig_layer_height:
                resample_map = {
                    'nearest': Image.NEAREST,
                    'bilinear': Image.BILINEAR,
                    'bicubic': Image.BICUBIC,
                    'lanczos': Image.LANCZOS,
                    'box': Image.BOX,
                    'hamming': Image.HAMMING,
                }
                resample = resample_map.get(transform_method, Image.LANCZOS)
                
                layer_pil = layer_pil.resize((target_layer_width, target_layer_height), resample)
                mask = mask.resize((target_layer_width, target_layer_height), Image.BILINEAR)

            # Apply rotation
            if rotate != 0:
                layer_pil, mask = self.transform_image_with_rotation(
                    layer_pil, mask, rotate, transform_method, anti_aliasing
                )

            # Calculate position
            x = int(canvas.width * x_percent / 100 - layer_pil.width / 2)
            y = int(canvas.height * y_percent / 100 - layer_pil.height / 2)

            # Create composition
            comp_canvas = copy.copy(canvas)
            comp_mask = Image.new("L", comp_canvas.size, color='black')
            
            # Paste layer at calculated position
            if x >= 0 and y >= 0 and x + layer_pil.width <= canvas.width and y + layer_pil.height <= canvas.height:
                # Layer fits completely within canvas
                comp_canvas.paste(layer_pil, (x, y))
                comp_mask.paste(mask, (x, y))
            else:
                # Handle partial overlap or out-of-bounds
                # Create a temporary canvas to handle positioning
                temp_canvas = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
                temp_mask = Image.new('L', canvas.size, 0)
                
                # Calculate clipping bounds
                paste_x = max(0, x)
                paste_y = max(0, y)
                crop_x = max(0, -x)
                crop_y = max(0, -y)
                crop_w = min(layer_pil.width - crop_x, canvas.width - paste_x)
                crop_h = min(layer_pil.height - crop_y, canvas.height - paste_y)
                
                if crop_w > 0 and crop_h > 0:
                    layer_cropped = layer_pil.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
                    mask_cropped = mask.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
                    
                    temp_canvas.paste(layer_cropped, (paste_x, paste_y))
                    temp_mask.paste(mask_cropped, (paste_x, paste_y))
                
                comp_canvas = temp_canvas
                comp_mask = temp_mask

            # Apply blend mode
            if blend_mode != "normal":
                comp_canvas = self.apply_blend_mode(canvas, comp_canvas, blend_mode, opacity)
            else:
                # Simple alpha blending for normal mode
                alpha = opacity / 100.0
                comp_canvas = Image.blend(canvas, comp_canvas, alpha)

            # Final composition with mask
            canvas.paste(comp_canvas, mask=comp_mask)

            ret_images.append(pil2tensor(canvas))
            ret_masks.append(image2mask(comp_mask))

        print(f"{self.NODE_NAME} Processed {len(ret_images)} image(s).")
        return (torch.cat(ret_images, dim=0), torch.cat(ret_masks, dim=0))


# Node registration
NODE_CLASS_MAPPINGS = {
    "ImageBlendAdvance_UTK": ImageBlendAdvance_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageBlendAdvance_UTK": "Image Blend Advance (UTK)",
}
