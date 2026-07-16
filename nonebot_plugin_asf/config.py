from __future__ import annotations

from typing import Any

from pydantic import BaseModel, field_validator


def parse_id_set(value: str | int | None) -> set[int]:
    if value is None or value == "":
        return set()
    return {int(item.strip()) for item in str(value).split(",") if item.strip()}


class Config(BaseModel):
    telegram_bot_token: str = ""
    telegram_proxy: str = ""
    telegram_allowed_user_ids: str = ""
    telegram_allowed_chat_ids: str = ""
    asf_base_url: str = "http://asf:1242"
    asf_ipc_password: str = ""
    poll_timeout_seconds: int = 45

    @field_validator(
        "telegram_bot_token",
        "telegram_proxy",
        "telegram_allowed_user_ids",
        "telegram_allowed_chat_ids",
        "asf_base_url",
        "asf_ipc_password",
        mode="before",
    )
    @classmethod
    def coerce_scalar_to_string(cls, value: Any) -> str:
        if value is None:
            return ""
        return str(value)

    @field_validator("asf_base_url")
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")

    @property
    def allowed_user_ids(self) -> set[int]:
        return parse_id_set(self.telegram_allowed_user_ids)

    @property
    def allowed_chat_ids(self) -> set[int]:
        return parse_id_set(self.telegram_allowed_chat_ids)

    def validate_runtime(self) -> None:
        missing = []
        if not self.telegram_bot_token:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not self.asf_ipc_password:
            missing.append("ASF_IPC_PASSWORD")
        if not self.allowed_user_ids and not self.allowed_chat_ids:
            missing.append("TELEGRAM_ALLOWED_USER_IDS or TELEGRAM_ALLOWED_CHAT_IDS")
        if missing:
            raise RuntimeError("Missing required nonebot-plugin-asf config: " + ", ".join(missing))
