# Импортируем необходимые модули
from typing import Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from cachetools import TTLCache

# Определяем middleware для ограничения частоты запросов пользователя
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int = 1) -> None:
        """
        :param time_limit:
            - Задержка, при срабатывании "отключает" хендлер на определенное время.
            По умолчанию 1 секунда.
        """
        # Создаем кэш для хранения информации о последних запросах пользователя
        self._limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict], Awaitable[None]],
        event: Message | CallbackQuery,
        data: dict
    ) -> None:
        # Если пользователь уже отправлял запрос в течение заданного времени, игнорируем запрос
        if event.from_user.id in self._limit:
            return
        else:
            # Иначе добавляем пользователя в кэш и обрабатываем запрос
            self._limit[event.from_user.id] = None
        return await handler(event, data)