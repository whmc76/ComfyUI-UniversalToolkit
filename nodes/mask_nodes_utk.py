import torch

class MaskAnd_UTK:
    CATEGORY = "UniversalToolkit/Mask"
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"mask1": ("MASK",), "mask2": ("MASK",)}}
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "and_mask"
    def and_mask(self, mask1, mask2):
        # 逐像素与操作，支持batch
        if mask1.shape != mask2.shape:
            raise ValueError("输入的两个MASK尺寸不一致")
        return (mask1 * mask2,)

class MaskSub_UTK:
    CATEGORY = "UniversalToolkit/Mask"
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"mask1": ("MASK",), "mask2": ("MASK",)}}
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "sub_mask"
    def sub_mask(self, mask1, mask2):
        # 逐像素减法，支持batch，结果裁剪到[0,1]
        if mask1.shape != mask2.shape:
            raise ValueError("输入的两个MASK尺寸不一致")
        return (torch.clamp(mask1 - mask2, 0, 1),)

class MaskAdd_UTK:
    CATEGORY = "UniversalToolkit/Mask"
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"mask1": ("MASK",), "mask2": ("MASK",)}}
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "add_mask"
    def add_mask(self, mask1, mask2):
        # 逐像素加法，支持batch，结果裁剪到[0,1]
        if mask1.shape != mask2.shape:
            raise ValueError("输入的两个MASK尺寸不一致")
        return (torch.clamp(mask1 + mask2, 0, 1),) 