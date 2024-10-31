from typing import Annotated

import nonebot
from pydantic import BaseModel, BeforeValidator


def color_validator(value: str | int) -> int:
    if isinstance(value, str):
        value = int(value.strip("#"), base=16)
    if not 0x000000 <= value <= 0xFFFFFF:
        raise ValueError("Value must be a valid RGB hex code")
    return value


ColorHex = Annotated[int, BeforeValidator(color_validator)]


class Config(BaseModel):
    msgrelay_channels: dict[str, list[str]]

    msgrelay_header_template: str = (
        "{session.sender.name} {op_type}d a message from {session.channel.name} "
        "({session.channel.type}:{session.channel.id}) at {op_time:%Y-%m-%d %H:%M:%S}:"
    )
    msgrelay_header_boundary: str = "\n"

    msgrelay_discord_use_embed: bool = True
    msgrelay_discord_embed_footer: str = (
        "{session.channel.name} ({session.channel.platform}, {session.channel.id})"
    )
    msgrelay_discord_embed_color: ColorHex = 0x388E3C


config = nonebot.get_plugin_config(Config)
