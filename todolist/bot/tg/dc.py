from dataclasses import dataclass
from typing import List, Optional, Dict, Callable, Any

import marshmallow
import marshmallow_dataclass


@dataclass
class Chat:
    id: int
    username: str

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Message:
    message_id: int
    chat: Chat
    date: int
    text: Optional[str] = ""

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message = "{}"

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE


GetUpdatesResponseSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
SendMessageResponseSchema = marshmallow_dataclass.class_schema(SendMessageResponse)


@dataclass
class FSMData:
    next_handler: Callable[..., str]
    data: Dict[str, Any]
