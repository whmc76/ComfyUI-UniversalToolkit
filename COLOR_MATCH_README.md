# Color Match (UTK) 节点使用说明

## 概述

Color Match (UTK) 节点是从 kjnodes 项目移植过来的颜色匹配功能，现在已成功集成到 ComfyUI Universal Toolkit 的 image 分类中。该节点能够将参考图像的颜色特征转移到目标图像上，非常适合用于自动色彩分级、照片后期处理和影片色彩统一等场景。

## 功能特点

- **多种颜色匹配算法**：支持 6 种不同的颜色匹配方法
- **强度控制**：可调节颜色匹配的强度（0.0-10.0）
- **批处理支持**：支持批量图像处理
- **多线程优化**：可选择开启多线程以提升处理速度
- **高质量结果**：基于学术研究的先进算法

## 安装要求

在使用此节点之前，需要安装 `color-matcher` 依赖库：

```bash
pip install color-matcher
```

## 节点参数

### 必需参数
- **image_ref**：参考图像，作为颜色匹配的目标样式
- **image_target**：目标图像，需要被调整颜色的图像
- **method**：颜色匹配方法，可选择：
  - `mkl`：Monge-Kantorovich Linearization（默认）
  - `hm`：Histogram Matching
  - `reinhard`：Reinhard et al. method
  - `mvgd`：Multi-Variate Gaussian Distribution
  - `hm-mvgd-hm`：Histogram Matching + MVGD + Histogram Matching
  - `hm-mkl-hm`：Histogram Matching + MKL + Histogram Matching

### 可选参数
- **strength**：颜色匹配强度（默认：1.0，范围：0.0-10.0）
- **multithread**：是否启用多线程处理（默认：True）

## 使用方法

1. 在 ComfyUI 中，在节点菜单中找到 `UTK/image` 分类
2. 添加 `Color Match (UTK)` 节点
3. 连接参考图像到 `image_ref` 输入
4. 连接目标图像到 `image_target` 输入
5. 选择合适的颜色匹配方法
6. 调整强度参数（可选）
7. 运行工作流

## 算法说明

### 推荐的方法选择

- **mkl**：适合大多数场景的通用方法，效果平衡
- **hm-mvgd-hm**：复合方法，通常能获得最佳效果
- **reinhard**：经典方法，适合艺术风格转换
- **hm**：简单快速，适合基本的色彩调整

### 性能优化

- 对于单张图像，建议关闭多线程
- 对于批量处理，建议开启多线程以提升速度
- 较低的强度值（0.3-0.7）通常能产生更自然的效果

## 技术参考

该节点基于以下学术研究：
- Reinhard et al. 的颜色转移方法
- Pitie et al. 提出的 Monge-Kantorovich Linearization
- Multi-Variate Gaussian Distribution 转移的解析解

项目参考：https://github.com/hahnec/color-matcher/

## 故障排除

### 常见问题

1. **导入错误**：确保已安装 `color-matcher` 库
2. **处理失败**：检查输入图像是否为有效的张量格式
3. **内存不足**：对于大图像，可以尝试关闭多线程或降低批处理大小

### 错误处理

节点包含完善的错误处理机制：
- 如果颜色匹配失败，会自动返回原始图像
- 所有错误信息会在控制台中显示
- 支持优雅降级，确保工作流不会中断

## 更新日志

- **v1.0**：初始版本，从 kjnodes 移植并集成到 UTK
- 支持所有原始功能和参数
- 添加了详细的文档和错误处理
- 优化了代码结构和性能

---

*此节点是 ComfyUI Universal Toolkit 的一部分，致力于为 ComfyUI 用户提供更丰富的图像处理功能。*
