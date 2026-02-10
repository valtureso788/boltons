"""
Простые функциональные утилиты.

Здесь собраны небольшие, но полезные строительные блоки, которые часто
используются в инженерных библиотеках.
"""

from __future__ import annotations

from functools import wraps
from time import monotonic
from typing import Any, Callable, Dict, Hashable, Tuple, TypeVar, cast

__all__ = ["compose", "memoize"]

F = TypeVar("F", bound=Callable[..., Any])


def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """
    Функциональная композиция.

    ``compose(f, g, h)(x)`` эквивалентно ``f(g(h(x)))``.
    """

    if not funcs:
        raise ValueError("at least one function must be provided")

    def composed(value: Any) -> Any:
        result = value
        for fn in reversed(funcs):
            result = fn(result)
        return result

    return composed


def memoize(ttl: float | None = None) -> Callable[[F], F]:
    """
    Декоратор простого мемоизированного кеша.

    :param ttl: время жизни записи в секундах, если ``None`` — бесконечно.
    """

    def decorator(func: F) -> F:
        cache: Dict[Tuple[Hashable, Tuple[Hashable, ...]], Tuple[float, Any]] = {}

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            now = monotonic()

            if key in cache:
                ts, value = cache[key]
                if ttl is None or now - ts <= ttl:
                    return value

            value = func(*args, **kwargs)
            cache[key] = (now, value)
            return value

        return cast(F, wrapper)

    return decorator

