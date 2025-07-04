import torch

class ThinkRemover_UTK:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING",),
            },
            "optional": {}
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("cleared_content", "think_content")
    FUNCTION = "think_remover"
    CATEGORY = "UniversalToolkit/Tools"
    DESCRIPTION = "分离文本中的<think>内容和剩余内容。"

    def think_remover(self, text):
        cleared_content = text
        think_content = text
        think_tag = '</think>'
        # 检查是否包含'</think>'
        if think_tag in text.lower():
            end_index = text.lower().index(think_tag) + len(think_tag)
            think_content = text[:end_index].strip()
            cleared_content = text[end_index:].strip()
        return (cleared_content, think_content)

NODE_CLASS_MAPPINGS = {
    "ThinkRemover_UTK": ThinkRemover_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ThinkRemover_UTK": "Think Remover (UTK)",
} 