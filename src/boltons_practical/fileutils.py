"""
Утилиты для безопасной работы с файловой системой.

Функции спроектированы по мотивам идей из настоящей библиотеки `boltons.fileutils`
(`https://boltons.readthedocs.io/en/latest/fileutils.html`), но реализованы
самостоятельно и в упрощённом виде.
"""

from __future__ import annotations

from pathlib import Path
from shutil import copy2
from typing import Iterable, Iterator, Optional

__all__ = [
    "ensure_dir",
    "mkdir_p",
    "iter_find_files",
    "safe_write_text",
    "read_text_lines",
    "copy_file_atomic",
    "touch",
]


def ensure_dir(path: str | Path) -> Path:
    """
    Гарантированно создаёт директорию (аналог ``mkdir -p``).

    :param path: путь к директории
    :return: объект ``Path`` для созданной (или уже существующей) директории
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def mkdir_p(path: str | Path) -> Path:
    """
    Синоним для :func:`ensure_dir` в стиле Unix-команды ``mkdir -p``.
    """

    return ensure_dir(path)


def iter_find_files(
    root: str | Path,
    pattern: str = "*",
    *,
    include_dirs: bool = False,
) -> Iterator[Path]:
    """
    Итеративно ищет файлы (и опционально директории) по glob-паттерну,
    возвращая ленивый итератор.

    :param root: корневая директория поиска
    :param pattern: glob-паттерн (например, ``\"*.py\"``)
    :param include_dirs: если ``True``, в результат попадают и директории
    """
    base = Path(root)
    for path in base.rglob(pattern):
        if path.is_dir() and not include_dirs:
            continue
        yield path


def safe_write_text(
    path: str | Path,
    data: str,
    *,
    encoding: str = "utf-8",
    newline: Optional[str] = None,
) -> Path:
    """
    Безопасная запись текста в файл через временный файл и атомарный rename.

    Это снижает вероятность получить «битый» файл при аварийном завершении
    программы.
    """
    target = Path(path)
    ensure_dir(target.parent)

    tmp_path = target.with_suffix(target.suffix + ".tmp")
    with tmp_path.open("w", encoding=encoding, newline=newline) as f:
        f.write(data)

    tmp_path.replace(target)
    return target


def copy_file_atomic(src: str | Path, dst: str | Path) -> Path:
    """
    Копирует файл, используя временный файл и атомарный ``rename``.

    Подходит для случаев, когда важна целостность целевого файла.
    """
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.is_file():
        raise FileNotFoundError(f"source file does not exist: {src_path}")

    ensure_dir(dst_path.parent)

    tmp_path = dst_path.with_suffix(dst_path.suffix + ".tmp")
    copy2(src_path, tmp_path)
    tmp_path.replace(dst_path)
    return dst_path


def read_text_lines(
    path: str | Path,
    *,
    encoding: str = "utf-8",
    strip_newline: bool = True,
) -> Iterable[str]:
    """
    Читает файл построчно, по необходимости убирая символ перевода строки.
    """
    p = Path(path)
    with p.open("r", encoding=encoding) as f:
        for line in f:
            yield line.rstrip("\n\r") if strip_newline else line


def touch(path: str | Path) -> Path:
    """
    Аналог команды ``touch``: создаёт пустой файл, если его не было,
    и обновляет время последнего доступа.
    """
    p = Path(path)
    ensure_dir(p.parent)
    p.touch()
    return p

