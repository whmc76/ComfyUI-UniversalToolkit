# 视频提示词生成器 (Video Prompt Generator)

## 简介

视频提示词生成器是一个专为 ComfyUI 设计的自定义节点插件，提供强大的视频提示词生成功能。该插件支持中英文双语界面，帮助用户快速构建专业的电影化提示词。

## 原作者信息

- **原作者**: flybirdxx
- **项目地址**: https://github.com/flybirdxx/ComfyUI_Prompt_Helper
- **许可证**: MIT License

## 功能特点

* 🎬 **专业电影化提示词生成** - 构建高质量的视频生成提示词
* 🌐 **双语支持** - 自动检测系统语言，支持中文和英文界面
* 📋 **14个专业分类** - 覆盖电影制作的各个方面
* 🎯 **三种格式输出** - 专业、简单、详细三种提示词格式
* 🔧 **高度可定制** - 丰富的配置选项和预设
* 📚 **内置示例** - 包含多个使用示例和最佳实践

## 分类选项

插件提供以下14个专业分类：

1. **镜头大小 / Shot Size** - 全景、中景、特写等
2. **灯光类型 / Lighting Type** - 自然光、戏剧化灯光、柔光等
3. **光源 / Light Source** - 阳光、月光、火光等
4. **色调 / Color Tone** - 暖色调、冷色调、高对比度等
5. **摄像机角度 / Camera Angle** - 平视、仰视、俯视等
6. **镜头 / Lens** - 广角、人像、长焦等
7. **基础摄像机运动 / Basic Camera Movement** - 静态、平移、缩放等
8. **高级摄像机运动 / Advanced Camera Movement** - 推轨、斯坦尼康、航拍等
9. **时间 / Time of Day** - 黎明、黄昏、夜晚等
10. **运动 / Motion** - 慢动作、快动作、正常速度等
11. **视觉效果 / Visual Effects** - 镜头光晕、雨滴、雾气等
12. **视觉风格 / Visual Style** - 电影风格、纪录片、动作等
13. **角色情感 / Character Emotion** - 开心、悲伤、紧张等
14. **构图 / Composition** - 三分法、对称、非对称等

## 使用方法

1. **启动 ComfyUI** - 插件会自动加载并检测系统语言
2. **添加节点** - 在节点菜单中找到 "🎬 视频提示词生成器" 或 "🎬 Video Prompt Generator"
3. **配置参数** - 从各个分类中选择所需的选项
4. **生成提示词** - 插件会自动组合生成专业的提示词

### 示例工作流

```
用户输入: "一个战士在战场上奔跑"
配置选项:
- 镜头大小: 中景
- 灯光类型: 戏剧化灯光
- 色调: 高对比度
- 摄像机角度: 仰视角度
- 提示词格式: 专业

输出结果: "一个战士在战场上奔跑，中景，戏剧化灯光，高对比度，仰视角度，专业电影质量，高细节，4K分辨率"
```

## 文件结构

```
nodes/tools/
├── prompt_helper.py              # 主要功能代码
├── prompt_presets.json           # 预设配置文件
├── prompt_ui_labels.json         # 界面标签文件
└── README_prompt_helper.md       # 说明文档
```

## 配置文件

* **prompt_presets.json** - 包含所有分类的预设选项
* **prompt_ui_labels.json** - 定义界面标签的多语言文本

## 自定义配置

您可以通过编辑 JSON 配置文件来自定义选项：

1. 编辑 `prompt_presets.json` 添加新的预设选项
2. 修改 `prompt_ui_labels.json` 更新界面文本

## 兼容性

* **ComfyUI** - 支持最新版本的 ComfyUI
* **Python** - 需要 Python 3.7+
* **操作系统** - 支持 Windows、macOS、Linux

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 致谢

* 感谢 flybirdxx 提供的优秀视频提示词生成工具
* 感谢 ComfyUI 提供的优秀平台

---

## 更新日志

### v1.0.0 (集成版本)

* 初始集成到 ComfyUI-UniversalToolkit
* 支持14个专业分类
* 双语界面支持
* 三种提示词格式
* 保持原作者信息和 MIT 协议 