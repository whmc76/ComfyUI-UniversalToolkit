"""
ComfyUI Universal Toolkit - Common Utilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Common utility functions and constants used across all nodes.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import torch.nn.functional as F
import numpy as np
import re
import math
import random
import os
import json
import cv2
from comfy.utils import ProgressBar, common_upscale
from PIL import Image
from PIL.PngImagePlugin import PngInfo

# Import ComfyUI modules with fallbacks
MAX_RESOLUTION = 8192
SaveImage = None
ImageCompositeMasked = None
args = None
folder_paths = None

try:
    from nodes import MAX_RESOLUTION, SaveImage
except ImportError:
    pass

try:
    from comfy_extras.nodes_mask import ImageCompositeMasked
except ImportError:
    pass

try:
    from comfy.cli_args import args
except ImportError:
    pass

try:
    import folder_paths
except ImportError:
    pass

def log(message, message_type='info'):
    """简单的日志函数"""
    if message_type == 'error':
        print(f"❌ Error: {message}")
    elif message_type == 'warning':
        print(f"⚠️ Warning: {message}")
    elif message_type == 'finish':
        print(f"✅ {message}")
    else:
        print(f"ℹ️ {message}")

def tensor2pil(image):
    """将torch张量转换为PIL图像"""
    if image.dim() == 4:
        image = image.squeeze(0)
    if image.dim() == 3:
        if image.shape[0] == 1:  # 灰度图
            image = image.squeeze(0)
            image = (image * 255).clamp(0, 255).to(torch.uint8)
            return Image.fromarray(image.cpu().numpy(), mode='L')
        else:  # RGB图
            image = image.permute(1, 2, 0)
            image = (image * 255).clamp(0, 255).to(torch.uint8)
            return Image.fromarray(image.cpu().numpy(), mode='RGB')
    return None

def pil2tensor(image):
    """将PIL图像转换为torch张量"""
    if image.mode == 'L':
        image = image.convert('RGB')
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image)
    if image.dim() == 3:
        image = image.permute(2, 0, 1)
    return image

def image2mask(image):
    """将PIL图像转换为掩码张量"""
    if image.mode == 'L':
        return torch.tensor([pil2tensor(image)[0, :, :].tolist()])
    else:
        image = image.convert('RGB').split()[0]
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
        return [np.clip(255.0 * t.cpu().numpy(), 0, 255).astype(np.uint8) for t in tensor]

# Color transfer functions for ImitationHueNode
def image_stats(image):
    return np.mean(image[:, :, 1:], axis=(0, 1)), np.std(image[:, :, 1:], axis=(0, 1))

def is_skin_or_lips(lab_image):
    l, a, b = lab_image[:, :, 0], lab_image[:, :, 1], lab_image[:, :, 2]
    skin = (l > 20) & (l < 250) & (a > 120) & (a < 180) & (b > 120) & (b < 190)
    lips = (l > 20) & (l < 200) & (a > 150) & (b > 140)
    return (skin | lips).astype(np.float32)

def adjust_brightness(image, factor, mask=None):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2].astype(np.float32)
    if mask is not None:
        mask = mask.squeeze()
        v = np.where(mask > 0, np.clip(v * factor, 0, 255), v)
    else:
        v = np.clip(v * factor, 0, 255)
    hsv[:, :, 2] = v.astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def adjust_saturation(image, factor, mask=None):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    s = hsv[:, :, 1].astype(np.float32)
    if mask is not None:
        mask = mask.squeeze()
        s = np.where(mask > 0, np.clip(s * factor, 0, 255), s)
    else:
        s = np.clip(s * factor, 0, 255)
    hsv[:, :, 1] = s.astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def adjust_contrast(image, factor, mask=None):
    mean = np.mean(image)
    adjusted = image.astype(np.float32)
    if mask is not None:
        mask = mask.squeeze()
        mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
        adjusted = np.where(mask > 0, np.clip((adjusted - mean) * factor + mean, 0, 255), adjusted)
    else:
        adjusted = np.clip((adjusted - mean) * factor + mean, 0, 255)
    return adjusted.astype(np.uint8)

def adjust_tone(source, target, tone_strength=0.7, mask=None):
    h, w = target.shape[:2]
    source = cv2.resize(source, (w, h))
    lab_image = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype(np.float32)
    lab_source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype(np.float32)
    l_image = lab_image[:,:,0]
    l_source = lab_source[:,:,0]

    if mask is not None:
        mask = cv2.resize(mask, (w, h))
        mask = mask.astype(np.float32) / 255.0
        l_adjusted = np.copy(l_image)
        mean_source = np.mean(l_source[mask > 0])
        std_source = np.std(l_source[mask > 0])
        mean_target = np.mean(l_image[mask > 0])
        std_target = np.std(l_image[mask > 0])
        l_adjusted[mask > 0] = (l_image[mask > 0] - mean_target) * (std_source / (std_target + 1e-6)) * 0.7 + mean_source
        l_adjusted[mask > 0] = np.clip(l_adjusted[mask > 0], 0, 255)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
        l_enhanced = clahe.apply(l_adjusted.astype(np.uint8))
        l_final = cv2.addWeighted(l_adjusted, 0.7, l_enhanced.astype(np.float32), 0.3, 0)
        l_final = np.clip(l_final, 0, 255)
        l_contrast = cv2.addWeighted(l_final, 1.3, l_final, 0, -20)
        l_contrast = np.clip(l_contrast, 0, 255)
        l_image[mask > 0] = l_image[mask > 0] * (1 - tone_strength) + l_contrast[mask > 0] * tone_strength
    else:
        mean_source = np.mean(l_source)
        std_source = np.std(l_source)
        l_mean = np.mean(l_image)
        l_std = np.std(l_image)
        l_adjusted = (l_image - l_mean) * (std_source / (l_std + 1e-6)) * 0.7 + mean_source
        l_adjusted = np.clip(l_adjusted, 0, 255)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
        l_enhanced = clahe.apply(l_adjusted.astype(np.uint8))
        l_final = cv2.addWeighted(l_adjusted, 0.7, l_enhanced.astype(np.float32), 0.3, 0)
        l_final = np.clip(l_final, 0, 255)
        l_contrast = cv2.addWeighted(l_final, 1.3, l_final, 0, -20)
        l_contrast = np.clip(l_contrast, 0, 255)
        l_image = l_image * (1 - tone_strength) + l_contrast * tone_strength

    lab_image[:,:,0] = l_image
    return cv2.cvtColor(lab_image.astype(np.uint8), cv2.COLOR_LAB2BGR)

def color_transfer(source, target, mask=None, strength=1.0, skin_protection=0.2, auto_brightness=True,
                   brightness_range=0.5, auto_contrast=False, contrast_range=0.5,
                   auto_saturation=False, saturation_range=0.5, auto_tone=False, tone_strength=0.7):
    source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype(np.float32)
    target_lab = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype(np.float32)

    src_means, src_stds = image_stats(source_lab)
    tar_means, tar_stds = image_stats(target_lab)

    skin_lips_mask = is_skin_or_lips(target_lab.astype(np.uint8))
    skin_lips_mask = cv2.GaussianBlur(skin_lips_mask, (5, 5), 0)

    if mask is not None:
        mask = cv2.resize(mask, (target.shape[1], target.shape[0]))
        mask = mask.astype(np.float32) / 255.0

    result_lab = target_lab.copy()
    for i in range(1, 3):
        adjusted_channel = (target_lab[:, :, i] - tar_means[i - 1]) * (src_stds[i - 1] / (tar_stds[i - 1] + 1e-6)) + \
                           src_means[i - 1]
        adjusted_channel = np.clip(adjusted_channel, 0, 255)

        if mask is not None:
            result_lab[:, :, i] = target_lab[:, :, i] * (1 - mask) + \
                                  (target_lab[:, :, i] * skin_lips_mask * skin_protection + \
                                   adjusted_channel * skin_lips_mask * (1 - skin_protection) + \
                                   adjusted_channel * (1 - skin_lips_mask)) * mask
        else:
            result_lab[:, :, i] = target_lab[:, :, i] * skin_lips_mask * skin_protection + \
                                  adjusted_channel * skin_lips_mask * (1 - skin_protection) + \
                                  adjusted_channel * (1 - skin_lips_mask)

    result_bgr = cv2.cvtColor(result_lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
    final_result = cv2.addWeighted(target, 1 - strength, result_bgr, strength, 0)

    if mask is not None:
        mask = cv2.resize(mask, (target.shape[1], target.shape[0]))
        mask = mask.astype(np.float32) / 255.0
        if auto_brightness:
            source_brightness = np.mean(cv2.cvtColor(source, cv2.COLOR_BGR2GRAY))
            target_brightness = np.mean(cv2.cvtColor(target, cv2.COLOR_BGR2GRAY))
            brightness_difference = source_brightness - target_brightness
            brightness_factor = 1.0 + np.clip(brightness_difference / 255 * brightness_range, brightness_range*-1, brightness_range)
            final_result = adjust_brightness(final_result, brightness_factor, mask)
        if auto_contrast:
            source_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
            target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
            source_contrast = np.std(source_gray)
            target_contrast = np.std(target_gray)
            contrast_difference = source_contrast - target_contrast
            contrast_factor = 1.0 + np.clip(contrast_difference / 255, contrast_range*-1, contrast_range)
            final_result = adjust_contrast(final_result, contrast_factor, mask)
        if auto_saturation:
            source_hsv = cv2.cvtColor(source, cv2.COLOR_BGR2HSV)
            target_hsv = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
            source_saturation = np.mean(source_hsv[:, :, 1])
            target_saturation = np.mean(target_hsv[:, :, 1])
            saturation_difference = source_saturation - target_saturation
            saturation_factor = 1.0 + np.clip(saturation_difference / 255, saturation_range*-1, saturation_range)
            final_result = adjust_saturation(final_result, saturation_factor, mask)
        if auto_tone:
            final_result = adjust_tone(source, final_result, tone_strength, mask)
    else:
        if auto_brightness:
            source_brightness = np.mean(cv2.cvtColor(source, cv2.COLOR_BGR2GRAY))
            target_brightness = np.mean(cv2.cvtColor(target, cv2.COLOR_BGR2GRAY))
            brightness_difference = source_brightness - target_brightness
            brightness_factor = 1.0 + np.clip(brightness_difference / 255 * brightness_range, brightness_range*-1, brightness_range)
            final_result = adjust_brightness(final_result, brightness_factor)
        if auto_contrast:
            source_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
            target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
            source_contrast = np.std(source_gray)
            target_contrast = np.std(target_gray)
            contrast_difference = source_contrast - target_contrast
            contrast_factor = 1.0 + np.clip(contrast_difference / 255, contrast_range*-1, contrast_range)
            final_result = adjust_contrast(final_result, contrast_factor)
        if auto_saturation:
            source_hsv = cv2.cvtColor(source, cv2.COLOR_BGR2HSV)
            target_hsv = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
            source_saturation = np.mean(source_hsv[:, :, 1])
            target_saturation = np.mean(target_hsv[:, :, 1])
            saturation_difference = source_saturation - target_saturation
            saturation_factor = 1.0 + np.clip(saturation_difference / 255, saturation_range*-1, saturation_range)
            final_result = adjust_saturation(final_result, saturation_factor)
        if auto_tone:
            final_result = adjust_tone(source, final_result, tone_strength)

    return final_result 