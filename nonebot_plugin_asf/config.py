from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


def parse_id_set(value: str) -> set[int]:
    return {int(item.strip()) for item in value.split(",") if item.strip()}


class Config(BaseModel):
    telegram_bot_token: str = Field(min_length=1)
    telegram_proxy: str = ""
    telegram_allowed_user_ids: str = ""
    telegram_allowed_chat_ids: str = ""
    asf_base_url: str = "http://asf:1242"
    asf_ipc_password: str = Field(min_length=1)
    poll_timeout_seconds: int = 45

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
