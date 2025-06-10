import torch
import numpy as np
import re
import math

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
                "direction": (["right", "left", "up", "down", "auto"], {"default": "auto"}),
                "align": (["start", "center", "end"], {"default": "center"}),
                "spacing": ("INT", {"default": 0, "min": 0, "max": 1024, "step": 1}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "concatenate"
    
    def concatenate(self, image1, image2, direction, align, spacing):
        # 获取图像尺寸
        b1, c1, h1, w1 = image1.shape
        b2, c2, h2, w2 = image2.shape
        
        # 确保通道数相同
        if c1 != c2:
            raise ValueError("输入图像的通道数必须相同")
        
        # 如果是自动模式，根据图像尺寸决定拼接方向
        if direction == "auto":
            # 计算水平拼接和垂直拼接后的宽高比
            horizontal_ratio = (w1 + w2 + spacing) / max(h1, h2)
            vertical_ratio = max(w1, w2) / (h1 + h2 + spacing)
            
            # 选择更接近1:1比例的拼接方式
            direction = "right" if abs(horizontal_ratio - 1) <= abs(vertical_ratio - 1) else "down"
        
        # 计算输出尺寸
        if direction in ["right", "left"]:
            out_h = max(h1, h2)
            out_w = w1 + w2 + spacing
        else:  # up, down
            out_h = h1 + h2 + spacing
            out_w = max(w1, w2)
        
        # 创建输出张量
        output = torch.zeros((b1, c1, out_h, out_w), dtype=image1.dtype, device=image1.device)
        
        # 计算对齐位置
        if direction in ["right", "left"]:
            if align == "start":
                y1 = y2 = 0
            elif align == "center":
                y1 = (out_h - h1) // 2
                y2 = (out_h - h2) // 2
            else:  # end
                y1 = out_h - h1
                y2 = out_h - h2
            
            if direction == "right":
                x1 = 0
                x2 = w1 + spacing
            else:  # left
                x1 = w2 + spacing
                x2 = 0
        else:  # up, down
            if align == "start":
                x1 = x2 = 0
            elif align == "center":
                x1 = (out_w - w1) // 2
                x2 = (out_w - w2) // 2
            else:  # end
                x1 = out_w - w1
                x2 = out_w - w2
            
            if direction == "down":
                y1 = 0
                y2 = h1 + spacing
            else:  # up
                y1 = h2 + spacing
                y2 = 0
        
        # 复制图像数据
        output[:, :, y1:y1+h1, x1:x1+w1] = image1
        output[:, :, y2:y2+h2, x2:x2+w2] = image2
        
        return (output,)

class ImageConcatenateMulti_UTK:
    CATEGORY = "UniversalToolkit"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "direction": (["horizontal", "vertical"], {"default": "horizontal"}),
                "align": (["start", "center", "end"], {"default": "center"}),
                "spacing": ("INT", {"default": 0, "min": 0, "max": 1024, "step": 1}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "concatenate_multi"
    
    def concatenate_multi(self, images, direction, align, spacing):
        if len(images.shape) != 4:
            raise ValueError("输入必须是4D张量 [batch, channels, height, width]")
        
        b, c, h, w = images.shape
        
        # 计算输出尺寸
        if direction == "horizontal":
            out_h = h
            out_w = w * b + spacing * (b - 1)
        else:  # vertical
            out_h = h * b + spacing * (b - 1)
            out_w = w
        
        # 创建输出张量
        output = torch.zeros((1, c, out_h, out_w), dtype=images.dtype, device=images.device)
        
        # 复制图像数据
        for i in range(b):
            if direction == "horizontal":
                if align == "start":
                    y = 0
                elif align == "center":
                    y = (out_h - h) // 2
                else:  # end
                    y = out_h - h
                x = i * (w + spacing)
            else:  # vertical
                if align == "start":
                    x = 0
                elif align == "center":
                    x = (out_w - w) // 2
                else:  # end
                    x = out_w - w
                y = i * (h + spacing)
            
            output[0, :, y:y+h, x:x+w] = images[i]
        
        return (output,) 