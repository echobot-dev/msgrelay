import nonebot
from pydantic import BaseModel


class Config(BaseModel):
    msgrelay_channels: dict[str, list[str]]
    msgrelay_header_template: str = (
        "{session.sender.name} {op_type}d a message from {session.channel.name} "
        "({session.channel.type}:{session.channel.id}) at {op_time:%Y-%m-%d %H:%M:%S}:"
    )
    msgrelay_header_boundary: str = "\n"


config = nonebot.get_plugin_config(Config)
