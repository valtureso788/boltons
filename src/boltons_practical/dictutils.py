"""
Утилиты для работы со словарями.

По мотивам модуля ``boltons.dictutils`` из оригинальной библиотеки
[`mahmoud/boltons`](https://github.com/mahmoud/boltons).
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from typing import Any, Dict, Iterable, Iterator, Tuple

__all__ = ["FrozenDict", "merge_dicts", "pick", "omit"]


class FrozenDict(Mapping[str, Any]):
    """
    Иммутабельный словарь с хэшированием.

    Удобен, когда нужно использовать словарь в качестве ключа другого
    словаря или элемента множества.
    """

    def __init__(self, data: Mapping[str, Any] | Iterable[Tuple[str, Any]]):
        self._data: Dict[str, Any] = dict(data)
        self._hash: int | None = None

    def __getitem__(self, key: str) -> Any:  # type: ignore[override]
        return self._data[key]

    def __iter__(self) -> Iterator[str]:  # type: ignore[override]
        return iter(self._data)

    def __len__(self) -> int:  # type: ignore[override]
        return len(self._data)

    def __repr__(self) -> str:
        return f"FrozenDict({self._data!r})"

    def __hash__(self) -> int:
        if self._hash is None:
            # Порядок ключей не важен, поэтому сортируем пары.
            items = tuple(sorted(self._data.items()))
            self._hash = hash(items)
        return self._hash


def merge_dicts(
    base: MutableMapping[str, Any],
    *others: Mapping[str, Any],
    deep: bool = False,
) -> MutableMapping[str, Any]:
    """
    Объединяет несколько словарей в первый (base).

    :param base: словарь, который будет модифицирован
    :param others: остальные словари
    :param deep: если ``True``, то вложенные словари также сливаются рекурсивно
    :return: модифицированный ``base``
    """

    for other in others:
        for key, value in other.items():
            if (
                deep
                and key in base
                and isinstance(base[key], MutableMapping)
                and isinstance(value, Mapping)
            ):
                merge_dicts(base[key], value, deep=True)  # type: ignore[arg-type]
            else:
                base[key] = value
    return base


def pick(d: Mapping[str, Any], keys: Iterable[str]) -> Dict[str, Any]:
    """
    Возвращает новый словарь, содержащий только указанные ключи.
    Отсутствующие ключи игнорируются.
    """
    key_set = set(keys)
    return {k: v for k, v in d.items() if k in key_set}


def omit(d: Mapping[str, Any], keys: Iterable[str]) -> Dict[str, Any]:
    """
    Возвращает новый словарь без указанных ключей.
    """
    key_set = set(keys)
    return {k: v for k, v in d.items() if k not in key_set}

