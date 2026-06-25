from __future__ import annotations

import json
from typing import Any

import httpx

from .config import Config


def format_asf_result(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, indent=2)


async def run_asf_command(config: Config, command: str) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{config.asf_base_url}/Api/Command",
            json={"Command": command},
            headers={"Authentication": config.asf_ipc_password},
        )
        response.raise_for_status()
        payload = response.json()

    if payload.get("Success"):
        return format_asf_result(payload.get("Result", ""))

    message = payload.get("Message") or "Unknown error"
    return f"ASF command failed: {message}"
