# ComfyUI-UniversalToolkit

## 版本

- 当前版本：**v1.0.2**

## 更新日志

### v1.0.2
- 删除无用节点 Load Audio Plus Upload (UTK)
- 新增 Audio Crop Process (UTK) 支持原生音频上传
- 修复音频处理相关bug，完善依赖
- 作者信息、邮箱、GitHub 地址全部更新

### v0.1
- 项目结构模块化重构，所有节点分为 image_nodes、tool_nodes 两大类，便于维护和扩展。
- 工具类节点（ShowInt、ShowFloat、ShowList、ShowText、PreviewMask）合并为 tool_nodes_utk.py。
- 生成/分析类节点（EmptyUnitGenerator、ImageRatioDetector）合并为 image_nodes_utk.py。
- 删除所有冗余和历史遗留节点文件，保持 nodes/ 目录整洁。
- 统一节点命名后缀（UTK），便于识别。
- 完善空输入兜底逻辑，所有节点均支持安全桥接。

## 简介
本插件为 ComfyUI 提供通用工具节点，当前实现了丰富的图像与音频处理节点，支持批量生成、裁剪、拼接、分析等多种功能。

## 安装
1. 将本插件文件夹放入 ComfyUI 的 `custom_nodes/` 目录下。
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

### 依赖列表
- Pillow
- numpy
- torch
- librosa
- torchaudio

## 节点说明

### 音频相关节点
- **Load Audio Plus From Path (UTK)**：从本地路径加载音频，支持采样率、声道、裁剪、增益、立体声等参数。
- **Audio Crop Process (UTK)**：对AUDIO类型音频进行裁剪、重采样、增益、声道处理，支持与原生上传节点无缝对接。

### 图像与工具节点
- Empty Unit Generator
- Image Ratio Detector
- Depth Map Blur
- Image Concatenate
- Image Concatenate Multi
- Show Int/Float/List/Text/Mask (UTK)

## 作者信息
- 作者：CyberDickLang
- 邮箱：286878701@qq.com
- GitHub：[https://github.com/whmc76](https://github.com/whmc76)

## 兼容性
- 结构与 ComfyUI 官方插件规范兼容。
- 支持多分辨率、批量输出，参数面板友好。
- 音频节点兼容多格式、原生上传体验。

## 许可证
MIT