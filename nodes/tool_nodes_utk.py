import torch
import numpy as np
import cv2
from scipy.ndimage import binary_erosion, gaussian_filter

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

# mask二值化，阈值0.5
def mask_floor(mask):
    return (mask > 0.5).astype(np.float32)

# 腐蚀操作，kernel为feathering
def mask_erosion(mask, feathering):
    if feathering > 0:
        structure = np.ones((feathering, feathering), dtype=np.uint8)
        return binary_erosion(mask, structure=structure).astype(np.float32)
    return mask

# 高斯模糊，sigma=feathering/3
def mask_blur(mask, feathering):
    if feathering > 0:
        sigma = feathering / 3.0
        return gaussian_filter(mask, sigma=sigma)
    return mask

class FillMaskedArea_UTK:
    CATEGORY = "UniversalToolkit"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "fill_mode": (["neutral", "telea", "navier-stokes"], {"default": "neutral"}),
                "feathering": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1, "label": "Feathering (羽化/边缘过渡)"}),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "fill_masked"
    IS_PREVIEW = True

    def fill_masked(self, image, mask, fill_mode, feathering):
        # 支持batch
        if isinstance(image, torch.Tensor):
            if image.dim() == 4:
                batch_size = image.shape[0]
                results = []
                for i in range(batch_size):
                    img_np = image[i].cpu().numpy()
                    mask_np = mask[i].cpu().numpy() if mask.dim() == 4 else mask.cpu().numpy()
                    result = self._fill_single_image(img_np, mask_np, fill_mode, feathering)
                    results.append(result)
                return (torch.from_numpy(np.stack(results)).float(),)
            else:
                img_np = image.cpu().numpy()
                mask_np = mask.cpu().numpy()
                result = self._fill_single_image(img_np, mask_np, fill_mode, feathering)
                return (torch.from_numpy(result).unsqueeze(0).float(),)
        else:
            result = self._fill_single_image(image, mask, fill_mode, feathering)
            return (torch.from_numpy(result).unsqueeze(0).float(),)

    def _fill_single_image(self, image, mask, fill_mode, feathering):
        # [C,H,W] -> [H,W,C]
        if image.shape[0] <= 4:
            image = np.transpose(image, (1, 2, 0))
        if mask.ndim == 3 and mask.shape[0] == 1:
            mask = mask[0]
        elif mask.ndim == 3 and mask.shape[2] == 1:
            mask = mask[:, :, 0]
        # 归一化到0-1
        if mask.max() > 1.0:
            mask = mask / 255.0
        # 1. mask二值化
        mask_bin = mask_floor(mask)
        # 2. 腐蚀+高斯羽化
        if feathering > 0:
            mask_eroded = mask_erosion(mask_bin, feathering)
            mask_feathered = mask_blur(mask_eroded, feathering)
        else:
            mask_feathered = mask_bin
        alpha = np.clip(mask_feathered, 0, 1)
        # 3. neutral模式
        if fill_mode == "neutral":
            result = image.astype(np.float32) / 255.0 if image.dtype != np.float32 else image.copy()
            gray = np.ones_like(result) * 0.5
            out = result * (1 - alpha[..., None]) + gray * alpha[..., None]
            return np.clip(out, 0, 1)
        # 4. inpaint模式
        if image.dtype != np.uint8:
            img_uint8 = (image * 255).astype(np.uint8) if image.max() <= 1.0 else image.astype(np.uint8)
        else:
            img_uint8 = image.copy()
        mask_uint8 = (alpha > 0.5).astype(np.uint8)
        method = cv2.INPAINT_TELEA if fill_mode == "telea" else cv2.INPAINT_NS
        if img_uint8.shape[2] == 3:
            img_bgr = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2BGR)
            filled = cv2.inpaint(img_bgr, mask_uint8, 3, method)
            filled = cv2.cvtColor(filled, cv2.COLOR_BGR2RGB)
        else:
            filled = cv2.inpaint(img_uint8, mask_uint8, 3, method)
        filled = filled.astype(np.float32) / 255.0
        result = image.astype(np.float32) / 255.0 if image.dtype != np.float32 else image.copy()
        out = result * (1 - alpha[..., None]) + filled * alpha[..., None]
        return np.clip(out, 0, 1)

class ImageAndMaskPreview_UTK:
    pass # This class is now implemented in image_nodes_utk.py 