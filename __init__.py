"""
ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~

A comprehensive toolkit for ComfyUI that provides various utility nodes for image processing, text manipulation, and more.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

__version__ = "1.2.5"
__author__ = "CyberDickLang"
__email__ = "286878701@qq.com"
__url__ = "https://github.com/whmc76"

# 更新日志
CHANGELOG = {
    "1.2.5": [
        "优化Kontext预设系统，提升用户体验：",
        "- 为所有预设添加英文分类前缀，提升节点中的可读性",
        "- 重新组织预设分类：Core-核心编辑、Composite-图像合成、Scene-场景环境、Photo-摄影技术、Character-人物变换、Art-艺术风格、Effect-特殊效果、Utility-实用功能",
        "- 将花纹提取预设移动到实用功能类，更符合其功能定位",
        "- 升级身材改造预设，支持多种身材变化（高矮胖瘦、强壮肌肉、性感身材等）",
        "- 优化衣橱改造预设，强调保持角色特征不变和服装自然性",
        "- 升级专业产品图预设，确保产品特征不变和环境自然集成",
        "- 改进角色姿势视角变换预设，支持多种角度和姿势变化",
        "- 结合社区最佳实践，优化所有预设的brief描述",
        "- 提升预设指令的精确性和实用性",
        "- 保持所有预设的完整功能，总数维持30个",
    ],
    "1.2.4": [
        "优化预设分类结构，提升用户体验：",
        "- 重新整理预设分类，合并相似类别，减少重复",
        "- 将原11个分类优化为7个主要分类：核心编辑、图像合成、场景环境、摄影技术、人物变换、艺术风格、特殊效果",
        "- 将视角变换类合并到摄影技术类，将花纹提取类合并到核心编辑类",
        "- 将环境变换类合并到场景环境类，简化分类结构",
        "- 优化预设顺序，保持万能编辑作为默认选项",
        "- 提升预设分类的逻辑性和易用性",
        "- 保持所有30个预设的完整功能不变",
    ],
    "1.2.3": [
        "新增花纹提取预设和优化用户体验：",
        "- 添加Pattern Extraction (花纹提取)预设，支持指定提取对象",
        "- 将Universal Editor (万能编辑)预设移到最前面作为默认选项",
        "- 优化预设顺序，提升用户使用体验",
        "- 支持从任意对象中提取花纹、logo、图案等",
        "- 完全支持$user_prompt$占位符替换机制",
        "- 预设总数达到30个，覆盖各种图像处理需求",
    ],
    "1.2.2": [
        "新增万能编辑预设功能：",
        "- 添加Universal Editor (万能编辑)预设，支持精确的图像编辑指令转换",
        "- 基于Kontext格式和Flux模型的编辑指令生成",
        "- 支持人物、物体、背景、风格、文本等多种编辑类型",
        "- 严格遵循9条编辑规则，确保视觉一致性和精确性",
        "- 完全支持$user_prompt$占位符替换机制",
        "- 优化预设指令结构，移除重复的英文输出要求",
    ],
    "1.2.1": [
        "修复自动发布问题：",
        "- 精简pyproject.toml依赖配置，仅保留核心依赖",
        "- 解决Comfy Registry自动发布失败问题",
        "- 更新版本号避免重复发布",
        "- 确保依赖配置与Comfy Registry兼容",
    ],
    "1.2.0": [
        "版本更新发布：",
        "- 全面更新README文档，提供详细的功能介绍和使用指南",
        "- 优化项目结构和文档组织",
        "- 完善节点功能说明和分类",
        "- 更新版本推送代码，确保发布流程顺畅",
        "- 提升项目整体文档质量和用户体验",
    ],
    "1.1.9": [
        "升级 LoadKontextPresets_UTK 节点功能：",
        "- 新增用户提示输入参数（user_prompt），支持多行文本输入",
        "- 为所有27个预设添加$user_prompt$占位符，支持动态场景描述",
        "- 改造所有预设的brief描述，使其能够根据用户输入生成具体指令",
        "- 智能占位符替换：有用户输入时替换为具体需求，无输入时使用通用描述",
        "- 支持重新布光、场景传送、季节变换等预设的用户自定义场景",
        "- 支持人物变换、艺术风格、特殊效果等预设的个性化需求",
        "- 提升VLM模型生成指令的针对性和实用性",
        "- 保持原有27个预设的完整功能和分类结构",
    ],
    "1.1.8": [
        "新增 LoadKontextPresets_UTK 节点（Kontext VLM System Presets）：",
        "- 基于 Kontext 项目集成，提供25种图像变换预设",
        "- 支持情境深度融合、无痕融合、场景传送等多种预设",
        "- 支持移动镜头、重新布光、专业产品图等专业预设",
        "- 支持画面缩放、图像上色、电影海报等创意预设",
        "- 支持卡通漫画化、移除文字、更换发型等功能预设",
        "- 支持肌肉猛男化、清空家具、室内设计等特殊预设",
        "- 支持季节变换、时光旅人、材质置换等艺术预设",
        "- 支持微缩世界、幻想领域、衣橱改造等创意预设",
        "- 支持艺术风格模仿、蓝图视角、添加倒影等效果预设",
        "- 支持像素艺术、铅笔手绘、油画风格等艺术风格预设",
        "- 所有预设均按照官方指南进行重写和升级，提供专业的图像变换指令",
    ],
    "1.1.7": [
        "新增 ThinkRemover_UTK 节点：",
        "- 支持分离文本中的<think>内容和剩余内容，便于上下文处理和提示词优化",
    ],
    "1.1.6": [
        "新增 TextboxNode_UTK 节点（文本框节点）：",
        "- 基于 ComfyUI-LayerStyle 项目集成",
        "- 支持在图像上添加自定义样式的文本框",
        "- 支持文本颜色、背景颜色、透明度调节",
        "- 支持圆角边框、边框宽度和颜色设置",
        "- 支持文本对齐方式（左对齐、居中、右对齐）",
        "- 支持自定义字体路径和字体大小",
        "- 支持文本框位置精确定位",
        "- 支持文本自动换行和最大宽度限制",
        "- 支持批量图像处理",
    ],
    "1.1.5": [
        "版本更新发布：",
        "- 优化ImitationHueNode_UTK节点的色彩迁移算法",
        "- 改进皮肤保护功能，提高肤色保持效果",
        "- 增强自动亮度、对比度、饱和度调节的稳定性",
        "- 完善影调模仿功能的实现",
        "- 优化区域色彩迁移的掩码处理",
        "- 提升整体色彩迁移的自然度和准确性",
    ],
    "1.1.4": [
        "版本更新发布：",
        "- 更新插件版本号以支持ComfyUI-Manager和Registry获取",
        "- 确保与ComfyUI v3完全兼容",
        "- 优化插件元数据和发布配置",
    ],
    "1.1.3": [
        "修复 PurgeVRAM_UTK 节点类型不匹配问题：",
        "- 创建 AnyType 类实现，参考 ComfyUI-LayerStyle 项目",
        "- 解决 'received_type(IMAGE) mismatch input_type(*)' 错误",
        "- 支持接受任何类型输入并正确返回",
        "修复 CheckMask_UTK 节点 NoneType 错误：",
        "- 添加空值检查，防止 mask 为 None 时出错",
        "- 改进 tensor2pil 转换失败的处理",
        "- 增强错误处理和日志输出",
        "完成模块化重构：",
        "- 将 common_utils.py 功能拆分到不同目录",
        "- 创建 image_converters.py、color_utils.py、logging_utils.py、any_type.py",
        "- 删除 common_utils.py，避免依赖冲突",
        "- 更新所有相关文件的导入语句",
        "- 提高代码可维护性和模块化程度",
    ],
    "1.1.2": [
        "修复 DepthMapBlur_UTK 节点 kernel size 类型和 OpenCV 奇数断言问题，保证所有模糊核为正奇数，完全兼容 ComfyUI 规范。",
        "修正 EmptyUnitGenerator_UTK 输出 shape，所有节点输入输出严格遵循 ComfyUI 官方规范。",
        "完善节点导入路径为相对导入，兼容 ComfyUI v3 插件机制。",
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
        "- 支持多种掩码颜色和透明度调节",
    ],
    "1.0.5": [
        "新增 ImagePadForOutpaintMasked_UTK 节点，用于外绘时扩展图像尺寸：",
        "- 支持上下左右四个方向的独立扩展",
        "- 支持多种背景颜色（黑、白、灰、透明）",
        "- 支持掩码边缘羽化效果",
        "- 自动生成对应的掩码用于后续处理",
    ],
    "1.0.4": [
        "新增 FillMaskedArea_UTK 节点，支持三种填充模式：",
        "- neutral: 使用灰色填充，适合添加全新内容",
        "- telea: 基于 Telea 算法的边界填充",
        "- navier-stokes: 基于流体动力学的边界填充",
        "添加 opencv-python 依赖支持",
    ],
    "1.0.3": [
        "新增 MaskAnd_UTK、MaskSub_UTK、MaskAdd_UTK 三个mask像素级运算节点 (UTK)",
        "修正节点注册与显示名风格统一，完善导入路径",
    ],
    "1.0.2": [
        "删除无用节点 Load Audio Plus Upload (UTK)",
        "新增 Audio Crop Process (UTK) 支持原生音频上传",
        "修复音频处理相关bug，完善依赖",
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
        "- 优化多图拼接逻辑",
    ],
    "1.0.0": [
        "初始版本发布",
        "包含基础图像处理节点",
        "包含文本处理节点",
        "包含工具类节点",
    ],
}

# 导入节点模块
try:
    # 工具类节点
    # 音频节点
    from .nodes.audio.audio_crop_process import \
        NODE_CLASS_MAPPINGS as AUDIO_CROP_MAPPINGS
    from .nodes.audio.audio_crop_process import \
        NODE_DISPLAY_NAME_MAPPINGS as AUDIO_CROP_DISPLAY_MAPPINGS
    from .nodes.image.image_and_mask_preview import \
        NODE_CLASS_MAPPINGS as AND_MASK_PREVIEW_MAPPINGS
    from .nodes.image.image_and_mask_preview import \
        NODE_DISPLAY_NAME_MAPPINGS as AND_MASK_PREVIEW_DISPLAY_MAPPINGS
    # 图像节点
    from .nodes.image.image_concatenate_multi import \
        NODE_CLASS_MAPPINGS as CONCATENATE_MULTI_MAPPINGS
    from .nodes.image.image_concatenate_multi import \
        NODE_DISPLAY_NAME_MAPPINGS as CONCATENATE_MULTI_DISPLAY_MAPPINGS
    from .nodes.image.image_pad_for_outpaint_masked import \
        NODE_CLASS_MAPPINGS as PAD_OUTPAINT_MAPPINGS
    from .nodes.image.image_pad_for_outpaint_masked import \
        NODE_DISPLAY_NAME_MAPPINGS as PAD_OUTPAINT_DISPLAY_MAPPINGS
    from .nodes.image.imitation_hue_node import \
        NODE_CLASS_MAPPINGS as IMITATION_HUE_MAPPINGS
    from .nodes.image.imitation_hue_node import \
        NODE_DISPLAY_NAME_MAPPINGS as IMITATION_HUE_DISPLAY_MAPPINGS
    # 掩码节点
    from .nodes.mask.mask_operations import \
        NODE_CLASS_MAPPINGS as MASK_OPERATIONS_MAPPINGS
    from .nodes.mask.mask_operations import \
        NODE_DISPLAY_NAME_MAPPINGS as MASK_OPERATIONS_DISPLAY_MAPPINGS
    from .nodes.tools.math_expression_node import \
        NODE_CLASS_MAPPINGS as MATH_EXPRESSION_MAPPINGS
    from .nodes.tools.math_expression_node import \
        NODE_DISPLAY_NAME_MAPPINGS as MATH_EXPRESSION_DISPLAY_MAPPINGS
    from .nodes.tools.show_nodes import \
        NODE_CLASS_MAPPINGS as SHOW_NODES_MAPPINGS
    from .nodes.tools.show_nodes import \
        NODE_DISPLAY_NAME_MAPPINGS as SHOW_NODES_DISPLAY_MAPPINGS
    from .nodes.tools.text_concatenate_node import \
        NODE_CLASS_MAPPINGS as TEXT_CONCATENATE_MAPPINGS
    from .nodes.tools.text_concatenate_node import \
        NODE_DISPLAY_NAME_MAPPINGS as TEXT_CONCATENATE_DISPLAY_MAPPINGS
    # 文本框节点
    from .nodes.tools.textbox_node import \
        NODE_CLASS_MAPPINGS as TEXTBOX_MAPPINGS
    from .nodes.tools.textbox_node import \
        NODE_DISPLAY_NAME_MAPPINGS as TEXTBOX_DISPLAY_MAPPINGS

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
    TEXTBOX_MAPPINGS = {}
    TEXTBOX_DISPLAY_MAPPINGS = {}
    TEXT_CONCATENATE_MAPPINGS = {}
    TEXT_CONCATENATE_DISPLAY_MAPPINGS = {}
    MATH_EXPRESSION_MAPPINGS = {}
    MATH_EXPRESSION_DISPLAY_MAPPINGS = {}

# 尝试导入其他可能有依赖的节点
try:
    from .nodes.image.fill_masked_area import \
        NODE_CLASS_MAPPINGS as FILL_MASKED_MAPPINGS
    from .nodes.image.fill_masked_area import \
        NODE_DISPLAY_NAME_MAPPINGS as FILL_MASKED_DISPLAY_MAPPINGS
except ImportError:
    FILL_MASKED_MAPPINGS = {}
    FILL_MASKED_DISPLAY_MAPPINGS = {}

try:
    from .nodes.audio.load_audio import \
        NODE_CLASS_MAPPINGS as LOAD_AUDIO_MAPPINGS
    from .nodes.audio.load_audio import \
        NODE_DISPLAY_NAME_MAPPINGS as LOAD_AUDIO_DISPLAY_MAPPINGS
except ImportError:
    LOAD_AUDIO_MAPPINGS = {}
    LOAD_AUDIO_DISPLAY_MAPPINGS = {}

try:
    from .nodes.image.empty_unit_generator import \
        NODE_CLASS_MAPPINGS as EMPTY_UNIT_MAPPINGS
    from .nodes.image.empty_unit_generator import \
        NODE_DISPLAY_NAME_MAPPINGS as EMPTY_UNIT_DISPLAY
except ImportError:
    EMPTY_UNIT_MAPPINGS = {}
    EMPTY_UNIT_DISPLAY = {}

try:
    from .nodes.image.image_ratio_detector import \
        NODE_CLASS_MAPPINGS as RATIO_MAPPINGS
    from .nodes.image.image_ratio_detector import \
        NODE_DISPLAY_NAME_MAPPINGS as RATIO_DISPLAY
except ImportError:
    RATIO_MAPPINGS = {}
    RATIO_DISPLAY = {}

try:
    from .nodes.image.depth_map_blur import \
        NODE_CLASS_MAPPINGS as DEPTH_BLUR_MAPPINGS
    from .nodes.image.depth_map_blur import \
        NODE_DISPLAY_NAME_MAPPINGS as DEPTH_BLUR_DISPLAY
except ImportError:
    DEPTH_BLUR_MAPPINGS = {}
    DEPTH_BLUR_DISPLAY = {}

try:
    from .nodes.image.image_concatenate import \
        NODE_CLASS_MAPPINGS as CONCAT_MAPPINGS
    from .nodes.image.image_concatenate import \
        NODE_DISPLAY_NAME_MAPPINGS as CONCAT_DISPLAY
except ImportError:
    CONCAT_MAPPINGS = {}
    CONCAT_DISPLAY = {}

try:
    from .nodes.image.image_scale_by_aspect_ratio import \
        NODE_CLASS_MAPPINGS as SCALE_ASPECT_MAPPINGS
    from .nodes.image.image_scale_by_aspect_ratio import \
        NODE_DISPLAY_NAME_MAPPINGS as SCALE_ASPECT_DISPLAY
except ImportError:
    SCALE_ASPECT_MAPPINGS = {}
    SCALE_ASPECT_DISPLAY = {}

try:
    from .nodes.image.image_mask_scale_as import \
        NODE_CLASS_MAPPINGS as MASK_SCALE_MAPPINGS
    from .nodes.image.image_mask_scale_as import \
        NODE_DISPLAY_NAME_MAPPINGS as MASK_SCALE_DISPLAY
except ImportError:
    MASK_SCALE_MAPPINGS = {}
    MASK_SCALE_DISPLAY = {}

try:
    from .nodes.image.image_scale_restore import \
        NODE_CLASS_MAPPINGS as SCALE_RESTORE_MAPPINGS
    from .nodes.image.image_scale_restore import \
        NODE_DISPLAY_NAME_MAPPINGS as SCALE_RESTORE_DISPLAY
except ImportError:
    SCALE_RESTORE_MAPPINGS = {}
    SCALE_RESTORE_DISPLAY = {}

try:
    from .nodes.image.image_remove_alpha import \
        NODE_CLASS_MAPPINGS as REMOVE_ALPHA_MAPPINGS
    from .nodes.image.image_remove_alpha import \
        NODE_DISPLAY_NAME_MAPPINGS as REMOVE_ALPHA_DISPLAY
except ImportError:
    REMOVE_ALPHA_MAPPINGS = {}
    REMOVE_ALPHA_DISPLAY = {}

try:
    from .nodes.image.image_combine_alpha import \
        NODE_CLASS_MAPPINGS as COMBINE_ALPHA_MAPPINGS
    from .nodes.image.image_combine_alpha import \
        NODE_DISPLAY_NAME_MAPPINGS as COMBINE_ALPHA_DISPLAY
except ImportError:
    COMBINE_ALPHA_MAPPINGS = {}
    COMBINE_ALPHA_DISPLAY = {}

try:
    from .nodes.image.check_mask import \
        NODE_CLASS_MAPPINGS as CHECK_MASK_MAPPINGS
    from .nodes.image.check_mask import \
        NODE_DISPLAY_NAME_MAPPINGS as CHECK_MASK_DISPLAY
except ImportError:
    CHECK_MASK_MAPPINGS = {}
    CHECK_MASK_DISPLAY = {}

try:
    from .nodes.tools.purge_vram import \
        NODE_CLASS_MAPPINGS as PURGE_VRAM_MAPPINGS
    from .nodes.tools.purge_vram import \
        NODE_DISPLAY_NAME_MAPPINGS as PURGE_VRAM_DISPLAY
except ImportError:
    PURGE_VRAM_MAPPINGS = {}
    PURGE_VRAM_DISPLAY = {}

try:
    from .nodes.image.crop_by_mask import \
        NODE_CLASS_MAPPINGS as CROP_MASK_MAPPINGS
    from .nodes.image.crop_by_mask import \
        NODE_DISPLAY_NAME_MAPPINGS as CROP_MASK_DISPLAY
except ImportError:
    CROP_MASK_MAPPINGS = {}
    CROP_MASK_DISPLAY = {}

try:
    from .nodes.image.restore_crop_box import \
        NODE_CLASS_MAPPINGS as RESTORE_CROP_MAPPINGS
    from .nodes.image.restore_crop_box import \
        NODE_DISPLAY_NAME_MAPPINGS as RESTORE_CROP_DISPLAY
except ImportError:
    RESTORE_CROP_MAPPINGS = {}
    RESTORE_CROP_DISPLAY = {}

try:
    from .nodes.tools.think_remover_node import \
        NODE_CLASS_MAPPINGS as THINK_REMOVER_MAPPINGS
    from .nodes.tools.think_remover_node import \
        NODE_DISPLAY_NAME_MAPPINGS as THINK_REMOVER_DISPLAY_MAPPINGS
except ImportError as e:
    print(f"导入错误: {e}")
    # ... 其它 except ...
    THINK_REMOVER_MAPPINGS = {}
    THINK_REMOVER_DISPLAY_MAPPINGS = {}

try:
    from .nodes.tools.lora_info import \
        NODE_CLASS_MAPPINGS as LORA_INFO_MAPPINGS
    from .nodes.tools.lora_info import \
        NODE_DISPLAY_NAME_MAPPINGS as LORA_INFO_DISPLAY_MAPPINGS
except ImportError as e:
    print(f"导入错误: {e}")
    LORA_INFO_MAPPINGS = {}
    LORA_INFO_DISPLAY_MAPPINGS = {}

try:
    from .nodes.tools.kontext_presets import \
        NODE_CLASS_MAPPINGS as KONTEXT_PRESETS_MAPPINGS
    from .nodes.tools.kontext_presets import \
        NODE_DISPLAY_NAME_MAPPINGS as KONTEXT_PRESETS_DISPLAY_MAPPINGS
except ImportError as e:
    print(f"导入错误: {e}")
    KONTEXT_PRESETS_MAPPINGS = {}
    KONTEXT_PRESETS_DISPLAY_MAPPINGS = {}

# 合并所有节点映射
NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(EMPTY_UNIT_MAPPINGS)
NODE_CLASS_MAPPINGS.update(RATIO_MAPPINGS)
NODE_CLASS_MAPPINGS.update(DEPTH_BLUR_MAPPINGS)
NODE_CLASS_MAPPINGS.update(CONCAT_MAPPINGS)
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
NODE_CLASS_MAPPINGS.update(MASK_OPERATIONS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(LOAD_AUDIO_MAPPINGS)
NODE_CLASS_MAPPINGS.update(AUDIO_CROP_MAPPINGS)
NODE_CLASS_MAPPINGS.update(TEXTBOX_MAPPINGS)
NODE_CLASS_MAPPINGS.update(TEXT_CONCATENATE_MAPPINGS)
NODE_CLASS_MAPPINGS.update(MATH_EXPRESSION_MAPPINGS)
NODE_CLASS_MAPPINGS.update(THINK_REMOVER_MAPPINGS)
NODE_CLASS_MAPPINGS.update(LORA_INFO_MAPPINGS)
NODE_CLASS_MAPPINGS.update(KONTEXT_PRESETS_MAPPINGS)

# 合并显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(EMPTY_UNIT_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(RATIO_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(DEPTH_BLUR_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(CONCAT_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(CONCATENATE_MULTI_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(PAD_OUTPAINT_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(AND_MASK_PREVIEW_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(IMITATION_HUE_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(SCALE_ASPECT_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(MASK_SCALE_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(SCALE_RESTORE_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(REMOVE_ALPHA_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(COMBINE_ALPHA_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(CHECK_MASK_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(PURGE_VRAM_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(CROP_MASK_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(RESTORE_CROP_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(SHOW_NODES_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(FILL_MASKED_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(LOAD_AUDIO_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(AUDIO_CROP_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(MASK_OPERATIONS_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(TEXTBOX_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(TEXT_CONCATENATE_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(MATH_EXPRESSION_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(THINK_REMOVER_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(LORA_INFO_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(KONTEXT_PRESETS_DISPLAY_MAPPINGS)

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
        "TextboxNode_UTK",
        "TextConcatenate_UTK",
        "MathExpression_UTK",
        "ThinkRemover_UTK",
        "LoraInfo_UTK",
        "LoadKontextPresets_UTK",
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

# 调试：输出所有注册节点的分组属性
if __name__ == "__main__":
    with open("node_category_report.txt", "w", encoding="utf-8") as f:
        f.write("=== UniversalToolkit 节点分组属性清单 ===\n")
        for k, v in NODE_CLASS_MAPPINGS.items():
            cat = getattr(v, "CATEGORY", "无CATEGORY")
            f.write(f"{k}: CATEGORY = {cat}\n")
    print("节点分组清单已导出到 node_category_report.txt")
