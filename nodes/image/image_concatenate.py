"""
Image Concatenate Node
~~~~~~~~~~~~~~~~~~~~~

Concatenates two images side by side or vertically with various options.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import torch.nn.functional as F
from ..common_utils import log

class ImageConcatenate_UTK:
    CATEGORY = "UniversalToolkit"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "direction": (
                    [   'right',
                        'down',
                        'left',
                        'up',
                        'auto',
                    ],
                    {
                    "default": 'auto'
                    }),
                "match_image_size": ("BOOLEAN", {"default": True}),
                "max_size": ("INT", {"default": 4096, "min": 64, "max": 8192, "step": 64}),
                "background_color": (["black", "white", "gray", "transparent"], {"default": "black"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "concatenate"
    
    def concatenate(self, image1, image2, direction, match_image_size, max_size, background_color):
        # Check if the batch sizes are different
        batch_size1 = image1.shape[0]
        batch_size2 = image2.shape[0]

        # 保证batch维度一致，补齐到最大batch
        if batch_size1 != batch_size2:
            max_batch_size = max(batch_size1, batch_size2)
            if batch_size1 < max_batch_size:
                last_image1 = image1[-1].unsqueeze(0).repeat(max_batch_size - batch_size1, 1, 1, 1)
                image1 = torch.cat([image1, last_image1], dim=0)
            if batch_size2 < max_batch_size:
                last_image2 = image2[-1].unsqueeze(0).repeat(max_batch_size - batch_size2, 1, 1, 1)
                image2 = torch.cat([image2, last_image2], dim=0)

        # Get original dimensions
        h1, w1 = image1.shape[1:3]
        h2, w2 = image2.shape[1:3]

        # If direction is auto, determine the best direction based on image dimensions
        if direction == 'auto':
            horizontal_ratio = (w1 + w2) / max(h1, h2)
            vertical_ratio = max(w1, w2) / (h1 + h2)
            direction = 'right' if abs(horizontal_ratio - 1) <= abs(vertical_ratio - 1) else 'down'

        # Match image sizes if requested
        if match_image_size:
            if direction in ['right', 'left', 'auto']:
                target_height = max(h1, h2)
                if h1 < target_height:
                    scale = target_height / h1
                    new_width = int(w1 * scale)
                    image1 = torch.nn.functional.interpolate(
                        image1.permute(0, 3, 1, 2),
                        size=(target_height, new_width),
                        mode='bilinear',
                        align_corners=False
                    ).permute(0, 2, 3, 1)
                if h2 < target_height:
                    scale = target_height / h2
                    new_width = int(w2 * scale)
                    image2 = torch.nn.functional.interpolate(
                        image2.permute(0, 3, 1, 2),
                        size=(target_height, new_width),
                        mode='bilinear',
                        align_corners=False
                    ).permute(0, 2, 3, 1)
            else:  # up, down
                target_width = max(w1, w2)
                if w1 < target_width:
                    scale = target_width / w1
                    new_height = int(h1 * scale)
                    image1 = torch.nn.functional.interpolate(
                        image1.permute(0, 3, 1, 2),
                        size=(new_height, target_width),
                        mode='bilinear',
                        align_corners=False
                    ).permute(0, 2, 3, 1)
                if w2 < target_width:
                    scale = target_width / w2
                    new_height = int(h2 * scale)
                    image2 = torch.nn.functional.interpolate(
                        image2.permute(0, 3, 1, 2),
                        size=(new_height, target_width),
                        mode='bilinear',
                        align_corners=False
                    ).permute(0, 2, 3, 1)

        # Update dimensions after scaling
        h1, w1 = image1.shape[1:3]
        h2, w2 = image2.shape[1:3]

        # Calculate final dimensions
        if direction in ['right', 'left']:
            final_height = max(h1, h2)
            final_width = w1 + w2
        else:  # up, down
            final_height = h1 + h2
            final_width = max(w1, w2)

        # Check if we need to scale down
        if max(final_height, final_width) > max_size:
            scale = max_size / max(final_height, final_width)
            new_h1 = int(h1 * scale)
            new_w1 = int(w1 * scale)
            new_h2 = int(h2 * scale)
            new_w2 = int(w2 * scale)
            image1 = torch.nn.functional.interpolate(
                image1.permute(0, 3, 1, 2),
                size=(new_h1, new_w1),
                mode='bilinear',
                align_corners=False
            ).permute(0, 2, 3, 1)
            image2 = torch.nn.functional.interpolate(
                image2.permute(0, 3, 1, 2),
                size=(new_h2, new_w2),
                mode='bilinear',
                align_corners=False
            ).permute(0, 2, 3, 1)
            h1, w1 = image1.shape[1:3]
            h2, w2 = image2.shape[1:3]
            if direction in ['right', 'left']:
                final_height = max(h1, h2)
                final_width = w1 + w2
            else:
                final_height = h1 + h2
                final_width = max(w1, w2)

        # Ensure both images have the same number of channels
        channels_image1 = image1.shape[-1]
        channels_image2 = image2.shape[-1]
        if channels_image1 != channels_image2:
            if channels_image1 < channels_image2:
                alpha_channel = torch.ones((*image1.shape[:-1], channels_image2 - channels_image1), device=image1.device)
                image1 = torch.cat((image1, alpha_channel), dim=-1)
            else:
                alpha_channel = torch.ones((*image2.shape[:-1], channels_image1 - channels_image2), device=image2.device)
                image2 = torch.cat((image2, alpha_channel), dim=-1)

        # 创建输出张量，batch维度与输入一致
        batch_size = image1.shape[0]
        if background_color == "transparent":
            output = torch.zeros((batch_size, final_height, final_width, image1.shape[-1]), dtype=image1.dtype, device=image1.device)
        else:
            color_value = 1.0 if background_color == "white" else 0.0 if background_color == "black" else 0.5
            output = torch.full((batch_size, final_height, final_width, image1.shape[-1]), color_value, dtype=image1.dtype, device=image1.device)

        # 计算放置位置
        if direction == 'right':
            x1 = 0
            x2 = w1
            y1 = (final_height - h1) // 2
            y2 = (final_height - h2) // 2
        elif direction == 'left':
            x1 = w2
            x2 = 0
            y1 = (final_height - h1) // 2
            y2 = (final_height - h2) // 2
        elif direction == 'down':
            x1 = (final_width - w1) // 2
            x2 = (final_width - w2) // 2
            y1 = 0
            y2 = h1
        else:  # up
            x1 = (final_width - w1) // 2
            x2 = (final_width - w2) // 2
            y1 = h2
            y2 = 0

        # 批量放置图片
        output[:, y1:y1+h1, x1:x1+w1] = image1
        output[:, y2:y2+h2, x2:x2+w2] = image2

        return (output,)

# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImageConcatenate_UTK": ImageConcatenate_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageConcatenate_UTK": "Image Concatenate",
} 