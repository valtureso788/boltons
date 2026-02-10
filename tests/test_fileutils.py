import os
from pathlib import Path

from boltons_practical import (
    ensure_dir,
    mkdir_p,
    iter_find_files,
    safe_write_text,
    read_text_lines,
    copy_file_atomic,
    touch,
)


def test_ensure_dir_and_mkdir_p(tmp_path: Path) -> None:
    d1 = ensure_dir(tmp_path / "a" / "b")
    d2 = mkdir_p(tmp_path / "a" / "c")
    assert d1.is_dir()
    assert d2.is_dir()


def test_safe_write_and_read_lines(tmp_path: Path) -> None:
    target = tmp_path / "data.txt"
    safe_write_text(target, "one\ntwo\n")
    lines = list(read_text_lines(target))
    assert lines == ["one", "two"]


def test_iter_find_files_and_copy_file_atomic(tmp_path: Path) -> None:
    src = tmp_path / "src.txt"
    dst = tmp_path / "out" / "dst.txt"
    src.write_text("hello", encoding="utf-8")

    copied = copy_file_atomic(src, dst)
    assert copied.read_text(encoding="utf-8") == "hello"

    found = list(iter_find_files(tmp_path, "*.txt"))
    assert src in found
    assert dst in found


def test_touch_updates_timestamp(tmp_path: Path) -> None:
    file_path = tmp_path / "touch_me.txt"
    touch(file_path)
    first_mtime = os.stat(file_path).st_mtime

    touch(file_path)
    second_mtime = os.stat(file_path).st_mtime

    assert second_mtime >= first_mtime

