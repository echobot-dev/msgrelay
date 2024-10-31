from datetime import datetime
from typing import TYPE_CHECKING, Literal

from nonebot_plugin_alconna import UniMessage
from pydantic import AwareDatetime, BaseModel, ConfigDict

from .msgformat import create_formatter

if TYPE_CHECKING:
    from nonebot.internal.adapter import Bot
    from nonebot_plugin_uninfo import Session as UninfoSession


class User(BaseModel):
    id: str
    name: str
    avatar: str | None = None


class Channel(BaseModel):
    id: str
    name: str
    type: str
    platform: str
    avatar: str | None = None


class RelaySession(BaseModel):
    adapter: str
    sender: User
    channel: Channel

    @classmethod
    def build(cls, session: "UninfoSession") -> "RelaySession":
        return cls(
            adapter=session.adapter,
            sender=User(
                id=session.user.id,
                name=(
                    (session.member.nick if session.member else session.user.nick)
                    or session.user.name
                    or "<N/A>"
                ),
                avatar=session.user.avatar,
            ),
            channel=Channel(
                id=session.scene.id,
                name=session.scene.name or "<N/A>",
                type=session.scene.type.name,
                platform=session.scope,
                avatar=session.scene.avatar,
            ),
        )


class RelayEvent(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    session: RelaySession
    message: UniMessage
    op_type: Literal["create", "update", "delete"]
    op_time: AwareDatetime

    async def send_message(self, bot: "Bot", channel: str) -> None:
        await create_formatter(bot, self).send_to(channel)
