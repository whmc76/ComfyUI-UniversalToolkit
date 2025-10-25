"""
API图像生成器节点
~~~~~~~~~~~~~~~~

通用API图像生成服务节点，支持多种运营商API接口。
提供统一的接口来调用不同的图像生成API服务。

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import json
import base64
import io
import requests
from PIL import Image
import numpy as np

# 条件导入torch，避免在没有torch的环境中导入失败
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    # 创建一个简单的torch替代类
    class MockTorch:
        @staticmethod
        def from_numpy(array):
            return array
        
        @staticmethod
        def permute(tensor, *dims):
            return tensor
            
        @staticmethod
        def unsqueeze(tensor, dim):
            return tensor
    
    torch = MockTorch()


class APIImageGenerator_UTK:
    """
    通用API图像生成器节点
    
    支持多种运营商API接口，提供统一的图像生成服务。
    包含运营商选择、API密钥管理、参数配置等功能。
    """
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "provider": (["placeholder", "jimeng4"], {
                    "tooltip": "选择API运营商",
                    "default": "placeholder"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "API密钥"
                }),
                "prompt": ("STRING", {
                    "default": "Generate a beautiful image",
                    "multiline": True,
                    "tooltip": "图像生成提示词"
                }),
                "negative_prompt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "负面提示词"
                }),
                "width": ("INT", {
                    "default": 1024,
                    "min": 256,
                    "max": 2048,
                    "step": 64,
                    "tooltip": "生成图像宽度"
                }),
                "height": ("INT", {
                    "default": 1024,
                    "min": 256,
                    "max": 2048,
                    "step": 64,
                    "tooltip": "生成图像高度"
                }),
                "steps": ("INT", {
                    "default": 20,
                    "min": 1,
                    "max": 100,
                    "tooltip": "生成步数"
                }),
                "cfg_scale": ("FLOAT", {
                    "default": 7.0,
                    "min": 1.0,
                    "max": 20.0,
                    "step": 0.1,
                    "tooltip": "CFG引导强度"
                }),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 2147483647,
                    "tooltip": "随机种子(-1为随机)"
                }),
                "scheduler": (["DDIM", "DDPM", "DPM++ 2M", "DPM++ 2M Karras", "DPM++ SDE", "DPM++ SDE Karras"], {
                    "default": "DDIM",
                    "tooltip": "调度器类型"
                }),
                "model": (["placeholder", "jimeng4-general", "jimeng4-portrait"], {
                    "default": "placeholder",
                    "tooltip": "选择模型(即梦4.0: general=通用模型, portrait=人像模型)"
                }),
            },
            "optional": {
                "image": ("IMAGE", {
                    "tooltip": "输入图像(仅图生图或编辑模型时需要)"
                }),
                "controlnet_image": ("IMAGE", {
                    "tooltip": "ControlNet输入图像(可选)"
                }),
                "controlnet_type": (["none", "canny", "depth", "pose", "openpose"], {
                    "default": "none",
                    "tooltip": "ControlNet类型"
                }),
                "controlnet_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "ControlNet强度"
                }),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "api_url")
    FUNCTION = "generate_image"
    CATEGORY = "UniversalToolkit/Tools"
    
    DESCRIPTION = """
    通用API图像生成器节点，支持多种运营商API接口。

    功能特性:
    - **多运营商支持**: 支持多种API服务提供商
    - **即梦4.0集成**: 已集成火山引擎即梦4.0图像生成API
    - **统一接口**: 提供标准化的参数配置
    - **灵活配置**: 支持完整的生成参数调整
    - **可选图像输入**: 支持文生图和图生图两种模式
    - **ControlNet支持**: 可选的控制网络输入
    - **URL输出**: 返回API调用地址用于调试

    支持的运营商:
    - **即梦4.0**: 火山引擎图像生成服务，支持通用和人像模型
    - **占位符**: 用于测试和演示的模拟API

    使用说明:
    1. 选择API运营商并填入对应的API密钥
    2. 输入生成提示词和参数
    3. 可选连接输入图像(仅图生图或编辑模型时需要)
    4. 可选添加ControlNet控制图像
    5. 执行生成获取结果图像和API调用地址

    注意事项:
    - 请确保API密钥有效且有足够额度
    - 即梦4.0需要有效的火山引擎API密钥
    - 不同运营商的参数范围可能不同
    - 生成时间取决于API服务商的响应速度
    - 输入图像仅在需要图生图或编辑功能时连接
    """

    def generate_image(self, provider, api_key, prompt, negative_prompt, 
                      width, height, steps, cfg_scale, seed, scheduler, model,
                      image=None, controlnet_image=None, controlnet_type="none", controlnet_strength=1.0):
        """
        执行API图像生成
        
        Args:
            provider: API运营商
            api_key: API密钥
            prompt: 生成提示词
            negative_prompt: 负面提示词
            width: 图像宽度
            height: 图像高度
            steps: 生成步数
            cfg_scale: CFG引导强度
            seed: 随机种子
            scheduler: 调度器类型
            model: 模型选择
            image: 输入图像(可选，仅图生图或编辑模型时需要)
            controlnet_image: ControlNet输入图像
            controlnet_type: ControlNet类型
            controlnet_strength: ControlNet强度
            
        Returns:
            Tuple[torch.Tensor, str]: 生成的图像和API调用URL
        """
        
        try:
            # 转换输入图像为PIL格式（如果提供了图像）
            input_image = None
            if image is not None:
                if isinstance(image, torch.Tensor):
                    # 处理批次图像，取第一张
                    if image.dim() == 4:
                        image = image[0]
                    
                    # 转换为numpy数组
                    if image.shape[0] == 3:  # CHW格式
                        image_np = image.permute(1, 2, 0).cpu().numpy()
                    else:  # HWC格式
                        image_np = image.cpu().numpy()
                    
                    # 归一化到0-255范围
                    if image_np.max() <= 1.0:
                        image_np = (image_np * 255).astype(np.uint8)
                    else:
                        image_np = image_np.astype(np.uint8)
                    
                    input_image = Image.fromarray(image_np)
                else:
                    input_image = image
            
            # 根据运营商调用不同的API
            if provider == "placeholder":
                # 占位符实现
                result_image, api_url = self._placeholder_api(
                    input_image, prompt, negative_prompt, width, height, 
                    steps, cfg_scale, seed, scheduler, model,
                    controlnet_image, controlnet_type, controlnet_strength
                )
            elif provider == "jimeng4":
                # 即梦4.0 API调用
                result_image, api_url = self._call_jimeng4_api(
                    api_key, input_image, prompt, negative_prompt,
                    width, height, steps, cfg_scale, seed, scheduler, model,
                    controlnet_image, controlnet_type, controlnet_strength
                )
            else:
                # 其他运营商API调用
                result_image, api_url = self._call_api(
                    provider, api_key, input_image, prompt, negative_prompt,
                    width, height, steps, cfg_scale, seed, scheduler, model,
                    controlnet_image, controlnet_type, controlnet_strength
                )
            
            # 转换结果为ComfyUI格式
            if isinstance(result_image, Image.Image):
                # 转换为RGB模式
                if result_image.mode != 'RGB':
                    result_image = result_image.convert('RGB')
                
                # 转换为numpy数组
                result_np = np.array(result_image).astype(np.float32) / 255.0
                
                # 转换为torch tensor (HWC -> CHW)
                result_tensor = torch.from_numpy(result_np).permute(2, 0, 1)
                
                # 添加批次维度
                result_tensor = result_tensor.unsqueeze(0)
            else:
                result_tensor = result_image
            
            return (result_tensor, api_url)
            
        except Exception as e:
            print(f"API图像生成错误: {str(e)}")
            # 返回原图像作为fallback
            if isinstance(image, torch.Tensor):
                return (image, f"错误: {str(e)}")
            else:
                # 转换PIL图像为tensor
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                result_np = np.array(image).astype(np.float32) / 255.0
                result_tensor = torch.from_numpy(result_np).permute(2, 0, 1).unsqueeze(0)
                return (result_tensor, f"错误: {str(e)}")

    def _placeholder_api(self, input_image, prompt, negative_prompt, width, height,
                        steps, cfg_scale, seed, scheduler, model,
                        controlnet_image=None, controlnet_type="none", controlnet_strength=1.0):
        """
        占位符API实现，用于测试和演示
        """
        if input_image is not None:
            # 如果有输入图像，调整尺寸
            result_image = input_image.resize((width, height), Image.Resampling.LANCZOS)
        else:
            # 如果没有输入图像，生成一个简单的彩色图像作为占位符
            result_image = Image.new('RGB', (width, height), color=(128, 128, 128))
        
        # 构造API URL（模拟）
        api_url = f"https://api.placeholder.com/v1/images/generations"
        
        return result_image, api_url

    def _call_jimeng4_api(self, api_key, input_image, prompt, negative_prompt,
                         width, height, steps, cfg_scale, seed, scheduler, model,
                         controlnet_image=None, controlnet_type="none", controlnet_strength=1.0):
        """
        调用即梦4.0 API服务
        
        基于火山引擎即梦4.0图像生成API文档实现
        """
        try:
            # 即梦4.0 API端点
            api_url = "https://ark.cn-beijing.volces.com/api/v3/seedream-4.0"
            
            # 构造请求数据
            request_data = {
                "prompt": prompt,
                "size": f"{width}x{height}",
                "response_format": "url",
                "model": model,
                "n": 1,  # 生成图像数量
            }
            
            # 添加负面提示词
            if negative_prompt:
                request_data["negative_prompt"] = negative_prompt
            
            # 添加随机种子
            if seed != -1:
                request_data["seed"] = seed
            
            # 添加CFG引导强度
            if cfg_scale != 7.0:
                request_data["guidance_scale"] = cfg_scale
            
            # 添加步数
            if steps != 20:
                request_data["num_inference_steps"] = steps
            
            # 如果有输入图像，处理图生图
            if input_image is not None:
                # 将图像转换为base64
                buffer = io.BytesIO()
                input_image.save(buffer, format='PNG')
                image_base64 = base64.b64encode(buffer.getvalue()).decode()
                request_data["image"] = image_base64
                request_data["strength"] = 0.8  # 默认强度
            
            # 请求头
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # 发送请求
            print(f"调用即梦4.0 API: {api_url}")
            print(f"请求数据: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
            
            response = requests.post(api_url, headers=headers, json=request_data, timeout=60)
            
            if response.status_code == 200:
                result_data = response.json()
                
                # 获取生成的图像URL
                if "data" in result_data and len(result_data["data"]) > 0:
                    image_url = result_data["data"][0]["url"]
                    
                    # 下载图像
                    image_response = requests.get(image_url, timeout=30)
                    if image_response.status_code == 200:
                        image_bytes = io.BytesIO(image_response.content)
                        result_image = Image.open(image_bytes)
                        result_image = result_image.convert('RGB')
                        
                        return result_image, api_url
                    else:
                        raise Exception(f"下载图像失败: {image_response.status_code}")
                else:
                    raise Exception("API响应中未找到图像数据")
            else:
                error_msg = f"API调用失败: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg += f" - {error_data['error']}"
                except:
                    error_msg += f" - {response.text}"
                raise Exception(error_msg)
                
        except Exception as e:
            print(f"即梦4.0 API调用错误: {str(e)}")
            # 返回占位符图像
            if input_image is not None:
                result_image = input_image
            else:
                result_image = Image.new('RGB', (width, height), color=(128, 128, 128))
            return result_image, f"错误: {str(e)}"

    def _call_api(self, provider, api_key, input_image, prompt, negative_prompt,
                  width, height, steps, cfg_scale, seed, scheduler, model,
                  controlnet_image=None, controlnet_type="none", controlnet_strength=1.0):
        """
        调用实际的API服务
        
        这里可以根据不同的provider实现不同的API调用逻辑
        后续添加具体API时会扩展此方法
        """
        
        # 构造API请求数据
        api_data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "seed": seed if seed != -1 else None,
            "scheduler": scheduler,
            "model": model,
        }
        
        # 如果提供了输入图像，转换为base64编码
        if input_image is not None:
            buffer = io.BytesIO()
            input_image.save(buffer, format='PNG')
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            api_data["input_image"] = image_base64
        
        # 添加ControlNet参数
        if controlnet_image is not None and controlnet_type != "none":
            # 处理ControlNet图像
            if isinstance(controlnet_image, torch.Tensor):
                if controlnet_image.dim() == 4:
                    controlnet_image = controlnet_image[0]
                
                if controlnet_image.shape[0] == 3:
                    controlnet_np = controlnet_image.permute(1, 2, 0).cpu().numpy()
                else:
                    controlnet_np = controlnet_image.cpu().numpy()
                
                if controlnet_np.max() <= 1.0:
                    controlnet_np = (controlnet_np * 255).astype(np.uint8)
                else:
                    controlnet_np = controlnet_np.astype(np.uint8)
                
                controlnet_pil = Image.fromarray(controlnet_np)
            else:
                controlnet_pil = controlnet_image
            
            # 转换为base64
            controlnet_buffer = io.BytesIO()
            controlnet_pil.save(controlnet_buffer, format='PNG')
            controlnet_base64 = base64.b64encode(controlnet_buffer.getvalue()).decode()
            
            api_data.update({
                "controlnet_type": controlnet_type,
                "controlnet_strength": controlnet_strength,
                "controlnet_image": controlnet_base64,
            })
        
        # 构造API URL
        api_url = f"https://api.{provider}.com/v1/images/generations"
        
        # 这里应该发送实际的HTTP请求
        # 目前返回占位符图像
        print(f"模拟调用API: {provider}")
        print(f"API数据: {json.dumps(api_data, indent=2, ensure_ascii=False)}")
        
        # 生成占位符图像
        if input_image is not None:
            result_image = input_image
        else:
            result_image = Image.new('RGB', (width, height), color=(128, 128, 128))
        
        return result_image, api_url


# 节点注册
NODE_CLASS_MAPPINGS = {
    "APIImageGenerator_UTK": APIImageGenerator_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APIImageGenerator_UTK": "API Image Generator (UTK)",
}
