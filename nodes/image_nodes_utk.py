import torch
import torch.nn.functional as F
import numpy as np
import re
import math
import random
import os
import json
from comfy.utils import ProgressBar, common_upscale
from PIL import Image
from PIL.PngImagePlugin import PngInfo

# Import ComfyUI modules with fallbacks
MAX_RESOLUTION = 8192
SaveImage = None
ImageCompositeMasked = None
args = None
folder_paths = None

try:
    from nodes import MAX_RESOLUTION, SaveImage
except ImportError:
    pass

try:
    from comfy_extras.nodes_mask import ImageCompositeMasked
except ImportError:
    pass

try:
    from comfy.cli_args import args
except ImportError:
    pass

try:
    import folder_paths
except ImportError:
    pass

class EmptyUnitGenerator_UTK:
    CATEGORY = "UniversalToolkit"
    @classmethod
    def INPUT_TYPES(cls):
        ratio_options = [
            "custom",
            "SD1.5 - 1:1 square 512x512",
            "SD1.5 - 2:3 portrait 512x768",
            "SD1.5 - 3:4 portrait 512x682",
            "SD1.5 - 3:2 landscape 768x512",
            "SD1.5 - 4:3 landscape 682x512",
            "SD1.5 - 16:9 cinema 910x512",
            "SD1.5 - 1.85:1 cinema 952x512",
            "SD1.5 - 2:1 cinema 1024x512",
            "SDXL - 1:1 square 1024x1024",
            "SDXL - 3:4 portrait 896x1152",
            "SDXL - 5:8 portrait 832x1216",
            "SDXL - 9:16 portrait 768x1344",
            "SDXL - 9:21 portrait 640x1536",
            "SDXL - 4:3 landscape 1152x896",
            "SDXL - 3:2 landscape 1216x832",
            "SDXL - 16:9 landscape 1344x768",
            "SDXL - 21:9 landscape 1536x640",
        ]
        latent_type_options = ["standard", "sd3", "hunyuan", "ltx"]
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 4096, "step": 8, "label": "Width (custom only)"}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 4096, "step": 8, "label": "Height (custom only)"}),
                "ratio": (ratio_options, {"default": ratio_options[9], "label": "Resolution/Ratio"}),
                "scale": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 8.0, "step": 0.1, "label": "Scale (放大倍数)"}),
                "divisor": ("INT", {"default": 8, "min": 1, "max": 512, "step": 1, "label": "Divisor (整除裁切)"}),
                "image_color": (["white", "black", "gray", "red", "green", "blue"], {"default": "white"}),
                "batch": ("INT", {"default": 1, "min": 1, "max": 16, "label": "Batch 数量"}),
                "latent_type": (latent_type_options, {"default": "standard", "label": "Latent类型"}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("IMAGE", "MASK", "LATENT", "INT", "INT")
    RETURN_NAMES = ("image", "mask", "latent", "width", "height")
    FUNCTION = "generate"

    def generate(self, width, height, ratio, scale, divisor, image_color, batch, latent_type):
        if ratio == "custom":
            w = width
            h = height
        else:
            m = re.search(r"(\d+)x(\d+)", ratio)
            if m:
                w, h = int(m.group(1)), int(m.group(2))
            else:
                w, h = 1024, 1024
        w = max(1, int(round(w * scale)))
        h = max(1, int(round(h * scale)))
        if divisor > 1:
            w = (w // divisor) * divisor
            h = (h // divisor) * divisor
        COLOR_OPTIONS = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "gray": (128, 128, 128),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
        }
        color_rgb = COLOR_OPTIONS[image_color]
        images = []
        for _ in range(batch):
            img = torch.from_numpy(np.array(Image.new("RGB", (w, h), color_rgb))).float() / 255.0
            img = img.permute(2, 0, 1)
            images.append(img)
        images = torch.stack(images, dim=0)
        mask_value = color_rgb[0] / 255.0
        masks = torch.ones([batch, 1, h, w], dtype=torch.float32) * mask_value
        latent_channels = {
            "standard": 4,
            "sd3": 8,
            "hunyuan": 8,
            "ltx": 16,
        }.get(latent_type, 4)
        latent = {
            "samples": torch.zeros([batch, latent_channels, h // 8, w // 8], dtype=torch.float32),
            "batch_index_list": None
        }
        return images, masks, latent, w, h

class ImageRatioDetector_UTK:
    CATEGORY = "UniversalToolkit"
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"image": ("IMAGE",)}}
    RETURN_TYPES = ("STRING", "INT", "INT", "STRING")
    RETURN_NAMES = ("ratio_str", "width", "height", "approx_ratio_str")
    FUNCTION = "detect"
    def detect(self, image):
        if hasattr(image, 'dim') and image.dim() == 4:
            img = image[0]
        else:
            img = image
        shape = img.shape
        if len(shape) == 3:
            if shape[0] <= 4:
                _, h, w = shape
            else:
                h, w, _ = shape
        elif len(shape) == 2:
            h, w = shape
        else:
            return "?", 0, 0, "N/A"
        h = int(h)
        w = int(w)
        if w == 0 or h == 0:
            ratio_str = "0:0"
            approx_ratio_str = "N/A"
            return ratio_str, w, h, approx_ratio_str
        gcd = math.gcd(w, h)
        ratio_str = f"{w//gcd}:{h//gcd}"
        std_ratios = {
            "1:1": 1.0,
            "16:9": 16/9,
            "4:3": 4/3,
            "3:2": 3/2,
            "2:3": 2/3,
            "3:4": 3/4,
            "9:16": 9/16,
            "5:4": 5/4,
            "7:5": 7/5,
            "21:9": 21/9,
            "5:3": 5/3,
            "3:1": 3/1,
            "1:2": 1/2,
            "2:1": 2/1,
            "1:1.85": 1/1.85,
            "1:2.35": 1/2.35,
        }
        wh_ratio = float(w) / float(h)
        approx_ratio_str = min(std_ratios.keys(), key=lambda k: abs(std_ratios[k] - wh_ratio))
        return ratio_str, w, h, approx_ratio_str 

class DepthMapBlur_UTK:
    CATEGORY = "UniversalToolkit"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "depth_map": ("IMAGE",),
                "blur_strength": ("FLOAT", {"default": 64.0, "min": 0.0, "max": 256.0, "step": 1.0}),
                "focal_depth": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "focus_spread": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1}),
                "steps": ("INT", {"default": 5, "min": 1, "max": 32, "step": 1}),
                "focal_range": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "mask_blur": ("INT", {"default": 1, "min": 1, "max": 127, "step": 1}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_depth_blur"
    
    def apply_depth_blur(self, image, depth_map, blur_strength, focal_depth, focus_spread, steps, focal_range, mask_blur):
        # 确保输入图像和深度图具有相同的尺寸
        if image.shape[2:] != depth_map.shape[2:]:
            depth_map = torch.nn.functional.interpolate(depth_map, size=image.shape[2:], mode='bilinear', align_corners=False)
        
        # 将深度图转换为灰度图
        if depth_map.shape[1] == 3:
            depth_map = depth_map.mean(dim=1, keepdim=True)
        
        # 归一化深度图
        depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-8)
        
        # 计算模糊强度图
        depth_diff = torch.abs(depth_map - focal_depth)
        blur_map = torch.clamp(depth_diff * blur_strength / focus_spread, 0, blur_strength)
        
        # 应用焦点范围
        if focal_range > 0:
            focus_mask = torch.where(depth_diff < focal_range, 1.0, 0.0)
            blur_map = blur_map * (1 - focus_mask)
        
        # 对模糊强度图进行平滑处理
        if mask_blur > 1:
            blur_map = torch.nn.functional.avg_pool2d(blur_map, kernel_size=mask_blur, stride=1, padding=mask_blur//2)
        
        # 应用高斯模糊
        result = image.clone()
        for i in range(steps):
            # 计算当前步骤的模糊强度
            current_blur = blur_map * (i + 1) / steps
            
            # 对每个通道分别应用高斯模糊
            blurred = torch.zeros_like(result)
            for c in range(result.shape[1]):
                channel = result[:, c:c+1]
                kernel_size = torch.clamp(current_blur * 2 + 1, 3, 31).int()
                kernel_size = kernel_size + (kernel_size % 2 == 0).int()  # 确保是奇数
                padding = kernel_size // 2
                
                # 应用高斯模糊
                blurred[:, c:c+1] = torch.nn.functional.avg_pool2d(
                    channel,
                    kernel_size=kernel_size,
                    stride=1,
                    padding=padding
                )
            
            # 混合原始图像和模糊后的图像
            result = result * (1 - current_blur) + blurred * current_blur
        
        return (result,) 

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

class ImagePadForOutpaintMasked_UTK:
    CATEGORY = "UniversalToolkit"

    @classmethod
    def INPUT_TYPES(cls):
        color_options = ["gray", "white", "black", "red", "green", "blue", "yellow", "cyan", "magenta"]
        return {
            "required": {
                "image": ("IMAGE",),
                "data_mode": (["pixel", "percent"], {"default": "pixel"}),
                "left": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
                "top": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
                "right": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
                "bottom": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
                "feathering": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                "background_color": (color_options, {"default": "gray"}),
            },
            "optional": {
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "expand_image"

    def expand_image(self, image, data_mode, left, top, right, bottom, feathering, background_color, mask=None):
        B, H, W, C = image.size()
        # 处理 pad 参数
        if data_mode == "percent":
            left = int(W * left / 100)
            right = int(W * right / 100)
            top = int(H * top / 100)
            bottom = int(H * bottom / 100)
        # 背景色映射
        color_map = {
            "gray": [0.5, 0.5, 0.5],
            "white": [1.0, 1.0, 1.0],
            "black": [0.0, 0.0, 0.0],
            "red": [1.0, 0.0, 0.0],
            "green": [0.0, 1.0, 0.0],
            "blue": [0.0, 0.0, 1.0],
            "yellow": [1.0, 1.0, 0.0],
            "cyan": [0.0, 1.0, 1.0],
            "magenta": [1.0, 0.0, 1.0],
        }
        bg_rgb = color_map.get(background_color, [0.5, 0.5, 0.5])
        # 新图像
        new_image = torch.ones((B, H + top + bottom, W + left + right, C), dtype=torch.float32) 
        for i in range(C):
            new_image[:, :, :, i] = bg_rgb[i]
        new_image[:, top:top + H, left:left + W, :] = image
        # 掩码逻辑与原实现一致
        if mask is not None:
            if torch.allclose(mask, torch.zeros_like(mask)):
                print("Warning: The incoming mask is fully black. Handling it as None.")
                mask = None
        if mask is None:
            new_mask = torch.ones((B, H + top + bottom, W + left + right), dtype=torch.float32)
            t = torch.zeros((B, H, W), dtype=torch.float32)
        else:
            mask = F.pad(mask, (left, right, top, bottom), mode='constant', value=0)
            mask = 1 - mask
            t = torch.zeros_like(mask)
        if feathering > 0 and feathering * 2 < H and feathering * 2 < W:
            for i in range(H):
                for j in range(W):
                    dt = i if top != 0 else H
                    db = H - i if bottom != 0 else H
                    dl = j if left != 0 else W
                    dr = W - j if right != 0 else W
                    d = min(dt, db, dl, dr)
                    if d >= feathering:
                        continue
                    v = (feathering - d) / feathering
                    if mask is None:
                        t[:, i, j] = v * v
                    else:
                        t[:, top + i, left + j] = v * v
        if mask is None:
            new_mask[:, top:top + H, left:left + W] = t
            return (new_image, new_mask,)
        else:
            return (new_image, mask,)

class ImageAndMaskPreview_UTK(SaveImage):
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "white", "black"]
        return {
            "required": {
                "mask_opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "mask_color": (colors, {"default": "red"}),
                "pass_through": ("BOOLEAN", {"default": False}),
             },
            "optional": {
                "image": ("IMAGE",),
                "mask": ("MASK",),                
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("composite",)
    FUNCTION = "execute"
    CATEGORY = "UniversalToolkit"
    DESCRIPTION = """
Preview an image or a mask, when both inputs are used  
composites the mask on top of the image.
with pass_through on the preview is disabled and the  
composite is returned from the composite slot instead,  
this allows for the preview to be passed for video combine  
nodes for example.
"""

    def execute(self, mask_opacity, mask_color, pass_through, filename_prefix="ComfyUI", image=None, mask=None, prompt=None, extra_pnginfo=None):
        if mask is not None and image is None:
            preview = mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3)
        elif mask is None and image is not None:
            preview = image
        elif mask is not None and image is not None:
            mask_adjusted = mask * mask_opacity
            mask_image = mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3).clone()

            color_map = {
                "red": [255, 0, 0], "green": [0, 255, 0], "blue": [0, 0, 255],
                "yellow": [255, 255, 0], "cyan": [0, 255, 255], "magenta": [255, 0, 255],
                "white": [255, 255, 255], "black": [0, 0, 0]
            }
            color_list = color_map.get(mask_color, [255, 0, 0])
            
            mask_image[:, :, :, 0] = color_list[0] / 255 # Red channel
            mask_image[:, :, :, 1] = color_list[1] / 255 # Green channel
            mask_image[:, :, :, 2] = color_list[2] / 255 # Blue channel
            
            preview, = ImageCompositeMasked.composite(self, image, mask_image, 0, 0, True, mask_adjusted)
        if pass_through:
            return (preview, )
        return(self.save_images(preview, filename_prefix, prompt, extra_pnginfo)) 