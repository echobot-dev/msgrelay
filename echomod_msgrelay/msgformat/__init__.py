from typing import TYPE_CHECKING

from ._base import FallbackMessageFormatter, MessageFormatter
from .discord import DiscordMessageFormatter

if TYPE_CHECKING:
    from nonebot.internal.adapter import Bot

    from ..models import RelayEvent

ADAPTER_MAPPING: dict[str, type[MessageFormatter]] = {
    "Discord": DiscordMessageFormatter,
}


def create_formatter(bot: "Bot", event: "RelayEvent") -> MessageFormatter:
    return ADAPTER_MAPPING.get(bot.type, FallbackMessageFormatter)(bot, event)


__all__ = ("create_formatter",)
