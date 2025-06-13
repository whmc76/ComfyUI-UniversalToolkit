"""
ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~

A comprehensive toolkit for ComfyUI that provides various utility nodes for image processing, text manipulation, and more.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

__version__ = "1.0.2"
__author__ = "CyberDickLang"
__email__ = "286878701@qq.com"
__url__ = "https://github.com/whmc76"

# 更新日志
CHANGELOG = {
    "1.0.2": [
        "删除无用节点 Load Audio Plus Upload (UTK)",
        "新增 Audio Crop Process (UTK) 支持原生音频上传",
        "修复音频处理相关bug，完善依赖"
    ],
    "1.0.1": [
        "改进 ImageConcatenate_UTK 节点：",
        "- 添加 match_image_size 参数，支持自动匹配图像尺寸",
        "- 添加 max_size 参数，限制最大输出尺寸",
        "- 添加背景颜色选项",
        "- 优化图像拼接逻辑，保持宽高比",
        "改进 ImageConcatenateMulti_UTK 节点：",
        "- 与 ImageConcatenate_UTK 保持一致的功能",
        "- 支持自动方向选择",
        "- 支持图像尺寸匹配",
        "- 支持最大尺寸限制",
        "- 优化多图拼接逻辑"
    ],
    "1.0.0": [
        "初始版本发布",
        "包含基础图像处理节点",
        "包含文本处理节点",
        "包含工具类节点"
    ]
}

from .nodes.image_nodes_utk import EmptyUnitGenerator_UTK, ImageRatioDetector_UTK, DepthMapBlur_UTK, ImageConcatenate_UTK, ImageConcatenateMulti_UTK
from .nodes.tool_nodes_utk import ShowInt_UTK, ShowFloat_UTK, ShowList_UTK, ShowText_UTK, PreviewMask_UTK
from .nodes.audio_nodes_utk import LoadAudioPlusFromPath_UTK, AudioCropProcessUTK

NODE_CLASS_MAPPINGS = {
    "EmptyUnitGenerator_UTK": EmptyUnitGenerator_UTK,
    "ImageRatioDetector_UTK": ImageRatioDetector_UTK,
    "ShowInt_UTK": ShowInt_UTK,
    "ShowFloat_UTK": ShowFloat_UTK,
    "ShowList_UTK": ShowList_UTK,
    "ShowText_UTK": ShowText_UTK,
    "PreviewMask_UTK": PreviewMask_UTK,
    "DepthMapBlur_UTK": DepthMapBlur_UTK,
    "ImageConcatenate_UTK": ImageConcatenate_UTK,
    "ImageConcatenateMulti_UTK": ImageConcatenateMulti_UTK,
    "LoadAudioPlusFromPath_UTK": LoadAudioPlusFromPath_UTK,
    "AudioCropProcessUTK": AudioCropProcessUTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmptyUnitGenerator_UTK": "Empty Unit Generator",
    "ImageRatioDetector_UTK": "Image Ratio Detector",
    "ShowInt_UTK": "Show Int (UTK)",
    "ShowFloat_UTK": "Show Float (UTK)",
    "ShowList_UTK": "Show List (UTK)",
    "ShowText_UTK": "Show Text (UTK)",
    "PreviewMask_UTK": "Preview Mask (UTK)",
    "DepthMapBlur_UTK": "Depth Map Blur",
    "ImageConcatenate_UTK": "Image Concatenate",
    "ImageConcatenateMulti_UTK": "Image Concatenate Multi",
    "LoadAudioPlusFromPath_UTK": "Load Audio Plus From Path (UTK)",
    "AudioCropProcessUTK": "Audio Crop Process (UTK)",
}

NODE_CATEGORIES = {
    "UniversalToolkit": [
        "EmptyUnitGenerator_UTK",
        "ImageRatioDetector_UTK",
        "DepthMapBlur_UTK",
        "ImageConcatenate_UTK",
        "ImageConcatenateMulti_UTK",
        "LoadAudioPlusFromPath_UTK",
        "AudioCropProcessUTK",
    ]
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "NODE_CATEGORIES",
    "__version__",
    "__author__",
    "__email__",
    "__url__",
    "CHANGELOG"
] 