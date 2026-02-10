from boltons_practical import FrozenDict, merge_dicts, pick, omit


def test_frozendict_hash_and_equality() -> None:
    fd1 = FrozenDict({"a": 1, "b": 2})
    fd2 = FrozenDict({"b": 2, "a": 1})

    assert fd1 == fd2
    assert hash(fd1) == hash(fd2)


def test_merge_dicts_shallow_and_deep() -> None:
    base = {"a": 1, "nested": {"x": 1}}
    other = {"b": 2, "nested": {"y": 2}}

    merged_shallow = merge_dicts(dict(base), other, deep=False)
    assert merged_shallow["nested"] == {"y": 2}

    merged_deep = merge_dicts(dict(base), other, deep=True)
    assert merged_deep["nested"] == {"x": 1, "y": 2}


def test_pick_and_omit() -> None:
    d = {"a": 1, "b": 2, "c": 3}

    assert pick(d, ["a", "c", "z"]) == {"a": 1, "c": 3}
    assert omit(d, ["b"]) == {"a": 1, "c": 3}

