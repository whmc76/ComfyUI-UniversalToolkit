"""
Image Composite Masked Node
~~~~~~~~~~~~~~~~~~~~~~~~~~

Local implementation of ImageCompositeMasked for UniversalToolkit.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import torch.nn.functional as F

class ImageCompositeMasked:
    """
    Local implementation of ImageCompositeMasked for compositing images with masks.
    Based on KJNodes implementation.
    """
    
    @staticmethod
    def composite(self, image, mask_image, x, y, resize_mask, mask):
        """
        Composite an image with a mask at specified position.
        
        Args:
            image: Base image tensor (B, H, W, C)
            mask_image: Mask image tensor (B, H, W, C) 
            x: X offset
            y: Y offset
            resize_mask: Whether to resize mask to match image
            mask: Alpha mask tensor (B, H, W)
            
        Returns:
            Composited image tensor
        """
        if image is None:
            return (mask_image,)
        
        if mask_image is None:
            return (image,)
        
        # Ensure tensors are on the same device
        device = image.device
        mask_image = mask_image.to(device)
        mask = mask.to(device) if mask is not None else None
        
        # Get dimensions
        batch_size, image_height, image_width, channels = image.shape
        mask_batch_size, mask_height, mask_width, mask_channels = mask_image.shape
        
        # Handle batch size mismatch
        if batch_size != mask_batch_size:
            if batch_size == 1:
                mask_image = mask_image[:1]
            elif mask_batch_size == 1:
                mask_image = mask_image.expand(batch_size, -1, -1, -1)
            else:
                raise ValueError("Batch sizes must match or one must be 1")
        
        # Resize mask if needed
        if resize_mask and (mask_height != image_height or mask_width != image_width):
            mask_image = F.interpolate(
                mask_image.permute(0, 3, 1, 2),  # (B, C, H, W)
                size=(image_height, image_width),
                mode='bilinear',
                align_corners=False
            ).permute(0, 2, 3, 1)  # (B, H, W, C)
        
        # Apply mask if provided
        if mask is not None:
            if mask.shape[1:] != (image_height, image_width):
                mask = F.interpolate(
                    mask.unsqueeze(1),  # (B, 1, H, W)
                    size=(image_height, image_width),
                    mode='bilinear',
                    align_corners=False
                ).squeeze(1)  # (B, H, W)
            
            # Expand mask to match channels
            mask = mask.unsqueeze(-1).expand(-1, -1, -1, channels)
            mask_image = mask_image * mask
        
        # Calculate crop region
        if x < 0:
            crop_x = -x
            x = 0
        else:
            crop_x = 0
            
        if y < 0:
            crop_y = -y
            y = 0
        else:
            crop_y = 0
        
        # Crop mask image if needed
        if crop_x > 0 or crop_y > 0:
            mask_image = mask_image[:, crop_y:, crop_x:, :]
        
        # Calculate final dimensions
        mask_height, mask_width = mask_image.shape[1:3]
        
        # Check bounds
        if x + mask_width > image_width:
            mask_width = image_width - x
            mask_image = mask_image[:, :, :mask_width, :]
            
        if y + mask_height > image_height:
            mask_height = image_height - y
            mask_image = mask_image[:, :mask_height, :, :]
        
        # Create output image
        result = image.clone()
        
        # Composite mask image onto result
        if mask is not None:
            # Use alpha blending
            alpha = mask[:, y:y+mask_height, x:x+mask_width, :]
            result[:, y:y+mask_height, x:x+mask_width, :] = (
                result[:, y:y+mask_height, x:x+mask_width, :] * (1 - alpha) +
                mask_image * alpha
            )
        else:
            # Direct replacement
            result[:, y:y+mask_height, x:x+mask_width, :] = mask_image
        
        return (result,) 