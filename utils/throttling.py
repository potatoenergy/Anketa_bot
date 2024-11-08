# Определяем декоратор для ограничения частоты запросов пользователя
def rate_limit(limit: int = 1):

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        return func

    return decorator
