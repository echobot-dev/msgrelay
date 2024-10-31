import abc
from typing import TYPE_CHECKING, Generic, TypeVar, final

from nonebot_plugin_alconna import Target, UniMessage

from ..config import config

if TYPE_CHECKING:
    from nonebot.internal.adapter.bot import Bot
    from nonebot.internal.adapter.message import Message, MessageSegment

    from ..models import RelayEvent

BotT = TypeVar("BotT", bound="Bot")


class MessageFormatter(abc.ABC, Generic[BotT]):
    def __init__(self, bot: "BotT", event: "RelayEvent") -> None:
        self.bot = bot
        self.event = event

    @abc.abstractmethod
    async def format(self) -> "Message | MessageSegment | UniMessage":
        raise NotImplementedError

    @abc.abstractmethod
    async def send_to(self, channel: str) -> None:
        raise NotImplementedError


@final
class FallbackMessageFormatter(MessageFormatter["Bot"]):
    async def format(self) -> "UniMessage":
        return (
            config.msgrelay_header_template.strip().format(**dict(self.event))
            + "\n==========\n"
            + self.event.message
        )

    async def send_to(self, channel: str) -> None:
        message = await self.format()
        await message.send(Target(channel, channel=True), bot=self.bot)
