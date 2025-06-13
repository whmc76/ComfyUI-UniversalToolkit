import torch

class Show_UTK:
    CATEGORY = "UniversalToolkit"
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"input": ("STRING", "INT", "FLOAT", "LIST", "MASK", "IMAGE", "LATENT")}}
    RETURN_TYPES = ("STRING", "INT", "FLOAT", "LIST", "MASK", "IMAGE", "LATENT")
    RETURN_NAMES = ("string", "int", "float", "list", "mask", "image", "latent")
    FUNCTION = "show"
    IS_PREVIEW = True

    def show(self, input):
        outs = [None] * 7
        if isinstance(input, str):
            outs[0] = input
        elif isinstance(input, int):
            outs[1] = input
        elif isinstance(input, float):
            outs[2] = input
        elif isinstance(input, list):
            outs[3] = input
        elif hasattr(input, "shape") and len(input.shape) == 4 and input.shape[1] == 1:
            outs[4] = input  # MASK
        elif hasattr(input, "shape") and len(input.shape) == 4 and input.shape[1] == 3:
            outs[5] = input  # IMAGE
        elif isinstance(input, dict) and "samples" in input:
            outs[6] = input  # LATENT
        return tuple(outs)

class ShowInt_UTK:
    CATEGORY = "UniversalToolkit"
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"int_val": ("INT",)}}
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int_val",)
    FUNCTION = "show"
    IS_PREVIEW = True
    def show(self, int_val=None):
        if int_val is None:
            int_val = 0
        return (int_val,)

class ShowFloat_UTK:
    CATEGORY = "UniversalToolkit"
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"float_val": ("FLOAT",)}}
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float_val",)
    FUNCTION = "show"
    IS_PREVIEW = True
    def show(self, float_val=None):
        if float_val is None:
            float_val = 0.0
        return (float_val,)

class ShowList_UTK:
    CATEGORY = "UniversalToolkit"
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"list_val": ("LIST",)}}
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("list_val",)
    FUNCTION = "show"
    IS_PREVIEW = True
    def show(self, list_val=None):
        if list_val is None:
            list_val = []
        return (list_val,)

class ShowText_UTK:
    CATEGORY = "UniversalToolkit"
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"text": ("STRING",)}}
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "show"
    IS_PREVIEW = True
    def show(self, text=None):
        if text is None:
            text = ""
        return (text,)

class PreviewMask_UTK:
    CATEGORY = "UniversalToolkit"
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"mask": ("MASK",)}}
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "show"
    IS_PREVIEW = True
    def show(self, mask=None):
        if mask is None:
            mask = torch.zeros([1, 1, 64, 64], dtype=torch.float32)
        return (mask,) 