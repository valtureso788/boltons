"""
Функции для работы с итераторами и потоками данных.

Идеи позаимствованы у модуля ``boltons.iterutils`` из библиотеки
[`boltons`](https://pypi.org/project/boltons/).
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import TypeVar, List

__all__ = ["chunked", "windowed", "unique_everseen"]


T = TypeVar("T")


def chunked(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
    """
    Разбивает входной итератор на куски фиксированного размера.

    Последний кусок может быть короче, если элементов не хватает.
    """
    if size <= 0:
        raise ValueError("size must be positive")

    chunk: List[T] = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) >= size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def windowed(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
    """
    Скользящее окно по итератору.

    Для входной последовательности ``[1, 2, 3, 4]`` и ``size=3`` результат:
    ``[1, 2, 3]``, затем ``[2, 3, 4]``.
    """
    if size <= 0:
        raise ValueError("size must be positive")

    from collections import deque

    window: "deque[T]" = deque(maxlen=size)
    for item in iterable:
        window.append(item)
        if len(window) == size:
            yield list(window)


def unique_everseen(iterable: Iterable[T]) -> Iterator[T]:
    """
    Удаляет дубликаты, сохраняя порядок первых вхождений.
    """
    seen: set[T] = set()
    for item in iterable:
        if item in seen:
            continue
        seen.add(item)
        yield item

