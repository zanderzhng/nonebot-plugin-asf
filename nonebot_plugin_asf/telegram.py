from __future__ import annotations

import asyncio
import html
import logging
from typing import Any

import httpx

from .asf import run_asf_command
from .commands import ASF_COMMANDS_TEXT, HELP_TEXT
from .config import Config

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.base_url = f"https://api.telegram.org/bot{config.telegram_bot_token}"
        self.offset = 0
        self.client = httpx.AsyncClient(
            proxy=config.telegram_proxy or None,
            timeout=httpx.Timeout(config.poll_timeout_seconds + 15, connect=30),
        )

    async def close(self) -> None:
        await self.client.aclose()

    async def run(self) -> None:
        await self._delete_webhook()
        await self._set_commands()
        logger.info("telegram polling started")

        while True:
            try:
                updates = await self._get_updates()
                for update in updates:
                    self.offset = max(self.offset, int(update["update_id"]) + 1)
                    await self._handle_update(update)
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("telegram polling error")
                await asyncio.sleep(5)

    async def _delete_webhook(self) -> None:
        response = await self.client.post(f"{self.base_url}/deleteWebhook")
        response.raise_for_status()
        logger.info("telegram webhook disabled")

    async def _set_commands(self) -> None:
        response = await self.client.post(
            f"{self.base_url}/setMyCommands",
            json={
                "commands": [
                    {"command": "help", "description": "Show usage"},
                    {"command": "commands", "description": "List ASF commands"},
                ]
            },
        )
        response.raise_for_status()
        logger.info("telegram menu commands registered")

    async def _get_updates(self) -> list[dict[str, Any]]:
        response = await self.client.post(
            f"{self.base_url}/getUpdates",
            json={
                "offset": self.offset,
                "timeout": self.config.poll_timeout_seconds,
                "allowed_updates": ["message"],
            },
        )
        response.raise_for_status()
        payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError(payload)
        return payload.get("result", [])

    async def _handle_update(self, update: dict[str, Any]) -> None:
        message = update.get("message") or {}
        chat = message.get("chat") or {}
        sender = message.get("from") or {}
        chat_id = chat.get("id")
        user_id = sender.get("id")
        text = (message.get("text") or "").strip()

        if chat_id is None or user_id is None or not text:
            return

        if not self._is_allowed(int(chat_id), int(user_id)):
            logger.warning("denied telegram user_id=%s chat_id=%s", user_id, chat_id)
            await self._send_message(chat_id, "Unauthorized.")
            return

        slash_command = _slash_command(text)

        if slash_command in {"/start", "/help"}:
            await self._send_message(chat_id, HELP_TEXT)
            return

        if slash_command == "/commands":
            await self._send_message(chat_id, ASF_COMMANDS_TEXT)
            return

        if text.startswith("/"):
            await self._send_message(chat_id, HELP_TEXT)
            return

        if not text.startswith("!"):
            await self._send_message(chat_id, "Use /commands for available commands, or prefix ASF commands with !.")
            return

        command = text[1:].strip()
        if not command:
            await self._send_message(chat_id, "Please provide an ASF command after !.")
            return

        try:
            result = await run_asf_command(self.config, command)
        except Exception as exc:
            logger.exception("asf command failed")
            result = f"Error communicating with ASF: {exc}"

        await self._send_message(chat_id, result or "(empty response)")

    def _is_allowed(self, chat_id: int, user_id: int) -> bool:
        return (
            user_id in self.config.allowed_user_ids
            or chat_id in self.config.allowed_chat_ids
        )

    async def _send_message(self, chat_id: int, text: str) -> None:
        for chunk in _split_message(text):
            response = await self.client.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": f"<pre>{html.escape(chunk)}</pre>",
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
            )
            response.raise_for_status()


def _split_message(text: str, limit: int = 3900) -> list[str]:
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    remaining = text
    while remaining:
        chunks.append(remaining[:limit])
        remaining = remaining[limit:]
    return chunks


def _slash_command(text: str) -> str | None:
    if not text.startswith("/"):
        return None
    command = text.split(maxsplit=1)[0].split("@", maxsplit=1)[0]
    return command.lower()
