import logging
from typing import TypedDict, Any, Dict

from apps.shared.messages import MESSAGES, MessageTemplate

logger = logging.getLogger(__name__)


class MessageDetail(TypedDict):
    """Final translated response message structure"""
    id: str
    message: str
    status_code: int


def get_message_detail(
    message_key: str,
    lang: str = "en",
    context: Dict[str, Any] | None = None
) -> MessageDetail:
    """
    Get translated and formatted message by message_key.

    Supports:
    - full language (uz-UZ)
    - short language (uz)
    - fallback to English
    """

    # 1) Get message template
    message = MESSAGES.get(message_key)

    if not message:
        logger.warning(f"Message key not found: {message_key}")
        message = MESSAGES.get("UNKNOWN_ERROR")

        # If even UNKNOWN_ERROR missing — create fallback
        if not message:
            logger.error("UNKNOWN_ERROR message not found in MESSAGES dictionary")
            return {
                "id": "SYSTEM_ERROR",
                "message": "An unexpected error occurred",
                "status_code": 500
            }

    # 2) Context for formatting
    context = context or {}

    messages_dict: Dict[str, str] = message["messages"]

    # 3) Language fallback order
    base_lang = lang.split("-")[0].split("_")[0]

    template = (
        messages_dict.get(lang)
        or messages_dict.get(base_lang)
        or messages_dict.get("en")
        or "Error occurred"
    )

    # 4) Format message safely
    try:
        formatted_message = template.format(**context)
    except Exception as e:
        logger.warning(
            f"Message formatting failed — key='{message_key}', lang='{lang}', "
            f"context={context}, error={e}"
        )
        formatted_message = template

    # 5) Return final structure
    return {
        "id": message["id"],
        "message": formatted_message,
        "status_code": message["status_code"],
    }


def get_raw_message(message_key: str) -> MessageTemplate | None:
    """Return raw MESSAGES template entry (internal use only)."""
    return MESSAGES.get(message_key)
