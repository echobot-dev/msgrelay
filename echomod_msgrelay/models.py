from datetime import datetime
from typing import Literal

from nonebot_plugin_alconna import UniMessage
from nonebot_plugin_uninfo import Session as UninfoSession
from pydantic import BaseModel, ConfigDict

from .config import config


class User(BaseModel):
    id: str
    name: str
    avatar: str | None = None


class Channel(BaseModel):
    id: str
    name: str
    type: str
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
                type=session.scope,
                avatar=session.scene.avatar,
            ),
        )


class RelayEvent(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    session: RelaySession
    message: UniMessage
    op_type: Literal["create", "update", "delete"]
    op_time: datetime

    def get_message(
        self, boundary: str = config.msgrelay_header_boundary
    ) -> UniMessage:
        return (
            config.msgrelay_header_template.strip().format(**dict(self))
            + boundary
            + self.message
        )
