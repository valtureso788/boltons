"""
boltons_practical
==================

Небольшой набор хорошо написанных утилит в духе оригинальной библиотеки
`boltons` (см. репозиторий [`mahmoud/boltons`](https://github.com/mahmoud/boltons)).

Модули:
    - fileutils: работа с файлами и директориями
    - dictutils: операции над словарями
    - iterutils: функции для работы с итераторами
    - functional: утилиты для функционального стиля программирования
"""

from . import fileutils, dictutils, iterutils, functional
from .fileutils import ensure_dir, mkdir_p, iter_find_files, safe_write_text, read_text_lines, copy_file_atomic, touch
from .dictutils import FrozenDict, merge_dicts, pick, omit
from .iterutils import chunked, windowed, unique_everseen
from .functional import compose, memoize

__all__ = [
    # подмодули
    "fileutils",
    "dictutils",
    "iterutils",
    "functional",
    # высокоуровневые утилиты
    "ensure_dir",
    "mkdir_p",
    "iter_find_files",
    "safe_write_text",
    "read_text_lines",
    "copy_file_atomic",
    "touch",
    "FrozenDict",
    "merge_dicts",
    "pick",
    "omit",
    "chunked",
    "windowed",
    "unique_everseen",
    "compose",
    "memoize",
]


