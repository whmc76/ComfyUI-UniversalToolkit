"""
Image Utilities for UniversalToolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Image processing utility functions for UniversalToolkit nodes.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import numpy as np
import torch
from PIL import Image


def tensor2pil(t_image: torch.Tensor) -> Image:
    """将 PyTorch tensor 转换为 PIL Image"""
    return Image.fromarray(
        np.clip(255.0 * t_image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8)
    )


def pil2tensor(image: Image) -> torch.Tensor:
    """将 PIL Image 转换为 PyTorch tensor"""
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


def image2mask(image: Image) -> torch.Tensor:
    """将图像转换为掩码格式"""
    if image.mode == "L":
        return torch.tensor([pil2tensor(image)[0, :, :].tolist()])
    else:
        image = image.convert("RGB").split()[0]
        return torch.tensor([pil2tensor(image)[0, :, :].tolist()])


def tensor2np(tensor: torch.Tensor) -> np.ndarray:
    """将 PyTorch tensor 转换为 numpy 数组"""
    return np.clip(255.0 * tensor.cpu().numpy(), 0, 255).astype(np.uint8)


def np2tensor(np_array: np.ndarray) -> torch.Tensor:
    """将 numpy 数组转换为 PyTorch tensor"""
    return torch.from_numpy(np_array.astype(np.float32) / 255.0).unsqueeze(0)


def log(message: str, message_type: str = "info"):
    name = "LayerStyle"
    if message_type == "error":
        message = "\033[1;41m" + str(message) + "\033[m"
    elif message_type == "warning":
        message = "\033[1;31m" + str(message) + "\033[m"
    elif message_type == "finish":
        message = "\033[1;32m" + str(message) + "\033[m"
    else:
        message = "\033[1;33m" + str(message) + "\033[m"
    print(f"# 😺dzNodes: {name} -> {message}")


def num_round_up_to_multiple(number: int, multiple: int) -> int:
    return ((number + multiple - 1) // multiple) * multiple


def fit_resize_image(
    image, target_width, target_height, fit, resize_sampler, background_color="#000000"
):
    image = image.convert("RGB")
    orig_width, orig_height = image.size
    if fit == "letterbox":
        if orig_width / orig_height > target_width / target_height:
            fit_width = target_width
            fit_height = int(target_width / orig_width * orig_height)
        else:
            fit_height = target_height
            fit_width = int(target_height / orig_height * orig_width)
        fit_image = image.resize((fit_width, fit_height), resize_sampler)
        ret_image = Image.new(
            "RGB", size=(target_width, target_height), color=background_color
        )
        ret_image.paste(
            fit_image,
            box=((target_width - fit_width) // 2, (target_height - fit_height) // 2),
        )
    elif fit == "crop":
        if orig_width / orig_height > target_width / target_height:
            fit_width = int(orig_height * target_width / target_height)
            fit_image = image.crop(
                (
                    (orig_width - fit_width) // 2,
                    0,
                    (orig_width - fit_width) // 2 + fit_width,
                    orig_height,
                )
            )
        else:
            fit_height = int(orig_width * target_height / target_width)
            fit_image = image.crop(
                (
                    0,
                    (orig_height - fit_height) // 2,
                    orig_width,
                    (orig_height - fit_height) // 2 + fit_height,
                )
            )
        ret_image = fit_image.resize((target_width, target_height), resize_sampler)
    else:
        ret_image = image.resize((target_width, target_height), resize_sampler)
    return ret_image


def is_valid_mask(tensor: torch.Tensor) -> bool:
    return tensor.sum().item() > 0
