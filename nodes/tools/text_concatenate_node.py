"""
Text Concatenate Node (UTK)
~~~~~~~~~~~~~~~~~~~~~~~~~~

拼接多个字符串，可自定义分隔符和空白处理。

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""


class TextConcatenate_UTK:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "delimiter": ("STRING", {"default": ", "}),
                "clean_whitespace": (["true", "false"], {}),
            },
            "optional": {
                "text_a": ("STRING", {"forceInput": True}),
                "text_b": ("STRING", {"forceInput": True}),
                "text_c": ("STRING", {"forceInput": True}),
                "text_d": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "text_concatenate"
    CATEGORY = "UniversalToolkit/Text"
    DESCRIPTION = "拼接多个字符串，可自定义分隔符和空白处理。"

    def text_concatenate(self, delimiter, clean_whitespace, **kwargs):
        text_inputs = []
        # 处理特殊分隔符\n
        if delimiter in ("\n", "\\n"):
            delimiter = "\n"
        # 按输入名排序拼接
        for k in sorted(kwargs.keys()):
            v = kwargs[k]
            if isinstance(v, str):
                if clean_whitespace == "true":
                    v = v.strip()
                if v != "":
                    text_inputs.append(v)
        merged_text = delimiter.join(text_inputs)
        return (merged_text,)


NODE_CLASS_MAPPINGS = {
    "TextConcatenate_UTK": TextConcatenate_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextConcatenate_UTK": "Text Concatenate (UTK)",
}
