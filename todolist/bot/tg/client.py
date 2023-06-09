from typing import Any

import requests
import logging

from marshmallow import ValidationError
from todolist.settings import BOT_TOKEN
from bot.tg.dc import GetUpdatesResponseSchema, SendMessageResponseSchema


logger = logging.getLogger(__name__)


class TgClient:
    def __init__(self, token: str = BOT_TOKEN, parse_mode: str = "Markdown"):
        self.token = token
        self.parse_mode = parse_mode

    def __get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60, **kwargs: Any) -> GetUpdatesResponseSchema:
        """
        Через getUpdates помимо 'update_id' и 'message' может передаваться много разных значений,
        подробнее тут https://core.telegram.org/bots/api#update , они нам в целом не нужны
        В данном методе реализована валидация данных, чтобы не было проблем при их сериализации
        """
        payload = {"offset": offset, "timeout": timeout, "allowed_updates": "message"}
        data: dict = requests.get(
            url=self.__get_url(method="getUpdates"),
            params=payload,
            **kwargs
        ).json()
        self._validate_response(data)

        return GetUpdatesResponseSchema().load(data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponseSchema:
        """
        Метод отправляющий сообщения пользователю
        """
        payload = {"chat_id": chat_id, "text": text, "parse_mode": self.parse_mode}
        data: dict = requests.get(
            url=self.__get_url(method="sendMessage"),
            params=payload
        ).json()
        self._validate_response(data)

        return SendMessageResponseSchema().load(data)

    @staticmethod
    def _validate_response(data: dict):
        """
        Валидации плохих ответов от TelegramAPI
        """
        if not data['ok']:
            logger.error(f"HTTP_CODE: {data['error_code']} {data['description']}")
            raise ValidationError(message=f"HTTP_CODE: {data['error_code']}, see logs")

