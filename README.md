# 消息分段插件 (Message Splitter Plugin)

一个 AstrBot 插件，允许 LLM 通过特定的关键字将回复内容分段发送，每段消息会作为独立的气泡显示。

## 功能特性

- 🎯 **智能分段**: 通过可配置的关键字（默认 `#split#`）实现消息分段
- 📝 **上下文注入**: 自动在 LLM 系统提示词中注入分段指令，指导 LLM 正确使用分段功能
- ⚙️ **可配置**: 支持自定义分段关键字和启用/禁用功能
- 🔌 **即插即用**: 无需额外配置，安装后即可使用

## 安装方式

### 方法一：通过 AstrBot WebUI 安装

1. 打开 AstrBot 仪表盘
2. 进入插件市场
3. 搜索 `astrbot_plugin_message_splitter`
4. 点击安装

### 方法二：手动安装

1. 克隆或下载本仓库到 AstrBot 的插件目录：

```bash
cd data/plugins
git clone https://github.com/GraduateDust800/astrbot_plugin_message_splitter.git
```

2. 重启 AstrBot 或在 WebUI 中重载插件

## 配置说明

插件配置文件位于 `data/plugins/astrbot_plugin_message_splitter/config.json`：

```json
{
  "split_keyword": "#split#",
  "enabled": true
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `split_keyword` | string | `#split#` | 用于分段的关键词 |
| `enabled` | boolean | `true` | 是否启用分段功能 |

## 使用示例

### 基本用法

当 LLM 在回复中使用分段关键字时，消息会被自动分割：

**LLM 回复内容：**
```
Hello World
#split#
你好，世界
```

**实际发送效果：**
- 第一个气泡：`Hello World`
- 第二个气泡：`你好，世界`

### 多段消息

可以分段发送多条消息：

**LLM 回复内容：**
```
第一条消息
#split#
第二条消息
#split#
第三条消息
```

**实际发送效果：**
- 第一个气泡：`第一条消息`
- 第二个气泡：`第二条消息`
- 第三个气泡：`第三条消息`

## 工作原理

1. **LLM 请求阶段** (`on_llm_request`):
   - 插件在系统提示词中注入分段指令
   - 告知 LLM 如何使用分段关键字

2. **消息发送前** (`on_decorating_result`):
   - 检测 LLM 回复中是否包含分段关键字
   - 如果包含，将消息按关键字分割
   - 将分割后的各部分重新组织到消息链中

## 自定义分段关键字

如果你想使用其他关键字（比如 `---` 或 `[[split]]`），只需修改配置文件：

```json
{
  "split_keyword": "---",
  "enabled": true
}
```

然后重载插件即可生效。

## 注意事项

- ⚠️ 分段关键字区分大小写
- ⚠️ 只有 LLM 生成的消息会被处理，普通指令回复不会受影响
- ⚠️ 分段后的消息会按顺序发送，但在某些平台可能仍显示为一条消息（取决于平台适配器实现）
- ⚠️ 如果 LLM 在关键字前后添加了多余空格，插件会自动处理

## 兼容性

- ✅ AstrBot v4.x
- ✅ 所有支持文本消息的平台
- ✅ 与其他插件兼容

## 开发信息

- **作者**: GraduateDust800
- **版本**: v1.0.0
- **许可证**: MIT

## 问题反馈

如果遇到问题或有建议，请提交 Issue 或 Pull Request。

## 更新日志

### v1.0.0

- ✨ 初始版本发布
- ✨ 支持通过 `#split#` 关键字分段消息
- ✨ 自动在系统提示词中注入分段指令
- ✨ 支持自定义分段关键字
