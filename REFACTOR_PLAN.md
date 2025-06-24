# ComfyUI Universal Toolkit 重构计划

## 概述

本项目将按照 ComfyUI-LayerStyle 项目的模块化组织方式，将大型节点文件拆分成多个独立的功能模块，提高代码的可维护性和模块化程度。

## 重构目标

1. **模块化组织**：将大型节点文件按功能拆分成独立模块
2. **代码复用**：创建共用工具函数，避免重复代码
3. **易于维护**：每个节点独立文件，便于修改和调试
4. **清晰结构**：按功能分类组织代码结构

## 目录结构

```
nodes/
├── common_utils.py              # 共用工具函数
├── image/                       # 图像处理节点
│   ├── __init__.py
│   ├── empty_unit_generator.py
│   ├── image_ratio_detector.py
│   ├── depth_map_blur.py
│   ├── image_concatenate.py
│   ├── image_concatenate_multi.py
│   ├── image_pad_for_outpaint.py
│   ├── image_and_mask_preview.py
│   ├── imitation_hue_node.py
│   ├── image_scale_by_aspect_ratio.py
│   ├── image_mask_scale_as.py
│   ├── image_scale_restore.py
│   ├── image_remove_alpha.py
│   ├── image_combine_alpha.py
│   ├── check_mask.py
│   ├── purge_vram.py
│   ├── crop_by_mask.py
│   └── restore_crop_box.py
├── tools/                       # 工具类节点
│   ├── __init__.py
│   ├── show_int.py
│   ├── show_float.py
│   ├── show_list.py
│   ├── show_text.py
│   ├── preview_mask.py
│   └── fill_masked_area.py
├── mask/                        # 掩码处理节点
│   ├── __init__.py
│   ├── mask_and.py
│   ├── mask_sub.py
│   └── mask_add.py
├── audio/                       # 音频处理节点
│   ├── __init__.py
│   ├── load_audio_plus_from_path.py
│   └── audio_crop_process.py
├── image_nodes_utk.py          # 原有文件（逐步迁移后删除）
├── tool_nodes_utk.py           # 原有文件（逐步迁移后删除）
├── mask_nodes_utk.py           # 原有文件（逐步迁移后删除）
└── audio_nodes_utk.py          # 原有文件（逐步迁移后删除）
```

## 重构步骤

### 第一阶段：基础架构 ✅
- [x] 创建目录结构
- [x] 创建共用工具函数 `common_utils.py`
- [x] 创建模块初始化文件

### 第二阶段：图像节点迁移 🔄
- [x] EmptyUnitGenerator_UTK
- [x] ImageRatioDetector_UTK  
- [x] DepthMapBlur_UTK
- [x] ImageConcatenate_UTK
- [ ] ImageConcatenateMulti_UTK
- [ ] ImagePadForOutpaintMasked_UTK
- [ ] ImageAndMaskPreview_UTK
- [ ] ImitationHueNode_UTK
- [ ] ImageScaleByAspectRatio_UTK
- [ ] ImageMaskScaleAs_UTK
- [ ] ImageScaleRestore_UTK
- [ ] ImageRemoveAlpha_UTK
- [ ] ImageCombineAlpha_UTK
- [ ] CheckMask_UTK
- [ ] PurgeVRAM_UTK
- [ ] CropByMask_UTK
- [ ] RestoreCropBox_UTK

### 第三阶段：工具节点迁移
- [ ] ShowInt_UTK
- [ ] ShowFloat_UTK
- [ ] ShowList_UTK
- [ ] ShowText_UTK
- [ ] PreviewMask_UTK
- [ ] FillMaskedArea_UTK

### 第四阶段：掩码节点迁移
- [ ] MaskAnd_UTK
- [ ] MaskSub_UTK
- [ ] MaskAdd_UTK

### 第五阶段：音频节点迁移
- [ ] LoadAudioPlusFromPath_UTK
- [ ] AudioCropProcessUTK

### 第六阶段：清理和优化
- [ ] 删除原有大型文件
- [ ] 更新文档
- [ ] 测试所有节点功能
- [ ] 优化导入结构

## 节点文件模板

每个节点文件应遵循以下模板：

```python
"""
节点名称
~~~~~~~~

节点功能描述

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
# 其他必要的导入
from ..common_utils import log, tensor2pil, pil2tensor  # 使用相对导入

class NodeName_UTK:
    CATEGORY = "UniversalToolkit"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # 输入参数定义
            },
            "optional": {
                # 可选参数定义
            }
        }
    
    RETURN_TYPES = ("TYPE1", "TYPE2")
    RETURN_NAMES = ("name1", "name2")
    FUNCTION = "function_name"
    
    def function_name(self, param1, param2, ...):
        # 节点实现逻辑
        return (output1, output2)

# Node mappings
NODE_CLASS_MAPPINGS = {
    "NodeName_UTK": NodeName_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NodeName_UTK": "Node Display Name",
}
```

## 导入结构

主 `__init__.py` 文件应使用以下导入结构：

```python
# 导入新的模块化节点
from .nodes.image.node_file import NODE_CLASS_MAPPINGS as NODE_MAPPINGS
from .nodes.image.node_file import NODE_DISPLAY_NAME_MAPPINGS as NODE_DISPLAY_MAPPINGS

# 合并所有映射
NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(NODE_MAPPINGS)
# ... 其他映射

NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(NODE_DISPLAY_MAPPINGS)
# ... 其他显示名称映射
```

## 优势

1. **模块化**：每个节点独立文件，便于维护
2. **可扩展**：新增节点只需创建新文件
3. **代码复用**：共用函数避免重复代码
4. **清晰结构**：按功能分类，易于理解
5. **冲突减少**：独立文件减少合并冲突

## 注意事项

1. **相对导入**：使用 `from ..common_utils import` 进行相对导入
2. **节点映射**：每个文件都要包含 `NODE_CLASS_MAPPINGS` 和 `NODE_DISPLAY_NAME_MAPPINGS`
3. **文档注释**：每个文件都要有清晰的文档字符串
4. **功能测试**：迁移后要测试节点功能是否正常
5. **渐进迁移**：逐步迁移，保持项目可用性

## 完成状态

- [x] 基础架构搭建
- [x] 共用工具函数创建
- [x] 部分图像节点迁移
- [ ] 完整节点迁移
- [ ] 测试和优化
- [ ] 文档更新 