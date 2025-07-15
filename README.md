# ComfyUI-UniversalToolkit

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/whmc76/ComfyUI-UniversalToolkit)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-v3+-orange.svg)](https://github.com/comfyanonymous/ComfyUI)

一个功能全面的ComfyUI工具包，提供丰富的图像处理、音频处理、掩码操作和实用工具节点，支持批量处理、智能分析、色彩迁移等多种高级功能。

## 🌟 主要特性

- **🎨 图像处理**：色彩迁移、图像拼接、尺寸调整、深度图模糊等
- **🎵 音频处理**：音频加载、裁剪、重采样、增益调节等
- **🎭 掩码操作**：掩码运算、填充、裁剪、预览等
- **🛠️ 实用工具**：数学表达式、文本处理、显存清理、预设加载等
- **📱 智能预设**：27种Kontext VLM系统预设，支持动态场景描述
- **🔧 模块化设计**：按功能分类，易于维护和扩展
- **⚡ 高性能**：支持批量处理，优化内存使用

## 📦 安装

### 方法一：通过ComfyUI-Manager安装（推荐）
1. 在ComfyUI中打开ComfyUI-Manager
2. 搜索 "ComfyUI-UniversalToolkit"
3. 点击安装

### 方法二：手动安装
1. 将本插件文件夹放入ComfyUI的 `custom_nodes/` 目录下
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 依赖要求
```
Pillow
numpy
torch
librosa
torchaudio
opencv-python
scipy
tqdm
```

## 🎯 节点功能详解

### 🎨 图像处理节点

#### 基础图像处理
- **EmptyUnitGenerator_UTK**：生成指定尺寸的空白图像、掩码和潜在空间
- **ImageRatioDetector_UTK**：检测图像宽高比，支持多种比例格式
- **ImageConcatenate_UTK**：水平或垂直拼接两张图像
- **ImageConcatenateMulti_UTK**：智能拼接多张图像，支持2-4图自动布局

#### 图像变换与调整
- **ImageScaleByAspectRatio_UTK**：按指定宽高比缩放图像
- **ImageMaskScaleAs_UTK**：按参考图像尺寸缩放图像
- **ImageScaleRestore_UTK**：将图像恢复到原始尺寸
- **ImageRemoveAlpha_UTK**：移除图像的Alpha通道
- **ImageCombineAlpha_UTK**：合并Alpha通道到图像

#### 高级图像处理
- **ImitationHueNode_UTK**：图像色彩迁移，支持皮肤保护和区域处理
- **DepthMapBlur_UTK**：基于深度图的智能模糊，模拟景深效果
- **ImagePadForOutpaintMasked_UTK**：外绘扩展，支持像素和百分比模式
- **ImageAndMaskPreview_UTK**：图像和掩码预览，支持叠加和并排显示

#### 掩码相关图像处理
- **CropByMask_UTK**：基于掩码智能裁剪，支持多种检测模式
- **RestoreCropBox_UTK**：恢复裁剪框到原始背景
- **FillMaskedArea_UTK**：掩码区域填充，支持多种算法
- **CheckMask_UTK**：检查掩码有效性

### 🎵 音频处理节点

- **LoadAudioPlusFromPath_UTK**：从本地路径加载音频，支持采样率、声道、裁剪、增益等参数
- **AudioCropProcess_UTK**：音频裁剪处理，支持重采样、增益、声道处理，与原生上传节点无缝对接

### 🎭 掩码操作节点

- **MaskAnd_UTK**：掩码与运算
- **MaskSub_UTK**：掩码减法运算
- **MaskAdd_UTK**：掩码加法运算

### 🛠️ 工具节点

#### 显示与预览
- **Show_UTK**：通用显示节点，支持所有数据类型预览

#### 文本处理
- **TextboxNode_UTK**：多行文本输入框
- **TextConcatenate_UTK**：文本拼接，支持自定义分隔符
- **ThinkRemover_UTK**：分离文本中的思考内容

#### 数学与逻辑
- **MathExpression_UTK**：数学表达式计算，支持复杂公式和函数

#### 系统工具
- **PurgeVRAM_UTK**：显存清理，支持选择性清理缓存和模型
- **LoraInfo_UTK**：LoRA信息查询，获取CivitAI触发词、示例提示词、基础模型等信息

#### 预设系统
- **LoadKontextPresets_UTK**：Kontext VLM系统预设，包含27种专业图像变换预设
  - 情境深度融合、无痕融合、场景传送
  - 移动镜头、重新布光、专业产品图
  - 画面缩放、图像上色、电影海报
  - 卡通漫画化、移除文字、更换发型
  - 肌肉猛男化、清空家具、室内设计
  - 季节变换、时光旅人、材质置换
  - 微缩世界、幻想领域、衣橱改造
  - 艺术风格模仿、蓝图视角、添加倒影
  - 像素艺术、铅笔手绘、油画风格

## 🚀 使用示例

### 图像拼接示例
```
ImageConcatenate_UTK
├── 输入：两张图像
├── 模式：水平/垂直拼接
├── 输出：拼接后的图像
```

### 色彩迁移示例
```
ImitationHueNode_UTK
├── 输入：源图像 + 目标图像
├── 参数：皮肤保护、亮度调节、对比度调节
├── 输出：色彩迁移后的图像
```

### 音频处理示例
```
AudioCropProcess_UTK
├── 输入：音频文件
├── 参数：裁剪时间、重采样率、增益调节
├── 输出：处理后的音频
```

## 📋 版本历史

### v1.2.0 (最新)
- 全面更新README文档，提供详细的功能介绍和使用指南
- 优化项目结构和文档组织
- 完善节点功能说明和分类
- 更新版本推送代码，确保发布流程顺畅
- 提升项目整体文档质量和用户体验

### v1.1.9
- 升级LoadKontextPresets_UTK节点功能
- 新增用户提示输入参数，支持动态场景描述
- 为所有27个预设添加$user_prompt$占位符
- 智能占位符替换，提升VLM模型生成指令的针对性

### v1.1.8
- 新增LoadKontextPresets_UTK节点
- 提供25种图像变换预设
- 支持情境深度融合、场景传送等多种预设

### v1.1.7
- 新增ThinkRemover_UTK节点
- 支持分离文本中的思考内容

### v1.1.6
- 新增TextboxNode_UTK节点
- 支持在图像上添加自定义样式文本框

### v1.1.5
- 优化ImitationHueNode_UTK节点的色彩迁移算法
- 改进皮肤保护功能，提高肤色保持效果

### v1.1.4
- 版本更新发布，支持ComfyUI-Manager和Registry获取
- 确保与ComfyUI v3完全兼容

### v1.1.3
- 修复PurgeVRAM_UTK节点类型不匹配问题
- 修复CheckMask_UTK节点NoneType错误
- 完成模块化重构

### v1.1.2
- 修复DepthMapBlur_UTK节点kernel size类型问题
- 修正EmptyUnitGenerator_UTK输出shape
- 完善节点导入路径

### v1.1.1
- 项目重构，按功能分类组织代码
- 新增多个图像处理节点
- 提高代码可维护性

### v1.1.0
- 新增CropByMask_UTK和RestoreCropBox_UTK节点
- 支持掩码裁剪和恢复功能

### v1.0.9
- 新增PurgeVRAM_UTK节点
- 支持显存清理功能

### v1.0.8
- 新增ImitationHueNode_UTK节点
- 支持图像色彩迁移功能

### v1.0.7
- 改进ImagePadForOutpaintMasked节点
- 新增数据模式和背景颜色选项

### v1.0.6
- 新增ImageAndMaskPreview_UTK节点
- 支持图像和掩码同时预览

### v1.0.5
- 新增ImagePadForOutpaintMasked_UTK节点
- 支持外绘时扩展图像尺寸

### v1.0.4
- 新增FillMaskedArea_UTK节点
- 支持三种填充模式

### v1.0.3
- 新增掩码像素级运算节点
- 修正节点注册与显示名风格

### v1.0.2
- 删除无用节点
- 新增AudioCropProcess节点
- 修复音频处理相关bug

### v1.0.1
- 改进图像拼接节点
- 添加图像尺寸匹配和最大尺寸限制

### v1.0.0
- 初始版本发布
- 包含基础图像处理、文本处理、工具类节点

## 🔧 兼容性

- **ComfyUI版本**：v1.0.0+
- **Python版本**：3.8+
- **操作系统**：Windows, macOS, Linux
- **GPU支持**：NVIDIA CUDA (推荐)

## 📁 项目结构

```
ComfyUI-UniversalToolkit/
├── nodes/
│   ├── image/           # 图像处理节点
│   ├── audio/           # 音频处理节点
│   ├── mask/            # 掩码操作节点
│   ├── tools/           # 工具节点
│   └── image_utils.py   # 图像工具函数
├── web/                 # Web界面扩展
├── reference_code/      # 参考代码
├── __init__.py          # 主入口文件
├── requirements.txt     # 依赖列表
├── pyproject.toml       # 项目配置
└── README.md           # 说明文档
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

### 开发规范
- 遵循PEP8代码风格
- 节点命名统一加`_UTK`后缀
- 所有节点必须通过测试验证
- 新增功能需更新文档

## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件

## 👨‍💻 作者信息

- **作者**：CyberDickLang
- **邮箱**：286878701@qq.com
- **GitHub**：[https://github.com/whmc76](https://github.com/whmc76)

## 🙏 致谢

感谢以下项目的开源贡献：
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - 优秀的AI图像生成框架
- [ComfyUI-LayerStyle](https://github.com/your-repo) - 模块化设计参考
- [ComfyUI-MingNodes](https://github.com/your-repo) - 色彩迁移算法参考
- [Kontext](https://github.com/your-repo) - VLM预设系统
- [kjnodes](https://github.com/kijai/ComfyUI-KJNodes) - 节点开发参考和灵感
- [audio-separation-nodes-comfyui](https://github.com/christian-byrne/audio-separation-nodes-comfyui) - 音频处理节点参考

---

⭐ 如果这个项目对您有帮助，请给我们一个Star！ 