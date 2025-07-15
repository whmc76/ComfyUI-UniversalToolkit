"""
Lora Info Node
~~~~~~~~~~~~~

获取LoRA模型信息，包括触发词、示例提示词、基础模型等。

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import folder_paths
import hashlib
import requests
import json
import server
from aiohttp import web
import os


db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lora_info_db.json')

def load_json_from_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")
        return {}

def save_dict_to_json(data_dict, file_path):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)
            print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving JSON to file: {e}")

def get_model_version_info(hash_value):
    api_url = f"https://civitai.com/api/v1/model-versions/by-hash/{hash_value}"
    try:
        response = requests.get(api_url, timeout=10)  # 设置10秒超时
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[LoraInfo_UTK] CivitAI API返回错误状态码: {response.status_code}")
            return {}
    except requests.exceptions.ConnectionError:
        print("[LoraInfo_UTK] 无法连接到CivitAI服务器，请检查网络连接")
        return {}
    except requests.exceptions.Timeout:
        print("[LoraInfo_UTK] 连接CivitAI服务器超时，请稍后重试")
        return {}
    except requests.exceptions.RequestException as e:
        print(f"[LoraInfo_UTK] 请求CivitAI API时发生错误: {e}")
        return {}
    except Exception as e:
        print(f"[LoraInfo_UTK] 获取模型信息时发生未知错误: {e}")
        return {}

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def get_metadata(filepath):
    """从LoRA文件中提取元数据"""
    try:
        filepath = folder_paths.get_full_path("loras", filepath)
        with open(filepath, "rb") as file:
            # https://github.com/huggingface/safetensors#format
            # 8 bytes: N, an unsigned little-endian 64-bit integer, containing the size of the header
            header_size = int.from_bytes(file.read(8), "little", signed=False)

            if header_size <= 0:
                return None

            header = file.read(header_size)
            if header_size <= 0:
                return None
            header_json = json.loads(header)
            return header_json["__metadata__"] if "__metadata__" in header_json else None
    except Exception as e:
        print(f"Error reading metadata from {filepath}: {e}")
        return None

def sort_tags_by_frequency(meta_tags):
    """按训练频率排序标签"""
    if meta_tags is None:
        return []
    if "ss_tag_frequency" in meta_tags:
        meta_tags = meta_tags["ss_tag_frequency"]
        meta_tags = json.loads(meta_tags)
        sorted_tags = {}
        for _, dataset in meta_tags.items():
            for tag, count in dataset.items():
                tag = str(tag).strip()
                if tag in sorted_tags:
                    sorted_tags[tag] = sorted_tags[tag] + count
                else:
                    sorted_tags[tag] = count
        # 按训练频率排序，最常见的标签在前
        sorted_tags = dict(sorted(sorted_tags.items(), key=lambda item: item[1], reverse=True))
        return list(sorted_tags.keys())
    else:
        return []

def get_lora_info(lora_name):
    try:
        db = load_json_from_file(db_path)
        output = None
        examplePrompt = None
        trainedWords = None
        baseModel = None
        metaInfo = None

        loraInfo = db.get(lora_name, {})

        if isinstance(loraInfo, str):
            loraInfo = {}
        
        output = loraInfo.get('output', None)
        examplePrompt = loraInfo.get('examplePrompt', None)
        trainedWords = loraInfo.get('trainedWords', None)
        baseModel = loraInfo.get('baseModel', None)
        metaInfo = loraInfo.get('metaInfo', None)

        if output is None or baseModel is None:
            output = ""
            try:
                lora_path = folder_paths.get_full_path("loras", lora_name)
                if not lora_path:
                    print(f"[LoraInfo_UTK] 无法找到LoRA文件: {lora_name}")
                    return ("", "", "", "", "")
                
                LORAsha256 = calculate_sha256(lora_path)
                model_info = get_model_version_info(LORAsha256)
                
                if model_info.get("trainedWords", None) is None:
                    trainedWords = ""
                else:
                    trainedWords = ",".join(model_info.get("trainedWords"))
                baseModel = model_info.get("baseModel", "")
                images = model_info.get('images')
                examplePrompt = None
                modelID = model_info.get("modelId")
                
                if modelID:
                    output += f"URL: https://civitai.com/models/{modelID}\n"
                if trainedWords:
                    output += "Triggers: " + trainedWords
                    output += "\n"
                
                if baseModel:
                    output += f"Base Model: {baseModel}\n"
                if images:
                    output += "\nExamples:\n"
                    for image in images:
                        output += f"\nOutput: {image.get('url')}\n"
                        meta = image.get("meta")
                        if meta:
                            for key, value in meta.items():
                                if examplePrompt is None and key == "prompt":
                                    examplePrompt = value
                                output += f"{key}: {value}\n"
                        output += '\n'

                # 获取元数据信息
                try:
                    metadata = get_metadata(lora_name)
                    if metadata:
                        metaInfo = json.dumps(metadata, indent=2, ensure_ascii=False)
                    else:
                        metaInfo = ""
                except Exception as e:
                    print(f"[LoraInfo_UTK] 读取元数据时发生错误: {e}")
                    metaInfo = ""

                db[lora_name] = {
                    "output": output,
                    "trainedWords": trainedWords,
                    "examplePrompt": examplePrompt,
                    "baseModel": baseModel,
                    "metaInfo": metaInfo
                    }
                save_dict_to_json(db, db_path)
                
            except Exception as e:
                print(f"[LoraInfo_UTK] 处理LoRA文件时发生错误: {e}")
                output = f"处理LoRA文件时发生错误: {e}"
                trainedWords = ""
                examplePrompt = ""
                baseModel = ""
                metaInfo = ""
        
        return (output, trainedWords, examplePrompt, baseModel, metaInfo)
        
    except Exception as e:
        print(f"[LoraInfo_UTK] 获取LoRA信息时发生严重错误: {e}")
        return ("", "", "", "", "")


@server.PromptServer.instance.routes.post('/lora_info_utk')
async def fetch_lora_info(request):
    try:
        post = await request.post()
        lora_name = post.get("lora_name")
        
        if not lora_name:
            return web.json_response({
                "error": "未提供LoRA名称",
                "output": "",
                "triggerWords": "",
                "examplePrompt": "",
                "baseModel": "",
                "metaInfo": ""
            })
        
        (output, triggerWords, examplePrompt, baseModel, metaInfo) = get_lora_info(lora_name)

        return web.json_response({
            "output": output, 
            "triggerWords": triggerWords, 
            "examplePrompt": examplePrompt, 
            "baseModel": baseModel,
            "metaInfo": metaInfo
        })
    except Exception as e:
        print(f"[LoraInfo_UTK] Web API调用时发生错误: {e}")
        return web.json_response({
            "error": f"处理请求时发生错误: {e}",
            "output": "",
            "triggerWords": "",
            "examplePrompt": "",
            "baseModel": "",
            "metaInfo": ""
        })

class LoraInfo_UTK:
    """
    LoRA信息节点
    
    获取LoRA模型的详细信息，包括：
    - 触发词 (Trigger Words)
    - 示例提示词 (Example Prompt)
    - 基础模型 (Base Model)
    - CivitAI链接
    - 示例图片
    - 元数据信息 (Meta Info)
    """
    
    @classmethod
    def INPUT_TYPES(s):
        LORA_LIST = sorted(folder_paths.get_filename_list("loras"), key=str.lower)
        return {
            "required": {
                "lora_name": (LORA_LIST, {"default": LORA_LIST[0] if LORA_LIST else ""})
            },
        }

    RETURN_NAMES = ("lora_name", "civitai_trigger", "example_prompt", "civitai_info", "meta_info")
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    FUNCTION = "lora_info"
    OUTPUT_NODE = True
    CATEGORY = "UniversalToolkit/Tools"

    def lora_info(self, lora_name):
        try:
            (output, triggerWords, examplePrompt, baseModel, metaInfo) = get_lora_info(lora_name)
            
            # 构建信息文本
            info_text = f"LoRA: {lora_name}\n"
            if baseModel:
                info_text += f"Base Model: {baseModel}\n"
            if triggerWords:
                info_text += f"Trigger Words: {triggerWords}\n"
            if examplePrompt:
                info_text += f"Example Prompt: {examplePrompt}\n"
            if output:
                info_text += f"\n详细信息:\n{output}"
            
            return {
                "ui": {
                    "text": (info_text,), 
                    "model": (baseModel,)
                }, 
                "result": (lora_name, triggerWords or "", examplePrompt or "", info_text, metaInfo or "")
            }
        except Exception as e:
            print(f"[LoraInfo_UTK] 节点执行时发生错误: {e}")
            error_text = f"LoRA: {lora_name}\n获取信息时发生错误: {e}"
            return {
                "ui": {
                    "text": (error_text,), 
                    "model": ("",)
                }, 
                "result": (lora_name, "", "", error_text, "")
            }


# Node mappings
NODE_CLASS_MAPPINGS = {
    "LoraInfo_UTK": LoraInfo_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraInfo_UTK": "Lora Info (UTK)",
} 