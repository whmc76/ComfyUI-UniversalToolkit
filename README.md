# ComfyUI-UniversalToolkit

## 简介
本插件为 ComfyUI 提供多尺寸空白单元（image/mask/latent）生成节点，结构完全遵循 ComfyUI 插件标准。

## 目录结构
```
ComfyUI-UniversalToolkit/
├── main.py
├── image_utils.py
├── requirements.txt
├── README.md
└── nodes/
    ├── __init__.py
    └── image_nodes.py
```

## 安装方法
1. 将本目录放入 ComfyUI 的 custom_nodes 目录下。
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 重启 ComfyUI。

## 节点说明
### 空单元生成器（EmptyUnitGenerator）
- 输入参数：
  - 图像大小：small/medium/large
  - 构图比例：1:1/3:4/16:9
  - 颜色：white/black/gray/red/green/blue
- 输出：
  - image：空白图像
  - mask：空白蒙版
  - latent：空白潜空间

## 依赖
- Pillow
- numpy

## 功能特点
- 模块化设计，各功能独立封装
- 支持多种基础数据类型处理
- 提供直观的节点界面
- 完善的错误处理和参数验证

## 已实现功能
- 多尺寸、多比例空白图像/mask/latent 一键生成
  - 支持 small（sd1.5）、medium（flux/sdxl）、large（high resolution）三种尺寸
  - 支持 1:1、3:4、16:9 等常见比例
  - 支持自定义颜色

## 使用方法
1. 启动 ComfyUI
2. 在节点菜单中找到 "UniversalToolkit" 分类
3. 选择需要的节点并配置参数
4. 连接节点并运行工作流

## 开发计划
- [ ] 添加更多图像处理节点
- [ ] 添加数据类型转换节点
- [ ] 添加逻辑处理节点
- [ ] 优化节点界面
- [ ] 添加更多示例工作流

## 贡献指南
欢迎提交 Issue 和 Pull Request！

## 许可证
MIT License