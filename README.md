# ComfyUI-UniversalToolkit

## 版本

- 当前版本：**v0.1**

## 更新日志

### v0.1
- 项目结构模块化重构，所有节点分为 image_nodes、tool_nodes 两大类，便于维护和扩展。
- 工具类节点（ShowInt、ShowFloat、ShowList、ShowText、PreviewMask）合并为 tool_nodes_utk.py。
- 生成/分析类节点（EmptyUnitGenerator、ImageRatioDetector）合并为 image_nodes_utk.py。
- 删除所有冗余和历史遗留节点文件，保持 nodes/ 目录整洁。
- 统一节点命名后缀（UTK），便于识别。
- 完善空输入兜底逻辑，所有节点均支持安全桥接。

## 简介
本插件为 ComfyUI 提供通用工具节点，当前实现了"空白单元生成"节点，可批量生成指定分辨率、颜色的 image、mask、latent。

## 安装
1. 将本插件文件夹放入 ComfyUI 的 `custom_nodes/` 目录下。
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 节点说明

### Universal Blank Unit
- **output_type**: 选择输出类型（image/mask/latent）
- **ratio_type**: 分辨率类型（standard/social_media）
- **ratio**: 具体分辨率
- **batch**: 批量数
- **image_color**: 颜色（仅 image/mask 有效）

#### 分辨率预设
- **Standard**:
  - 1:1 (512x512)
  - 16:9 (896x512)
  - 4:5 (512x640)
  - 3:2 (768x512)
  - 2:3 (512x768)

- **Social Media**:
  - Instagram Post (1080x1080)
  - Instagram Story (1080x1920)
  - Twitter Post (1600x900)
  - Facebook Cover (820x312)

#### 颜色预设
- White
- Black
- Gray
- Red
- Green
- Blue

## 兼容性
- 结构与 ComfyUI 官方插件规范兼容。
- 支持多分辨率、批量输出，参数面板友好。

## 许可证
MIT