"""
Image Crop By Mask And Resize Node for ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Image crop by mask and resize functionality adapted from kjnodes.
Crops images based on mask detection and optionally resizes to target resolution.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
from comfy.utils import common_upscale
from nodes import MAX_RESOLUTION


class ImageCropByMaskAndResize_UTK:
    """
    Image Crop By Mask And Resize node that crops images based on mask detection
    and optionally resizes them to a target resolution.
    
    This node implements the kjnodes approach for batch processing:
    1. Analyze all masks to find optimal crop regions
    2. Calculate unified dimensions for consistent output
    3. Crop all images using unified dimensions
    4. Optionally resize to target resolution
    """
    
    RETURN_TYPES = ("IMAGE", "MASK", "BBOX")
    RETURN_NAMES = ("images", "masks", "bbox")
    FUNCTION = "crop"
    CATEGORY = "UniversalToolkit/Image"
    
    DESCRIPTION = """
Crops images based on mask detection and optionally resizes to target resolution.

This node processes batches of images and masks, ensuring all outputs have
consistent dimensions. It uses a three-stage approach:

1. **Analysis Stage**: Detect crop regions for each mask individually
2. **Unification Stage**: Calculate optimal unified dimensions 
3. **Processing Stage**: Crop all images with unified dimensions and resize

Features:
- **Batch Processing**: Handles multiple images and masks correctly
- **16-pixel Alignment**: Ensures dimensions are divisible by 16 (AI-friendly)
- **Aspect Ratio Preservation**: Maintains proportions during resize
- **Flexible Constraints**: Min/max crop resolution limits
- **Quality Scaling**: Uses high-quality Lanczos for images, bilinear for masks

Parameters:
- **base_resolution**: Target resolution for the longer side
- **padding**: Extra padding around detected regions  
- **min/max_crop_resolution**: Constraints for crop region size
"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "base_resolution": ("INT", {
                    "default": 512, 
                    "min": 64, 
                    "max": MAX_RESOLUTION, 
                    "step": 16
                }),
                "padding": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": MAX_RESOLUTION, 
                    "step": 1
                }),
                "min_crop_resolution": ("INT", {
                    "default": 128, 
                    "min": 64, 
                    "max": MAX_RESOLUTION, 
                    "step": 16
                }),
                "max_crop_resolution": ("INT", {
                    "default": 512, 
                    "min": 64, 
                    "max": MAX_RESOLUTION, 
                    "step": 16
                }),
            },
        }

    def crop_by_mask(self, mask, padding=0, min_crop_resolution=None, max_crop_resolution=None):
        """
        Detect crop region for a single mask using kjnodes algorithm.
        """
        iy, ix = (mask == 1).nonzero(as_tuple=True)
        h0, w0 = mask.shape

        if iy.numel() == 0:
            x_c = w0 / 2.0
            y_c = h0 / 2.0
            width = 0
            height = 0
        else:
            x_min = ix.min().item()
            x_max = ix.max().item()
            y_min = iy.min().item()
            y_max = iy.max().item()

            width = x_max - x_min
            height = y_max - y_min

            if width > w0 or height > h0:
                raise Exception("Masked area out of bounds")

            x_c = (x_min + x_max) / 2.0
            y_c = (y_min + y_max) / 2.0

        if min_crop_resolution:
            width = max(width, min_crop_resolution)
            height = max(height, min_crop_resolution)

        if max_crop_resolution:
            width = min(width, max_crop_resolution)
            height = min(height, max_crop_resolution)

        if w0 <= width:
            x0 = 0
            w = w0
        else:
            x0 = max(0, x_c - width / 2 - padding)
            w = width + 2 * padding
            if x0 + w > w0:
                x0 = w0 - w

        if h0 <= height:
            y0 = 0
            h = h0
        else:
            y0 = max(0, y_c - height / 2 - padding)
            h = height + 2 * padding
            if y0 + h > h0:
                y0 = h0 - h

        return (int(x0), int(y0), int(w), int(h))

    def crop(self, image, mask, base_resolution, padding=0, min_crop_resolution=128, max_crop_resolution=512):
        """
        Crop images by mask and resize to target resolution.
        Implements kjnodes batch processing strategy.
        """
        mask = mask.round()
        image_list = []
        mask_list = []
        bbox_list = []

        # === Stage 1: Collect all bounding boxes ===
        bbox_params = []
        aspect_ratios = []
        
        for i in range(image.shape[0]):
            x0, y0, w, h = self.crop_by_mask(
                mask[i], 
                padding, 
                min_crop_resolution, 
                max_crop_resolution
            )
            bbox_params.append((x0, y0, w, h))
            aspect_ratios.append(w / h if h > 0 else 1.0)

        # === Stage 2: Calculate unified dimensions ===
        max_w = max([w for x0, y0, w, h in bbox_params])
        max_h = max([h for x0, y0, w, h in bbox_params])
        max_aspect_ratio = max(aspect_ratios) if aspect_ratios else 1.0

        # Ensure dimensions are divisible by 16 (kjnodes standard)
        max_w = (max_w + 15) // 16 * 16
        max_h = (max_h + 15) // 16 * 16
        
        # Calculate target dimensions based on aspect ratio
        if max_aspect_ratio > 1:
            target_width = base_resolution
            target_height = int(base_resolution / max_aspect_ratio)
        else:
            target_height = base_resolution
            target_width = int(base_resolution * max_aspect_ratio)

        # === Stage 3: Process each image with unified dimensions ===
        for i in range(image.shape[0]):
            x0, y0, w, h = bbox_params[i]

            # Adjust cropping to use maximum width and height
            x_center = x0 + w / 2
            y_center = y0 + h / 2

            x0_new = int(max(0, x_center - max_w / 2))
            y0_new = int(max(0, y_center - max_h / 2))
            x1_new = int(min(x0_new + max_w, image.shape[2]))
            y1_new = int(min(y0_new + max_h, image.shape[1]))
            x0_new = x1_new - max_w
            y0_new = y1_new - max_h

            # Crop image and mask
            cropped_image = image[i][y0_new:y1_new, x0_new:x1_new, :]
            cropped_mask = mask[i][y0_new:y1_new, x0_new:x1_new]
            
            # Ensure target dimensions are divisible by 16
            target_width = (target_width + 15) // 16 * 16
            target_height = (target_height + 15) // 16 * 16

            # Resize using ComfyUI's common_upscale
            cropped_image = cropped_image.unsqueeze(0).movedim(-1, 1)  # (B, C, H, W)
            cropped_image = common_upscale(cropped_image, target_width, target_height, "lanczos", "disabled")
            cropped_image = cropped_image.movedim(1, -1).squeeze(0)  # (H, W, C)

            cropped_mask = cropped_mask.unsqueeze(0).unsqueeze(0)  # (1, 1, H, W)
            cropped_mask = common_upscale(cropped_mask, target_width, target_height, 'bilinear', "disabled")
            cropped_mask = cropped_mask.squeeze(0).squeeze(0)  # (H, W)

            image_list.append(cropped_image)
            mask_list.append(cropped_mask)
            bbox_list.append((x0_new, y0_new, x1_new, y1_new))

        return (torch.stack(image_list), torch.stack(mask_list), bbox_list)


# Node registration
NODE_CLASS_MAPPINGS = {
    "ImageCropByMaskAndResize_UTK": ImageCropByMaskAndResize_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageCropByMaskAndResize_UTK": "Image Crop By Mask And Resize (UTK)",
}
