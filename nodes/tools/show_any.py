"""
Show Any Node for ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Display any type of input data in a text field, showing data type and content.
Acts as a passthrough node for debugging and inspection.

Based on comfyui-easy-use's showAnything node implementation.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import json
import torch
import numpy as np
from typing import Any, List

# Import AnyType for accepting any input type
try:
    from comfy.comfy_types.node_typing import IO
    ANY_TYPE = IO.ANY
except ImportError:
    try:
        from comfy_extras.nodes_custom_sampler import AnyType
        ANY_TYPE = AnyType("*")
    except ImportError:
        from .any_type import AnyType
        ANY_TYPE = AnyType("*")


class ShowAny_UTK:
    """
    显示任意类型数据的节点
    
    功能：
    - 接受任何类型的输入数据
    - 在文本框中显示数据类型和数据内容
    - 直接输出输入的数据（不做任何修改）
    - 用于调试和查看数据流
    
    参考实现：comfyui-easy-use 的 showAnything 节点
    """
    
    CATEGORY = "UniversalToolkit/Tools"
    RETURN_TYPES = (ANY_TYPE,)
    RETURN_NAMES = ("data",)
    FUNCTION = "show_any"
    INPUT_IS_LIST = True
    OUTPUT_NODE = True
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "data": (ANY_TYPE, {
                    "tooltip": "输入任意类型的数据"
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }
    
    def format_data(self, data: Any) -> str:
        """
        格式化数据为可读的字符串
        
        Args:
            data: 要格式化的数据
            
        Returns:
            格式化后的字符串
        """
        # 获取数据类型
        data_type = type(data).__name__
        
        # 根据不同类型格式化数据
        if data is None:
            return f"Type: NoneType\nValue: None"
        
        elif isinstance(data, str):
            return f"Type: string\nValue: {data}"
        
        elif isinstance(data, (int, float)):
            return f"Type: {data_type}\nValue: {data}"
        
        elif isinstance(data, bool):
            return f"Type: boolean\nValue: {data}"
        
        elif isinstance(data, (list, tuple)):
            # 列表或元组
            try:
                # 尝试转换为JSON格式
                json_str = json.dumps(data, ensure_ascii=False, indent=2)
                return f"Type: {data_type}\nLength: {len(data)}\nValue:\n{json_str}"
            except (TypeError, ValueError):
                # 如果无法序列化为JSON，显示repr
                return f"Type: {data_type}\nLength: {len(data)}\nValue: {repr(data)}"
        
        elif isinstance(data, dict):
            # 字典
            try:
                json_str = json.dumps(data, ensure_ascii=False, indent=2)
                return f"Type: dict\nKeys: {len(data)}\nValue:\n{json_str}"
            except (TypeError, ValueError):
                return f"Type: dict\nKeys: {len(data)}\nValue: {repr(data)}"
        
        elif isinstance(data, torch.Tensor):
            # PyTorch Tensor
            shape = list(data.shape)
            dtype = str(data.dtype)
            device = str(data.device)
            min_val = float(data.min().item()) if data.numel() > 0 else None
            max_val = float(data.max().item()) if data.numel() > 0 else None
            
            info = f"Type: torch.Tensor\nShape: {shape}\nDtype: {dtype}\nDevice: {device}"
            if min_val is not None and max_val is not None:
                info += f"\nMin: {min_val:.6f}\nMax: {max_val:.6f}"
            info += f"\nNumel: {data.numel()}"
            
            return info
        
        elif isinstance(data, np.ndarray):
            # NumPy Array
            shape = data.shape
            dtype = str(data.dtype)
            min_val = float(data.min()) if data.size > 0 else None
            max_val = float(data.max()) if data.size > 0 else None
            
            info = f"Type: numpy.ndarray\nShape: {shape}\nDtype: {dtype}"
            if min_val is not None and max_val is not None:
                info += f"\nMin: {min_val:.6f}\nMax: {max_val:.6f}"
            info += f"\nSize: {data.size}"
            
            return info
        
        else:
            # 其他类型，尝试使用repr
            try:
                repr_str = repr(data)
                # 限制长度，避免过长
                if len(repr_str) > 500:
                    repr_str = repr_str[:500] + "..."
                return f"Type: {data_type}\nValue: {repr_str}"
            except Exception:
                return f"Type: {data_type}\nValue: <无法显示>"
    
    def show_any(self, unique_id=None, extra_pnginfo=None, **kwargs) -> dict:
        """
        显示任意类型的数据
        
        Args:
            unique_id: 节点的唯一ID（用于保存工作流）
            extra_pnginfo: 额外的PNG信息（用于保存工作流）
            **kwargs: 输入的数据（任意类型）
            
        Returns:
            dict: 包含ui显示和结果的字典
        """
        values = []
        if "data" in kwargs:
            for val in kwargs['data']:
                try:
                    if isinstance(val, str):
                        values.append(val)
                    elif isinstance(val, list):
                        values = val
                    elif isinstance(val, (int, float, bool)):
                        values.append(str(val))
                    elif isinstance(val, torch.Tensor):
                        # 处理torch.Tensor（IMAGE类型）
                        shape = list(val.shape)
                        values.append(f"torch.Tensor(shape={shape}, dtype={val.dtype})")
                    else:
                        val = json.dumps(val)
                        values.append(str(val))
                except Exception:
                    values.append(str(val))
                    pass
        
        # 保存到工作流中（用于加载工作流时恢复显示）
        if not extra_pnginfo:
            pass
        elif not isinstance(extra_pnginfo, list) or len(extra_pnginfo) == 0:
            pass
        elif (not isinstance(extra_pnginfo[0], dict) or "workflow" not in extra_pnginfo[0]):
            pass
        else:
            workflow = extra_pnginfo[0]["workflow"]
            if unique_id and isinstance(unique_id, list) and len(unique_id) > 0:
                node = next((x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])), None)
                if node:
                    node["widgets_values"] = [values]
        
        # 返回结果（完全按照comfyui-easy-use格式）
        if isinstance(values, list) and len(values) == 1:
            return {"ui": {"text": values}, "result": (values[0],)}
        else:
            return {"ui": {"text": values}, "result": (values,)}


# 节点映射
NODE_CLASS_MAPPINGS = {
    "ShowAny_UTK": ShowAny_UTK
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShowAny_UTK": "Show Any (UTK)"
}
