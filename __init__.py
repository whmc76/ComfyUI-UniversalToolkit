"""
ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~

A comprehensive toolkit for ComfyUI that provides various utility nodes for image processing, text manipulation, and more.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

__version__ = "1.1.2"
__author__ = "CyberDickLang"
__email__ = "286878701@qq.com"
__url__ = "https://github.com/whmc76"

# 更新日志
CHANGELOG = {
    "1.1.2": [
        "修复 DepthMapBlur_UTK 节点 kernel size 类型和 OpenCV 奇数断言问题，保证所有模糊核为正奇数，完全兼容 ComfyUI 规范。",
        "修正 EmptyUnitGenerator_UTK 输出 shape，所有节点输入输出严格遵循 ComfyUI 官方规范。",
        "完善节点导入路径为相对导入，兼容 ComfyUI v3 插件机制。"
    ],
    "1.1.1": [
        "项目重构：",
        "- 将大型节点文件按功能拆分成多个独立模块",
        "- 创建共用工具函数文件 common_utils.py",
        "- 按功能分类：image/、tools/、mask/、audio/",
        "- 提高代码可维护性和模块化程度",
        "- 参考 ComfyUI-LayerStyle 项目的模块化组织方式",
        "新增多个图像处理节点：",
        "- ImageScaleByAspectRatio_UTK: 按比例缩放图像",
        "- ImageMaskScaleAs_UTK: 按参考图像缩放",
        "- ImageScaleRestore_UTK: 恢复图像尺寸",
        "- ImageRemoveAlpha_UTK: 移除Alpha通道",
        "- ImageCombineAlpha_UTK: 合并Alpha通道",
        "- CheckMask_UTK: 检查掩码有效性",
        "- PurgeVRAM_UTK: 清理显存",
        "- CropByMask_UTK: 基于掩码裁剪",
        "- RestoreCropBox_UTK: 恢复裁剪框",
    ],
    "1.1.0": [
        "新增 CropByMaskV3_UTK 节点（掩码裁剪节点）:",
        "- 基于 ComfyUI-LayerStyle 项目集成",
        "- 支持三种检测模式：mask_area、min_bounding_rect、max_inscribed_rect",
        "- 支持掩码反转功能",
        "- 支持四个方向的预留边距设置",
        "- 支持整除倍数调整",
        "- 提供裁剪框预览功能",
        "新增 RestoreCropBox_UTK 节点（恢复裁剪框节点）:",
        "- 基于 ComfyUI-LayerStyle 项目集成",
        "- 支持将裁剪后的图像恢复到原始背景",
        "- 支持掩码反转功能",
        "- 支持自定义裁剪框位置",
        "- 自动处理批量图像和掩码",
    ],
    "1.0.9": [
        "新增 PurgeVRAM_UTK 节点（显存清理节点）:",
        "- 基于 ComfyUI-LayerStyle 项目集成",
        "- 支持清理GPU缓存和模型内存",
        "- 支持选择性清理（缓存/模型）",
        "- 添加内存清理辅助函数",
        "- 支持任意类型输入，保持数据流连续性",
    ],
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

# 导入节点模块
try:
    # 工具类节点
    from .nodes.tools.show_nodes import NODE_CLASS_MAPPINGS as SHOW_NODES_MAPPINGS
    from .nodes.tools.show_nodes import NODE_DISPLAY_NAME_MAPPINGS as SHOW_NODES_DISPLAY_MAPPINGS
    
    # 音频节点
    from .nodes.audio.audio_crop_process import NODE_CLASS_MAPPINGS as AUDIO_CROP_MAPPINGS
    from .nodes.audio.audio_crop_process import NODE_DISPLAY_NAME_MAPPINGS as AUDIO_CROP_DISPLAY_MAPPINGS
    
    # 掩码节点
    from .nodes.mask.mask_operations import NODE_CLASS_MAPPINGS as MASK_OPERATIONS_MAPPINGS
    from .nodes.mask.mask_operations import NODE_DISPLAY_NAME_MAPPINGS as MASK_OPERATIONS_DISPLAY_MAPPINGS
    
    # 图像节点
    from .nodes.image.image_concatenate_multi import NODE_CLASS_MAPPINGS as CONCATENATE_MULTI_MAPPINGS
    from .nodes.image.image_concatenate_multi import NODE_DISPLAY_NAME_MAPPINGS as CONCATENATE_MULTI_DISPLAY_MAPPINGS
    
    from .nodes.image.image_pad_for_outpaint_masked import NODE_CLASS_MAPPINGS as PAD_OUTPAINT_MAPPINGS
    from .nodes.image.image_pad_for_outpaint_masked import NODE_DISPLAY_NAME_MAPPINGS as PAD_OUTPAINT_DISPLAY_MAPPINGS
    
    from .nodes.image.image_and_mask_preview import NODE_CLASS_MAPPINGS as AND_MASK_PREVIEW_MAPPINGS
    from .nodes.image.image_and_mask_preview import NODE_DISPLAY_NAME_MAPPINGS as AND_MASK_PREVIEW_DISPLAY_MAPPINGS
    
    from .nodes.image.imitation_hue_node import NODE_CLASS_MAPPINGS as IMITATION_HUE_MAPPINGS
    from .nodes.image.imitation_hue_node import NODE_DISPLAY_NAME_MAPPINGS as IMITATION_HUE_DISPLAY_MAPPINGS

except ImportError as e:
    print(f"导入错误: {e}")
    # 如果模块化导入失败，使用空字典
    SHOW_NODES_MAPPINGS = {}
    SHOW_NODES_DISPLAY_MAPPINGS = {}
    AUDIO_CROP_MAPPINGS = {}
    AUDIO_CROP_DISPLAY_MAPPINGS = {}
    MASK_OPERATIONS_MAPPINGS = {}
    MASK_OPERATIONS_DISPLAY_MAPPINGS = {}
    CONCATENATE_MULTI_MAPPINGS = {}
    CONCATENATE_MULTI_DISPLAY_MAPPINGS = {}
    PAD_OUTPAINT_MAPPINGS = {}
    PAD_OUTPAINT_DISPLAY_MAPPINGS = {}
    AND_MASK_PREVIEW_MAPPINGS = {}
    AND_MASK_PREVIEW_DISPLAY_MAPPINGS = {}
    IMITATION_HUE_MAPPINGS = {}
    IMITATION_HUE_DISPLAY_MAPPINGS = {}

# 尝试导入其他可能有依赖的节点
try:
    from .nodes.tools.fill_masked_area import NODE_CLASS_MAPPINGS as FILL_MASKED_MAPPINGS
    from .nodes.tools.fill_masked_area import NODE_DISPLAY_NAME_MAPPINGS as FILL_MASKED_DISPLAY_MAPPINGS
except ImportError:
    FILL_MASKED_MAPPINGS = {}
    FILL_MASKED_DISPLAY_MAPPINGS = {}

try:
    from .nodes.audio.load_audio import NODE_CLASS_MAPPINGS as LOAD_AUDIO_MAPPINGS
    from .nodes.audio.load_audio import NODE_DISPLAY_NAME_MAPPINGS as LOAD_AUDIO_DISPLAY_MAPPINGS
except ImportError:
    LOAD_AUDIO_MAPPINGS = {}
    LOAD_AUDIO_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.empty_unit_generator import NODE_CLASS_MAPPINGS as IMAGE_GENERATOR_MAPPINGS
    from .nodes.image.empty_unit_generator import NODE_DISPLAY_NAME_MAPPINGS as IMAGE_GENERATOR_DISPLAY_MAPPINGS
except ImportError:
    IMAGE_GENERATOR_MAPPINGS = {}
    IMAGE_GENERATOR_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.image_ratio_detector import NODE_CLASS_MAPPINGS as IMAGE_DETECTOR_MAPPINGS
    from .nodes.image.image_ratio_detector import NODE_DISPLAY_NAME_MAPPINGS as IMAGE_DETECTOR_DISPLAY_MAPPINGS
except ImportError:
    IMAGE_DETECTOR_MAPPINGS = {}
    IMAGE_DETECTOR_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.depth_map_blur import NODE_CLASS_MAPPINGS as DEPTH_BLUR_MAPPINGS
    from .nodes.image.depth_map_blur import NODE_DISPLAY_NAME_MAPPINGS as DEPTH_BLUR_DISPLAY_MAPPINGS
except ImportError:
    DEPTH_BLUR_MAPPINGS = {}
    DEPTH_BLUR_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.image_concatenate import NODE_CLASS_MAPPINGS as CONCATENATE_MAPPINGS
    from .nodes.image.image_concatenate import NODE_DISPLAY_NAME_MAPPINGS as CONCATENATE_DISPLAY_MAPPINGS
except ImportError:
    CONCATENATE_MAPPINGS = {}
    CONCATENATE_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.image_scale_by_aspect_ratio import NODE_CLASS_MAPPINGS as SCALE_ASPECT_MAPPINGS
    from .nodes.image.image_scale_by_aspect_ratio import NODE_DISPLAY_NAME_MAPPINGS as SCALE_ASPECT_DISPLAY_MAPPINGS
except ImportError:
    SCALE_ASPECT_MAPPINGS = {}
    SCALE_ASPECT_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.image_mask_scale_as import NODE_CLASS_MAPPINGS as MASK_SCALE_MAPPINGS
    from .nodes.image.image_mask_scale_as import NODE_DISPLAY_NAME_MAPPINGS as MASK_SCALE_DISPLAY_MAPPINGS
except ImportError:
    MASK_SCALE_MAPPINGS = {}
    MASK_SCALE_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.image_scale_restore import NODE_CLASS_MAPPINGS as SCALE_RESTORE_MAPPINGS
    from .nodes.image.image_scale_restore import NODE_DISPLAY_NAME_MAPPINGS as SCALE_RESTORE_DISPLAY_MAPPINGS
except ImportError:
    SCALE_RESTORE_MAPPINGS = {}
    SCALE_RESTORE_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.image_remove_alpha import NODE_CLASS_MAPPINGS as REMOVE_ALPHA_MAPPINGS
    from .nodes.image.image_remove_alpha import NODE_DISPLAY_NAME_MAPPINGS as REMOVE_ALPHA_DISPLAY_MAPPINGS
except ImportError:
    REMOVE_ALPHA_MAPPINGS = {}
    REMOVE_ALPHA_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.image_combine_alpha import NODE_CLASS_MAPPINGS as COMBINE_ALPHA_MAPPINGS
    from .nodes.image.image_combine_alpha import NODE_DISPLAY_NAME_MAPPINGS as COMBINE_ALPHA_DISPLAY_MAPPINGS
except ImportError:
    COMBINE_ALPHA_MAPPINGS = {}
    COMBINE_ALPHA_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.check_mask import NODE_CLASS_MAPPINGS as CHECK_MASK_MAPPINGS
    from .nodes.image.check_mask import NODE_DISPLAY_NAME_MAPPINGS as CHECK_MASK_DISPLAY_MAPPINGS
except ImportError:
    CHECK_MASK_MAPPINGS = {}
    CHECK_MASK_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.purge_vram import NODE_CLASS_MAPPINGS as PURGE_VRAM_MAPPINGS
    from .nodes.image.purge_vram import NODE_DISPLAY_NAME_MAPPINGS as PURGE_VRAM_DISPLAY_MAPPINGS
except ImportError:
    PURGE_VRAM_MAPPINGS = {}
    PURGE_VRAM_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.crop_by_mask import NODE_CLASS_MAPPINGS as CROP_MASK_MAPPINGS
    from .nodes.image.crop_by_mask import NODE_DISPLAY_NAME_MAPPINGS as CROP_MASK_DISPLAY_MAPPINGS
except ImportError:
    CROP_MASK_MAPPINGS = {}
    CROP_MASK_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.restore_crop_box import NODE_CLASS_MAPPINGS as RESTORE_CROP_MAPPINGS
    from .nodes.image.restore_crop_box import NODE_DISPLAY_NAME_MAPPINGS as RESTORE_CROP_DISPLAY_MAPPINGS
except ImportError:
    RESTORE_CROP_MAPPINGS = {}
    RESTORE_CROP_DISPLAY_MAPPINGS = {}

# 合并所有节点映射
NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(IMAGE_GENERATOR_MAPPINGS)
NODE_CLASS_MAPPINGS.update(IMAGE_DETECTOR_MAPPINGS)
NODE_CLASS_MAPPINGS.update(DEPTH_BLUR_MAPPINGS)
NODE_CLASS_MAPPINGS.update(CONCATENATE_MAPPINGS)
NODE_CLASS_MAPPINGS.update(CONCATENATE_MULTI_MAPPINGS)
NODE_CLASS_MAPPINGS.update(PAD_OUTPAINT_MAPPINGS)
NODE_CLASS_MAPPINGS.update(AND_MASK_PREVIEW_MAPPINGS)
NODE_CLASS_MAPPINGS.update(IMITATION_HUE_MAPPINGS)
NODE_CLASS_MAPPINGS.update(SCALE_ASPECT_MAPPINGS)
NODE_CLASS_MAPPINGS.update(MASK_SCALE_MAPPINGS)
NODE_CLASS_MAPPINGS.update(SCALE_RESTORE_MAPPINGS)
NODE_CLASS_MAPPINGS.update(REMOVE_ALPHA_MAPPINGS)
NODE_CLASS_MAPPINGS.update(COMBINE_ALPHA_MAPPINGS)
NODE_CLASS_MAPPINGS.update(CHECK_MASK_MAPPINGS)
NODE_CLASS_MAPPINGS.update(PURGE_VRAM_MAPPINGS)
NODE_CLASS_MAPPINGS.update(CROP_MASK_MAPPINGS)
NODE_CLASS_MAPPINGS.update(RESTORE_CROP_MAPPINGS)
NODE_CLASS_MAPPINGS.update(SHOW_NODES_MAPPINGS)
NODE_CLASS_MAPPINGS.update(FILL_MASKED_MAPPINGS)
NODE_CLASS_MAPPINGS.update(LOAD_AUDIO_MAPPINGS)
NODE_CLASS_MAPPINGS.update(AUDIO_CROP_MAPPINGS)
NODE_CLASS_MAPPINGS.update(MASK_OPERATIONS_MAPPINGS)

# 合并显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(IMAGE_GENERATOR_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(IMAGE_DETECTOR_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(DEPTH_BLUR_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(CONCATENATE_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(CONCATENATE_MULTI_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(PAD_OUTPAINT_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(AND_MASK_PREVIEW_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(IMITATION_HUE_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(SCALE_ASPECT_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(MASK_SCALE_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(SCALE_RESTORE_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(REMOVE_ALPHA_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(COMBINE_ALPHA_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(CHECK_MASK_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(PURGE_VRAM_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(CROP_MASK_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(RESTORE_CROP_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(SHOW_NODES_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(FILL_MASKED_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(LOAD_AUDIO_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(AUDIO_CROP_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(MASK_OPERATIONS_DISPLAY_MAPPINGS)

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
        "ImageScaleByAspectRatio_UTK",
        "ImageMaskScaleAs_UTK",
        "ImageScaleRestore_UTK",
        "ImageRemoveAlpha_UTK",
        "ImageCombineAlpha_UTK",
        "CheckMask_UTK",
        "PurgeVRAM_UTK",
        "CropByMask_UTK",
        "RestoreCropBox_UTK",
        "Show_UTK",
        "ShowFloat_UTK",
        "PreviewMask_UTK",
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
    "CHANGELOG",
] 
