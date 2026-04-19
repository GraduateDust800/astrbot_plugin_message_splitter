import asyncio
import random

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, MessageChain, filter
from astrbot.api.message_components import Plain
from astrbot.api.provider import ProviderRequest
from astrbot.api.star import Context, Star, register


@register(
    "astrbot_plugin_message_splitter",
    "GraduateDust800",
    "消息分段插件，支持通过 #split# 关键字将消息分段发送",
    "1.0.0",
)
class MessageSplitterPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.context = context
        # 获取插件配置
        self.config = config
        # 分段关键字，默认为 #split#
        self.split_keyword = self.config.get("split_keyword", "#split#")
        # 是否启用功能
        self.enabled = self.config.get("enabled", True)
        # 获取分段延迟范围，默认 [1, 3] 秒
        delay_range = self.config.get("random_delay_range", [1, 3])
        if isinstance(delay_range, list) and len(delay_range) >= 2:
            self.delay_min = float(delay_range[0])
            self.delay_max = float(delay_range[1])
        else:
            self.delay_min = 1.0
            self.delay_max = 3.0

    async def initialize(self):
        """插件初始化"""
        logger.info(
            f"消息分段插件已加载，分段关键字: '{self.split_keyword}', 启用状态: {self.enabled}"
        )

    @filter.on_llm_request()
    async def on_llm_request(
        self, event: AstrMessageEvent, req: ProviderRequest
    ) -> None:
        """在 LLM 请求前，在系统提示词中注入分段指令"""
        if not self.enabled:
            return

        # 在系统提示词中添加分段指令说明
        split_instruction = f"""
如果你需要将回复拆分成多条独立的消息（即多个气泡），你必须**严格按照以下规则**使用关键字 `{self.split_keyword}`：

## 规则
1. 将每条消息的文本内容用 `{self.split_keyword}` 直接连接。
2. **绝对禁止**在 `{self.split_keyword}` 前后添加任何空格、换行符或其它字符（除非这些字符是消息内容本身的一部分）。
3. 整个回复中除了消息文本和分隔关键字外，不得包含任何额外说明或格式标记。

## 正确示例
你想发送两条消息：第一条是 `Hello World`，第二条是 `你好，世界`。  
你的回复必须是：
```
Hello World{self.split_keyword}你好，世界
```

## 错误示例（会导致解析失败）
- ❌ `Hello World {self.split_keyword} 你好，世界`（关键字前后有空格）
- ❌ `Hello World\n{self.split_keyword}\n你好，世界`（关键字前后有换行）

## 重要提醒
- 系统会直接按照 `{self.split_keyword}` 分割你的回复，生成独立的消息气泡。
- 如果你不需要分段发送，请正常回复，不要使用该关键字。
- 请务必严格遵守上述格式，否则消息将无法正确分段。
"""
        req.system_prompt += split_instruction
        logger.debug("已向 LLM 系统提示词中注入分段指令")

    @filter.on_decorating_result()
    async def on_decorating_result(self, event: AstrMessageEvent) -> None:
        """在发送消息前,处理 #split# 关键字,将消息分段发送"""
        if not self.enabled:
            return

        result = event.get_result()
        if result is None or not result.chain:
            return

        # 只处理 LLM 生成的结果
        if not result.is_llm_result():
            return

        # 提取所有文本内容
        full_text = ""
        for component in result.chain:
            if isinstance(component, Plain):
                full_text += component.text

        # 检查是否包含分段关键字
        if self.split_keyword not in full_text:
            return

        logger.debug("检测到分段关键字,开始处理消息分段")

        # 按分段关键字分割消息
        parts = full_text.split(self.split_keyword)
        # 过滤掉空字符串
        parts = [part.strip() for part in parts if part.strip()]

        if len(parts) <= 1:
            return

        # 清空原消息链,避免 AstrBot 后续重复发送
        result.chain.clear()

        # 分段延迟发送
        for i, part in enumerate(parts):
            if i > 0:  # 第一段不延迟,后续段延迟
                delay = random.uniform(self.delay_min, self.delay_max)
                await asyncio.sleep(delay)
            await event.send(MessageChain([Plain(part)]))

        logger.info(f"消息已分割为 {len(parts)} 段并分段发送")

    async def terminate(self):
        """插件卸载时的清理"""
        logger.info("消息分段插件已卸载")
