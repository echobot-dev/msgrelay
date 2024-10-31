"""Receive, resolve and relay messages."""

from datetime import datetime

import nonebot
from anyio import create_task_group
from nonebot import on_message
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot_plugin_alconna.uniseg import UniMsg
from nonebot_plugin_uninfo import Session, UniSession

from .config import config
from .models import RelayEvent, RelaySession

matcher = on_message(priority=1, block=False)


@matcher.handle()
async def resolve_message_event(
    state: T_State, message: UniMsg, session: Session = UniSession()
) -> None:
    if session.scene.id not in config.msgrelay_channels.get(session.adapter, []):
        logger.debug(
            f"The channel ({session.scene.name}:{session.scene.id}) where the message "
            "sent is not in the specified channels. Skipped."
        )
        await matcher.finish()

    state["event"] = RelayEvent(
        session=RelaySession.build(session),
        message=message,
        op_time=datetime.now().astimezone(),
        op_type="create",
    )


@matcher.handle()
async def relay_create_message(state: T_State) -> None:
    """Relay the created message to other channels."""
    event: RelayEvent | None = state.get("event")
    if not event:
        raise RuntimeError("No relay event found in the state.")

    async with create_task_group() as tg:
        for _, bot in nonebot.get_bots().items():
            for channel in config.msgrelay_channels.get(bot.type, []):
                if channel != event.session.channel.id:
                    tg.start_soon(event.send_message, bot, channel)
                    logger.info(
                        f"Message relayed to channel {event.session.channel.name} "
                        f"({event.session.channel.platform}:{channel})."
                    )
