"""
Image Concatenate Multi Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Concatenates multiple images in various directions and layouts.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch

class ImageConcatenateMulti_UTK:
    CATEGORY = "UniversalToolkit"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
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
                "grid_size": (["auto", "1x1", "2x2", "3x3", "4x4"], {"default": "auto"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "concatenate_multi"
    
    def concatenate_multi(self, images, direction, match_image_size, max_size, background_color, grid_size):
        if len(images.shape) != 4:
            raise ValueError("输入必须是4D张量 [batch, height, width, channels]")
        
        batch_size = images.shape[0]
        
        # 处理网格布局
        if grid_size != "auto":
            rows, cols = map(int, grid_size.split("x"))
            if batch_size > rows * cols:
                raise ValueError(f"图像数量 ({batch_size}) 超过网格大小 ({grid_size})")
            # 填充到网格大小
            if batch_size < rows * cols:
                padding = torch.zeros((rows * cols - batch_size, *images.shape[1:]), dtype=images.dtype, device=images.device)
                images = torch.cat([images, padding], dim=0)
                batch_size = rows * cols
        else:
            # 自动计算网格大小
            if direction in ['right', 'left', 'auto']:
                rows = 1
                cols = batch_size
            else:  # up, down
                rows = batch_size
                cols = 1

        # 获取所有图像的尺寸
        heights = []
        widths = []
        for i in range(batch_size):
            h, w = images[i].shape[:2]
            heights.append(h)
            widths.append(w)

        # 如果方向是auto，计算最佳方向
        if direction == 'auto':
            # 计算水平和垂直拼接的宽高比
            total_width = sum(widths)
            max_height = max(heights)
            horizontal_ratio = total_width / max_height

            total_height = sum(heights)
            max_width = max(widths)
            vertical_ratio = max_width / total_height

            # 选择更接近1:1的方向
            direction = 'right' if abs(horizontal_ratio - 1) <= abs(vertical_ratio - 1) else 'down'

        # 如果需要匹配图像尺寸
        if match_image_size:
            if direction in ['right', 'left', 'auto']:
                # 匹配高度
                target_height = max(heights)
                for i in range(batch_size):
                    if heights[i] < target_height:
                        scale = target_height / heights[i]
                        new_width = int(widths[i] * scale)
                        images[i] = torch.nn.functional.interpolate(
                            images[i].unsqueeze(0).permute(0, 3, 1, 2),
                            size=(target_height, new_width),
                            mode='bilinear',
                            align_corners=False
                        ).permute(0, 2, 3, 1).squeeze(0)
            else:  # up, down
                # 匹配宽度
                target_width = max(widths)
                for i in range(batch_size):
                    if widths[i] < target_width:
                        scale = target_width / widths[i]
                        new_height = int(heights[i] * scale)
                        images[i] = torch.nn.functional.interpolate(
                            images[i].unsqueeze(0).permute(0, 3, 1, 2),
                            size=(new_height, target_width),
                            mode='bilinear',
                            align_corners=False
                        ).permute(0, 2, 3, 1).squeeze(0)

        # 更新尺寸
        heights = []
        widths = []
        for i in range(batch_size):
            h, w = images[i].shape[:2]
            heights.append(h)
            widths.append(w)

        # 计算最终输出尺寸
        if direction in ['right', 'left', 'auto']:
            final_height = max(heights)
            final_width = sum(widths)
        else:  # up, down
            final_height = sum(heights)
            final_width = max(widths)

        # 检查是否需要缩放
        if max(final_height, final_width) > max_size:
            scale = max_size / max(final_height, final_width)
            for i in range(batch_size):
                new_height = int(heights[i] * scale)
                new_width = int(widths[i] * scale)
                images[i] = torch.nn.functional.interpolate(
                    images[i].unsqueeze(0).permute(0, 3, 1, 2),
                    size=(new_height, new_width),
                    mode='bilinear',
                    align_corners=False
                ).permute(0, 2, 3, 1).squeeze(0)

        # 更新最终尺寸
        heights = []
        widths = []
        for i in range(batch_size):
            h, w = images[i].shape[:2]
            heights.append(h)
            widths.append(w)

        if direction in ['right', 'left', 'auto']:
            final_height = max(heights)
            final_width = sum(widths)
        else:  # up, down
            final_height = sum(heights)
            final_width = max(widths)

        # 创建输出张量
        if background_color == "transparent":
            output = torch.zeros((1, final_height, final_width, images.shape[-1]), dtype=images.dtype, device=images.device)
        else:
            color_value = 1.0 if background_color == "white" else 0.0 if background_color == "black" else 0.5
            output = torch.full((1, final_height, final_width, images.shape[-1]), color_value, dtype=images.dtype, device=images.device)

        # 放置图像
        if direction in ['right', 'left', 'auto']:
            x_offset = 0
            for i in range(batch_size):
                h, w = images[i].shape[:2]
                y_offset = (final_height - h) // 2
                if direction == 'left':
                    x_offset = final_width - sum(widths[i:])
                output[0, y_offset:y_offset+h, x_offset:x_offset+w] = images[i]
                if direction != 'left':
                    x_offset += w
        else:  # up, down
            y_offset = 0
            for i in range(batch_size):
                h, w = images[i].shape[:2]
                x_offset = (final_width - w) // 2
                if direction == 'up':
                    y_offset = final_height - sum(heights[i:])
                output[0, y_offset:y_offset+h, x_offset:x_offset+w] = images[i]
                if direction != 'up':
                    y_offset += h

        return (output,)

# Node mappings
NODE_CLASS_MAPPINGS = {
    "ImageConcatenateMulti_UTK": ImageConcatenateMulti_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageConcatenateMulti_UTK": "Image Concatenate Multi (UTK)",
} 