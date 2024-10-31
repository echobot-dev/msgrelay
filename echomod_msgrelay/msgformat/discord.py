import mimetypes
from typing import TYPE_CHECKING, final

from nonebot.adapters.discord.api.model import (
    Embed,
    EmbedAuthor,
    EmbedFooter,
    EmbedImage,
)
from nonebot.adapters.discord.message import Message, MessageSegment

from ..config import config
from ._base import MessageFormatter

if TYPE_CHECKING:
    from nonebot.adapters.discord.bot import Bot
    from nonebot.adapters.discord.message import AttachmentSegment


@final
class DiscordMessageFormatter(MessageFormatter["Bot"]):
    async def format(self) -> Message:
        message = await self.event.message.export(self.bot)
        footer = config.msgrelay_discord_embed_footer.strip().format(**dict(self.event))

        formatted = Message(
            MessageSegment.embed(
                Embed(
                    # URL doesn't matter. It's just a placeholder used for merging
                    # multiple image embeds into one.
                    url="https://echobot.dev/",
                    description=message.extract_plain_text(),
                    author=EmbedAuthor(
                        name=self.event.session.sender.name,
                        icon_url=self.event.session.sender.avatar,
                    ),
                    footer=EmbedFooter(
                        text=footer, icon_url=self.event.session.channel.avatar
                    ),
                    color=config.msgrelay_discord_embed_color,
                    timestamp=self.event.op_time.isoformat(),
                )
            )
        )

        attachments: list[AttachmentSegment] = message["attachment"]
        formatted.extend(self._build_embed_image(attachments))

        return formatted

    def _build_embed_image(self, attachments: list["AttachmentSegment"]) -> Message:
        images = [
            i
            for i in attachments
            if (
                mimetypes.guess_type(i.data["attachment"].filename)[0] or ""
            ).startswith("image")
        ]

        return Message(
            MessageSegment.embed(
                Embed(
                    url="https://echobot.dev/",
                    image=EmbedImage(
                        url=f"attachment://{img.data['attachment'].filename}"
                    ),
                )
            )
            for img in images
        ).extend(images)

    async def send_to(self, channel: str) -> None:
        await self.bot.send_to(int(channel), await self.format())
