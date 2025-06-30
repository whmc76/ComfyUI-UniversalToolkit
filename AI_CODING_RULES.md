# AI 协作编程规则（AI Coding Rules）

## 总则
- 所有代码必须遵循本项目的风格和结构。
- 不允许自动拉取、克隆、下载外部项目或依赖，除非用户明确要求。
- 只允许在本地已有文件和依赖范围内进行开发和修改。
- 遵循用户指令，优先满足用户需求。
- 保持代码风格、接口、参数、行为与用户项目一致。

## 参考项目代码的强制要求
- 当用户指定参考某个项目（如GitHub仓库、第三方节点等）时，**必须严格复制该项目的相关代码实现**，保持原有逻辑、参数、shape处理、异常处理等完全一致。
- **不得自行"优化"或"简化"实现，不得随意更改shape、类型、参数声明、默认值、边界处理等。**
- 如需适配本地环境，仅允许在不影响核心逻辑的前提下做最小必要的兼容性调整，并需明确告知用户。
- 如遇到与主线ComfyUI不兼容的情况，优先保持参考项目的原始行为，并向用户说明。

## 代码风格
- 遵循 PEP8 代码风格。
- 类、函数、变量命名需简洁明了，使用英文。
- 关键逻辑必须有中英文注释。
- 遵循PEP8及项目原有风格。
- 变量、函数、类命名与参考项目保持一致。

## 节点开发
- 节点参数需有默认值、类型、范围说明。
- 输入输出类型必须与 ComfyUI 规范一致。
- **所有节点的输入和输出shape、类型、参数名、返回名，必须严格遵循ComfyUI官方节点开发规范，保证与ComfyUI原生节点和其他插件节点100%兼容。不得自定义非标准shape或类型。**
- 新增节点需在 `__init__.py` 注册，并补充到文档。
- 节点参数、UI、输出类型、行为与参考项目完全一致。
- 不得随意增删参数或更改默认值。

## 依赖管理
- 避免严格的依赖版本限制。除非有兼容性或安全性要求，否则建议只指定主版本或不指定版本。
- 依赖声明与参考项目一致，不随意更改依赖版本。
- 禁止跨文件导入自定义工具函数（如 color_utils、common_utils），所有通用函数应直接内置到节点文件。
- 如需参考第三方实现，务必将原始代码存放于 `reference_code/`，主线代码只保留必要部分。

## 变更限制
- 不允许删除或覆盖用户已有的自定义节点。
- 不允许修改依赖包的源码。
- 不允许自动生成或修改测试数据文件，除非用户要求。
- 仅在用户明确要求时才可对参考项目代码做自定义扩展或优化。
- 所有变更需在注释中注明原因。

## 其它
- 如需引入第三方实现，必须先征得用户同意。
- 任何自动化操作前，需先说明理由和影响。

## 目录结构与分层（UniversalToolkit 专项）

```
nodes/
├── image/         # 图像处理相关节点
│   ├── imitation_hue_node.py
│   ├── image_concatenate.py
│   └── ...（其他 image 节点）
├── tools/         # 工具类节点
│   ├── purge_vram.py
│   ├── fill_masked_area.py
│   └── ...（其他工具节点）
reference_code/    # 官方/第三方参考实现存放目录
```
- 图像处理节点统一分类为 `UniversalToolkit/Image`
- 工具节点统一分类为 `Tools`

## 节点注册与命名规范
- 每个节点文件需包含如下注册方式：
  ```python
  NODE_CLASS_MAPPINGS = {
      "节点类名": 节点类,
  }
  NODE_DISPLAY_NAME_MAPPINGS = {
      "节点类名": "节点显示名",
  }
  ```
- 节点类名建议统一加 `_UTK` 后缀，显示名加 `(UTK)`。

## 测试与验证
- 所有节点必须能通过 `test_nodes.py` 脚本批量导入测试。
- 新增节点或重构后，需补充测试用例，确保无依赖缺失和导入错误。

## 参考实现与同步
- 如需同步第三方（如 MingNodes）实现，务必：
  - 保持参数、输入输出、算法与官方一致
  - 分类、注册方式可按 UniversalToolkit 规范适配
  - 参考代码完整保留在 `reference_code/`，主线代码只保留实际用到部分

## 其它约定
- 禁止使用已废弃的 `common_utils.py`、`color_utils.py` 等历史文件。
- 所有节点文件需自包含所需的工具函数，避免循环依赖和导入混乱。
- 重要变更需在文件头部注明来源、变更说明和版权信息。

# ComfyUI-UniversalToolkit 开发规范（AI_CODING_RULES）

## 2024-07-13 重要改进与规则

### 1. 节点注册与导入（ComfyUI v3官方规范）
- 每个节点文件只导出自己的 `NODE_CLASS_MAPPINGS` 和 `NODE_DISPLAY_NAME_MAPPINGS`。
- `__init__.py` 必须静态导入所有节点注册字典，禁止动态try/except导入和动态合并。
- 只导出 `NODE_CLASS_MAPPINGS`、`NODE_DISPLAY_NAME_MAPPINGS`，对齐官方插件加载机制。
- 节点注册顺序清晰，所有节点都必须被静态合并进主注册字典。

### 2. 节点分组与命名
- 每个节点类必须有唯一且规范的 `CATEGORY` 属性，分组如 `UniversalToolkit/Image`、`UniversalToolkit/Mask`、`UniversalToolkit/Audio`、`UniversalToolkit/Tools`。
- 节点类名、注册名、显示名必须唯一，全部带 `_UTK` 后缀，禁止与原生节点或其它插件重名。
- 节点显示名统一加 `(UTK)` 后缀，保证界面分组风格一致。

### 3. pyproject.toml 规范
- 必须包含 `[project]` 和 `[tool.comfy]` 两大段，字段严格对齐官方文档：
  - `name`、`description`、`version`、`license`、`dependencies`、`Repository`
  - `[tool.comfy]` 下 `PublisherId`、`DisplayName`、`Icon` 必填
- `PublisherId` 必须与Registry注册一致，`DisplayName`为插件在ComfyUI-Manager/Registry中的显示名

### 4. 目录结构与分层
- 按功能分为 `nodes/image`、`nodes/mask`、`nodes/audio`、`nodes/tools` 四大目录，每个节点独立py文件
- 禁止使用绝对导入和跨目录utils模块，所有依赖应在本插件目录下

### 5. 节点输入输出与兼容性
- 所有节点输入输出shape、类型、参数名、返回名必须严格遵循ComfyUI官方节点开发规范
- 禁止随意更改节点实现、参数、shape，所有节点必须与ComfyUI原生节点和其它插件100%兼容
- 任何涉及shape、类型、参数的修正，必须优先保证与ComfyUI主程序和主流插件生态兼容

### 6. 其它重要约定
- 禁止在`__init__.py`中做复杂逻辑或动态注册，推荐静态声明所有节点映射
- 禁止用旧版的`register_node`、`register_nodes`等动态注册API
- 所有节点分组、命名、注册、导入、依赖、pyproject.toml等必须随时对齐ComfyUI官方最新规范

---

**本规范为ComfyUI-UniversalToolkit插件开发的最高准则，所有贡献者和维护者必须严格遵守。**

（如有新规范或官方更新，须第一时间同步修订本文件） 