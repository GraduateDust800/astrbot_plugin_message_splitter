# 消息分段插件 (Message Splitter Plugin)

## 目录结构

```
astrbot_plugin_message_splitter/
├── main.py              # 插件主文件，包含核心逻辑
├── metadata.yaml        # 插件元数据（名称、版本、作者等）
├── _conf_schema.json    # 配置 schema 定义文件
├── README.md           # 插件说明文档
├── USAGE.md            # 详细使用指南
└── LICENSE             # 许可证文件（如果需要）
```

## 文件说明

### main.py
插件的核心实现文件，包含：
- `MessageSplitterPlugin` 类：插件主类
- `on_llm_request()` 方法：在 LLM 请求前注入分段指令
- `on_decorating_result()` 方法：在消息发送前处理分段关键字

### metadata.yaml
插件的元数据信息：
```yaml
name: astrbot_plugin_message_splitter
display_name: 消息分段插件
desc: 通过 #split# 关键字将 LLM 回复分段发送，每个分段作为独立消息气泡
version: v1.0.0
author: GraduateDust800
repo: https://github.com/GraduateDust800/astrbot_plugin_message_splitter
```

### _conf_schema.json
配置 schema 定义文件，AstrBot 会根据此文件生成配置界面：
```json
{
  "split_keyword": {
    "type": "string",
    "description": "消息分段关键字",
    "hint": "LLM 使用此关键字来分段发送消息",
    "default": "#split#"
  },
  "enabled": {
    "type": "bool",
    "description": "启用消息分段功能",
    "hint": "开启后自动处理分段关键字",
    "default": true
  }
}
```

### README.md
插件的说明文档，包含：
- 功能特性介绍
- 安装方法
- 配置说明
- 使用示例
- 注意事项

### USAGE.md
详细的使用指南，包含：
- 快速开始步骤
- 各种使用场景示例
- 高级配置选项
- 故障排除指南
- 技术细节说明

## 快速安装

1. 将整个文件夹复制到 AstrBot 的插件目录：
   ```
   data/plugins/astrbot_plugin_message_splitter/
   ```

2. 重启 AstrBot 或在 WebUI 中重载插件

3. 开始使用！LLM 现在可以使用 `#split#` 关键字来分段发送消息

## 核心功能

### 1. 智能分段
通过可配置的关键字（默认 `#split#`）实现消息分段

### 2. 上下文注入
自动在 LLM 系统提示词中注入分段指令，指导 LLM 正确使用分段功能

### 3. 可配置
支持自定义分段关键字和启用/禁用功能

### 4. 即插即用
无需额外配置，安装后即可使用

## 技术架构

### 事件钩子

1. **on_llm_request** (`EventType.OnLLMRequestEvent`)
   - 时机：在 LLM 请求前触发
   - 功能：在系统提示词中注入分段指令

2. **on_decorating_result** (`EventType.OnDecoratingResultEvent`)
   - 时机：在消息发送前触发
   - 功能：检测并处理分段关键字

### 消息处理流程

```
用户消息 → LLM 请求（注入分段指令） → LLM 回复
     ↓
检测分段关键字 → 分割消息 → 重构消息链 → 发送消息
```

### 消息链结构

分段后的消息链：
```python
[
    Plain("第一部分"),
    Plain("\n"),
    Plain("第二部分"),
    Plain("\n"),
    Plain("第三部分")
]
```

## 配置选项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `split_keyword` | string | `#split#` | 分段关键字 |
| `enabled` | boolean | `true` | 是否启用分段功能 |

## 测试

插件包含完整的单元测试，运行测试：

```bash
uv run pytest tests/test_message_splitter.py -v
```

## 开发信息

- **作者**：GraduateDust800
- **版本**：v1.0.0
- **许可证**：MIT
- **兼容版本**：AstrBot v4.x

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

1. 克隆仓库
2. 安装依赖：`uv sync`
3. 运行测试：`uv run pytest tests/test_message_splitter.py -v`
4. 代码格式化：`uv run ruff format .`
5. 代码检查：`uv run ruff check .`

## 更新日志

### v1.0.0 (2026-04-19)

- ✨ 初始版本发布
- ✨ 支持通过 `#split#` 关键字分段消息
- ✨ 自动在系统提示词中注入分段指令
- ✨ 支持自定义分段关键字
- ✨ 完整的测试覆盖
- ✨ 详细的文档
