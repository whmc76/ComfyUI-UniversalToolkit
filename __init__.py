"""
ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~

A comprehensive toolkit for ComfyUI that provides various utility nodes for image processing, text manipulation, and more.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

__version__ = "1.0.8"
__author__ = "CyberDickLang"
__email__ = "286878701@qq.com"
__url__ = "https://github.com/whmc76"

# 更新日志
CHANGELOG = {
    "1.0.8": [
        "新增 ImitationHueNode_UTK 节点（追色节点）:",
        "- 基于 ComfyUI-MingNodes 项目集成",
        "- 支持图像色彩迁移和追色功能",
        "- 支持皮肤保护参数，避免肤色失真",
        "- 支持自动亮度、对比度、饱和度调节",
        "- 支持影调模仿功能",
        "- 支持区域色彩迁移（通过掩码）",
        "- 添加 opencv-python 依赖支持",
    ],
    "1.0.7": [
        "改进 ImagePadForOutpaintMasked (UTK) 节点:",
        "- 新增数据模式（data_mode）参数，支持 'pixel' 和 'percent' 两种模式",
        "- 在 'percent' 模式下，允许输入大于100的百分比",
        "- 新增背景颜色（background_color）预设选项",
        "改进 ImageAndMaskPreview (UTK) 节点:",
        "- 将颜色输入从手动输入字符串改为预设颜色下拉菜单",
    ],
    "1.0.6": [
        "新增 ImageAndMaskPreview_UTK 节点，用于同时预览图像和掩码：",
        "- 支持叠加模式（overlay）：在图像上叠加彩色掩码",
        "- 支持并排模式（side_by_side）：图像和掩码并排显示",
        "- 支持单独显示模式（mask_only/image_only）",
        "- 支持多种掩码颜色和透明度调节"
    ],
    "1.0.5": [
        "新增 ImagePadForOutpaintMasked_UTK 节点，用于外绘时扩展图像尺寸：",
        "- 支持上下左右四个方向的独立扩展",
        "- 支持多种背景颜色（黑、白、灰、透明）",
        "- 支持掩码边缘羽化效果",
        "- 自动生成对应的掩码用于后续处理"
    ],
    "1.0.4": [
        "新增 FillMaskedArea_UTK 节点，支持三种填充模式：",
        "- neutral: 使用灰色填充，适合添加全新内容",
        "- telea: 基于 Telea 算法的边界填充",
        "- navier-stokes: 基于流体动力学的边界填充",
        "添加 opencv-python 依赖支持"
    ],
    "1.0.3": [
        "新增 MaskAnd_UTK、MaskSub_UTK、MaskAdd_UTK 三个mask像素级运算节点 (UTK)",
        "修正节点注册与显示名风格统一，完善导入路径"
    ],
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

from .nodes.image_nodes_utk import EmptyUnitGenerator_UTK, ImageRatioDetector_UTK, DepthMapBlur_UTK, ImageConcatenate_UTK, ImageConcatenateMulti_UTK, ImagePadForOutpaintMasked_UTK, ImageAndMaskPreview_UTK, ImitationHueNode_UTK
from .nodes.tool_nodes_utk import ShowInt_UTK, ShowFloat_UTK, ShowList_UTK, ShowText_UTK, PreviewMask_UTK, FillMaskedArea_UTK
from .nodes.audio_nodes_utk import LoadAudioPlusFromPath_UTK, AudioCropProcessUTK
from .nodes.mask_nodes_utk import MaskAnd_UTK, MaskSub_UTK, MaskAdd_UTK

NODE_CLASS_MAPPINGS = {
    "EmptyUnitGenerator_UTK": EmptyUnitGenerator_UTK,
    "ImageRatioDetector_UTK": ImageRatioDetector_UTK,
    "ShowInt_UTK": ShowInt_UTK,
    "ShowFloat_UTK": ShowFloat_UTK,
    "ShowList_UTK": ShowList_UTK,
    "ShowText_UTK": ShowText_UTK,
    "PreviewMask_UTK": PreviewMask_UTK,
    "FillMaskedArea_UTK": FillMaskedArea_UTK,
    "ImageAndMaskPreview_UTK": ImageAndMaskPreview_UTK,
    "DepthMapBlur_UTK": DepthMapBlur_UTK,
    "ImageConcatenate_UTK": ImageConcatenate_UTK,
    "ImageConcatenateMulti_UTK": ImageConcatenateMulti_UTK,
    "ImagePadForOutpaintMasked_UTK": ImagePadForOutpaintMasked_UTK,
    "LoadAudioPlusFromPath_UTK": LoadAudioPlusFromPath_UTK,
    "AudioCropProcessUTK": AudioCropProcessUTK,
    "MaskAnd_UTK": MaskAnd_UTK,
    "MaskSub_UTK": MaskSub_UTK,
    "MaskAdd_UTK": MaskAdd_UTK,
    "ImitationHueNode_UTK": ImitationHueNode_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmptyUnitGenerator_UTK": "Empty Unit Generator",
    "ImageRatioDetector_UTK": "Image Ratio Detector",
    "ShowInt_UTK": "Show Int (UTK)",
    "ShowFloat_UTK": "Show Float (UTK)",
    "ShowList_UTK": "Show List (UTK)",
    "ShowText_UTK": "Show Text (UTK)",
    "PreviewMask_UTK": "Preview Mask (UTK)",
    "FillMaskedArea_UTK": "Fill Masked Area (UTK)",
    "ImageAndMaskPreview_UTK": "Image And Mask Preview (UTK)",
    "DepthMapBlur_UTK": "Depth Map Blur",
    "ImageConcatenate_UTK": "Image Concatenate",
    "ImageConcatenateMulti_UTK": "Image Concatenate Multi",
    "ImagePadForOutpaintMasked_UTK": "Image Pad For Outpaint Masked (UTK)",
    "LoadAudioPlusFromPath_UTK": "Load Audio Plus From Path (UTK)",
    "AudioCropProcessUTK": "Audio Crop Process (UTK)",
    "MaskAnd_UTK": "Mask And (UTK)",
    "MaskSub_UTK": "Mask Sub (UTK)",
    "MaskAdd_UTK": "Mask Add (UTK)",
    "ImitationHueNode_UTK": "Imitation Hue Node (UTK)",
}

NODE_CATEGORIES = {
    "UniversalToolkit": [
        "EmptyUnitGenerator_UTK",
        "ImageRatioDetector_UTK",
        "DepthMapBlur_UTK",
        "ImageConcatenate_UTK",
        "ImageConcatenateMulti_UTK",
        "ImagePadForOutpaintMasked_UTK",
        "FillMaskedArea_UTK",
        "ImageAndMaskPreview_UTK",
        "LoadAudioPlusFromPath_UTK",
        "AudioCropProcessUTK",
        "MaskAnd_UTK",
        "MaskSub_UTK",
        "MaskAdd_UTK",
        "ImitationHueNode_UTK",
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