from __future__ import annotations

import asyncio
import logging

from nonebot import get_driver, get_plugin_config
from nonebot.log import logger
from nonebot.plugin import PluginMetadata

from .config import Config
from .telegram import TelegramBot

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_asf",
    description="Control ArchiSteamFarm from Telegram through ASF IPC.",
    usage="Use /commands for command list and prefix ASF commands with !, e.g. !status.",
    type="application",
    homepage="https://github.com/JustArchiNET/ArchiSteamFarm/wiki/IPC",
    config=Config,
    supported_adapters=None,
)

config = get_plugin_config(Config)

driver = get_driver()
telegram_bot: TelegramBot | None = None
polling_task: asyncio.Task[None] | None = None


@driver.on_startup
async def start_polling() -> None:
    global polling_task, telegram_bot
    config.validate_runtime()
    telegram_bot = TelegramBot(config)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    polling_task = asyncio.create_task(telegram_bot.run())
    logger.info("nonebot_plugin_asf started")


@driver.on_shutdown
async def stop_polling() -> None:
    if polling_task:
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            pass
    if telegram_bot:
        await telegram_bot.close()
    logger.info("nonebot_plugin_asf stopped")
