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
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {}
    
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def get_lora_info(lora_name):
    db = load_json_from_file(db_path)
    output = None
    examplePrompt = None
    trainedWords = None
    baseModel = None

    loraInfo = db.get(lora_name, {})

    if isinstance(loraInfo, str):
        loraInfo = {}
    
    output = loraInfo.get('output', None)
    examplePrompt = loraInfo.get('examplePrompt', None)
    trainedWords = loraInfo.get('trainedWords', None)
    baseModel = loraInfo.get('baseModel', None)

    if output is None or baseModel is None:
        output = ""
        lora_path = folder_paths.get_full_path("loras", lora_name)
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

        db[lora_name] = {
            "output": output,
            "trainedWords": trainedWords,
            "examplePrompt": examplePrompt,
            "baseModel": baseModel
            }
        save_dict_to_json(db, db_path)
    
    return (output, trainedWords, examplePrompt, baseModel)


@server.PromptServer.instance.routes.post('/lora_info_utk')
async def fetch_lora_info(request):
    post = await request.post()
    lora_name = post.get("lora_name")
    (output, triggerWords, examplePrompt, baseModel) = get_lora_info(lora_name)

    return web.json_response({"output": output, "triggerWords": triggerWords, "examplePrompt": examplePrompt, "baseModel": baseModel})

class LoraInfo_UTK:
    """
    LoRA信息节点
    
    获取LoRA模型的详细信息，包括：
    - 触发词 (Trigger Words)
    - 示例提示词 (Example Prompt)
    - 基础模型 (Base Model)
    - CivitAI链接
    - 示例图片
    """
    
    @classmethod
    def INPUT_TYPES(s):
        LORA_LIST = sorted(folder_paths.get_filename_list("loras"), key=str.lower)
        return {
            "required": {
                "lora_name": (LORA_LIST, {"default": LORA_LIST[0] if LORA_LIST else ""})
            },
        }

    RETURN_NAMES = ("lora_name", "civitai_trigger", "example_prompt", "civitai_info")
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    FUNCTION = "lora_info"
    OUTPUT_NODE = True
    CATEGORY = "UniversalToolkit/Tools"

    def lora_info(self, lora_name):
        (output, triggerWords, examplePrompt, baseModel) = get_lora_info(lora_name)
        
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
            "result": (lora_name, triggerWords or "", examplePrompt or "", info_text)
        }


# Node mappings
NODE_CLASS_MAPPINGS = {
    "LoraInfo_UTK": LoraInfo_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraInfo_UTK": "Lora Info (UTK)",
} 