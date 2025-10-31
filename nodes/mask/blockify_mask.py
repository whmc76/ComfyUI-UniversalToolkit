import torch
import torch.nn.functional as F


class BlockifyMask_UTK:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "masks": ("MASK",),
                "block_size": ("INT", {"default": 16, "min": 1, "max": 4096, "step": 1}),
                "device": (["cpu", "cuda"], {"default": "cpu"}),
            },
            "optional": {
                # 可选二值化
                "binarize": ("BOOLEAN", {"default": True}),
                "threshold": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "blockify"
    CATEGORY = "UniversalToolkit/Mask"
    DESCRIPTION = "将连续掩码按 block_size 进行像素块化（马赛克化），可选二值化。"

    def blockify(self, masks: torch.Tensor, block_size: int, device: str, binarize: bool = True, threshold: float = 0.5):
        mask_tensor = masks
        if block_size <= 1:
            out = torch.clamp(mask_tensor, 0.0, 1.0)
            return (out,)

        # 选择设备（多数情况下 CPU 足够；如选 cuda 则尝试放到 GPU）
        use_cuda = device == "cuda" and torch.cuda.is_available()
        x_in = mask_tensor
        if use_cuda:
            x_in = x_in.to("cuda")

        # BxHxW -> Bx1xHxW for pooling
        x = x_in.unsqueeze(1).contiguous()

        # 平均池化到较小网格；ceil 对齐，边缘使用对称填充避免尺寸不整除
        pooled = F.avg_pool2d(x, kernel_size=block_size, stride=block_size, ceil_mode=True)

        # 还原到原尺寸，使用最近邻形成块状
        out = F.interpolate(pooled, size=(mask_tensor.shape[1], mask_tensor.shape[2]), mode="nearest").squeeze(1)

        if binarize:
            out = (out >= threshold).float()

        out = torch.clamp(out, 0.0, 1.0)
        if use_cuda:
            out = out.to("cpu")
        return (out,)


NODE_CLASS_MAPPINGS = {"BlockifyMask_UTK": BlockifyMask_UTK}
NODE_DISPLAY_NAME_MAPPINGS = {"BlockifyMask_UTK": "Blockify Mask (UTK)"}


