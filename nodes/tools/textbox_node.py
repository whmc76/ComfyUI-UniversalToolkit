"""
TextBox Node (Prompt/参数传递)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

提供一个多行文本输入框，作为工作流中的文本参数节点。

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""


class TextBoxNode_UTK:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "text", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "textbox"
    CATEGORY = "UniversalToolkit/Text"
    DESCRIPTION = "提供一个多行文本输入框，作为工作流中的文本参数节点。"

    def textbox(self, text):
        return (text,)


NODE_CLASS_MAPPINGS = {
    "TextBoxNode_UTK": TextBoxNode_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextBoxNode_UTK": "TextBox (UTK)",
}
