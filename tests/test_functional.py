import time

from boltons_practical import compose, memoize


def test_compose_order() -> None:
    def inc(x: int) -> int:
        return x + 1

    def dbl(x: int) -> int:
        return x * 2

    fn = compose(str, dbl, inc)  # str(dbl(inc(x)))
    assert fn(3) == "8"


def test_memoize_ttl() -> None:
    calls = {"count": 0}

    @memoize(ttl=0.1)
    def slow_add(a: int, b: int) -> int:
        calls["count"] += 1
        return a + b

    assert slow_add(1, 2) == 3
    assert slow_add(1, 2) == 3
    # результат взят из кеша
    assert calls["count"] == 1

    time.sleep(0.11)

    # TTL истёк, функция вызывается снова
    assert slow_add(1, 2) == 3
    assert calls["count"] == 2

