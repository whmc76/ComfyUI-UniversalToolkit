"""
Color to Mask Node for ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Color to mask conversion functionality adapted from kjnodes.
Converts chosen RGB values to mask based on color distance threshold.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
from comfy.utils import ProgressBar


class ColorToMask_UTK:
    """
    Color to Mask node that converts chosen RGB values to mask.
    
    This node analyzes input images and creates masks based on color similarity
    to a specified RGB color within a threshold distance. Useful for isolating
    specific colored areas in images for masking purposes.
    """
    
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "color_to_mask"
    CATEGORY = "UniversalToolkit/Tools"
    
    DESCRIPTION = """
Converts chosen RGB value to a mask based on color distance.

The node calculates the Euclidean distance between each pixel's color 
and the target RGB color. Pixels within the threshold distance are 
included in the mask (white), while others are excluded (black).

With batch inputs, the **per_batch** parameter controls the number 
of images processed at once for memory efficiency.

Parameters:
- RGB values: Target color to match (0-255)
- Threshold: Maximum color distance for inclusion (0-255)
- Invert: Flip the mask (exclude matching colors instead)
- Per batch: Number of images to process simultaneously
"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "Input images to convert to masks"}),
                "red": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 255, 
                    "step": 1,
                    "tooltip": "Red component of target color"
                }),
                "green": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 255, 
                    "step": 1,
                    "tooltip": "Green component of target color"
                }),
                "blue": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 255, 
                    "step": 1,
                    "tooltip": "Blue component of target color"
                }),
                "threshold": ("INT", {
                    "default": 10, 
                    "min": 0, 
                    "max": 255, 
                    "step": 1,
                    "tooltip": "Maximum color distance for inclusion in mask"
                }),
                "invert": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Invert the mask (exclude matching colors)"
                }),
                "per_batch": ("INT", {
                    "default": 16, 
                    "min": 1, 
                    "max": 4096, 
                    "step": 1,
                    "tooltip": "Number of images to process simultaneously"
                }),
            },
        }

    def color_to_mask(self, images, red, green, blue, threshold, invert, per_batch):
        """
        Convert RGB color to mask based on color distance threshold.
        
        Args:
            images: Input image tensor
            red: Red component of target color (0-255)
            green: Green component of target color (0-255)
            blue: Blue component of target color (0-255)
            threshold: Maximum color distance for inclusion
            invert: Whether to invert the mask
            per_batch: Number of images to process per batch
            
        Returns:
            Tuple containing the mask tensor
        """
        # Define target color and mask colors
        color = torch.tensor([red, green, blue], dtype=torch.uint8)
        black = torch.tensor([0, 0, 0], dtype=torch.uint8)
        white = torch.tensor([255, 255, 255], dtype=torch.uint8)
        
        # Swap colors if invert is True
        if invert:
            black, white = white, black

        # Initialize progress bar and output list
        steps = images.shape[0]
        pbar = ProgressBar(steps)
        tensors_out = []
        
        # Process images in batches
        for start_idx in range(0, images.shape[0], per_batch):
            end_idx = min(start_idx + per_batch, images.shape[0])
            batch_images = images[start_idx:end_idx]
            
            # Calculate color distances using Euclidean distance
            # Convert images from [0,1] to [0,255] range for comparison
            color_distances = torch.norm(batch_images * 255 - color.float(), dim=-1)
            
            # Create mask based on threshold
            mask = color_distances <= threshold
            
            # Apply mask to create output (white for match, black for no match)
            mask_out = torch.where(mask.unsqueeze(-1), white.float(), black.float())
            
            # Convert to grayscale mask by taking mean across color channels
            mask_out = mask_out.mean(dim=-1)
            
            # Normalize to [0,1] range and move to CPU
            mask_out = mask_out / 255.0
            tensors_out.append(mask_out.cpu())
            
            # Update progress bar
            batch_count = mask_out.shape[0]
            pbar.update(batch_count)
       
        # Concatenate all batches and ensure proper range
        tensors_out = torch.cat(tensors_out, dim=0)
        tensors_out = torch.clamp(tensors_out, min=0.0, max=1.0)
        
        return (tensors_out,)


# Node registration
NODE_CLASS_MAPPINGS = {
    "ColorToMask_UTK": ColorToMask_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ColorToMask_UTK": "Color To Mask (UTK)",
}
