"""
Image Converters for UniversalToolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Image format conversion utilities for UniversalToolkit.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import cv2
import numpy as np
import torch
from PIL import Image


def tensor2pil(image):
    """将torch张量转换为PIL图像"""
    if image.dim() == 4:
        image = image.squeeze(0)
    if image.dim() == 3:
        if image.shape[0] == 1:  # 灰度图
            image = image.squeeze(0)
            image = (image * 255).clamp(0, 255).to(torch.uint8)
            return Image.fromarray(image.cpu().numpy(), mode="L")
        else:  # RGB图
            image = image.permute(1, 2, 0)
            image = (image * 255).clamp(0, 255).to(torch.uint8)
            return Image.fromarray(image.cpu().numpy(), mode="RGB")
    return None


def pil2tensor(image):
    """将PIL图像转换为torch张量"""
    if image.mode == "L":
        image = image.convert("RGB")
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image)
    if image.dim() == 3:
        image = image.permute(2, 0, 1)
    return image


def image2mask(image):
    """将PIL图像转换为掩码张量"""
    if image.mode == "L":
        return torch.tensor([pil2tensor(image)[0, :, :].tolist()])
    else:
        image = image.convert("RGB").split()[0]
        return torch.tensor([pil2tensor(image)[0, :, :].tolist()])


def tensor2cv2(image: torch.Tensor) -> np.array:
    """将torch张量转换为OpenCV格式"""
    if image.dim() == 4:
        image = image.squeeze()
    npimage = image.numpy()
    cv2image = np.uint8(npimage * 255 / npimage.max())
    return cv2.cvtColor(cv2image, cv2.COLOR_RGB2BGR)


def pil2cv2(pil_img):
    """将PIL图像转换为OpenCV格式"""
    np_img_array = np.asarray(pil_img)
    return cv2.cvtColor(np_img_array, cv2.COLOR_RGB2BGR)


def cv22pil(cv2_img):
    """将OpenCV图像转换为PIL图像"""
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cv2_img)


def tensor2np(tensor):
    """将torch张量转换为numpy数组"""
    if len(tensor.shape) == 3:  # Single image
        return np.clip(255.0 * tensor.cpu().numpy(), 0, 255).astype(np.uint8)
    else:  # Batch of images
        return [
            np.clip(255.0 * t.cpu().numpy(), 0, 255).astype(np.uint8) for t in tensor
        ]
