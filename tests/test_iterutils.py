from boltons_practical import chunked, windowed, unique_everseen


def test_chunked_basic() -> None:
    data = list(chunked(range(7), 3))
    assert data == [[0, 1, 2], [3, 4, 5], [6]]


def test_windowed_basic() -> None:
    data = list(windowed([1, 2, 3, 4], 3))
    assert data == [[1, 2, 3], [2, 3, 4]]


def test_unique_everseen_preserves_order() -> None:
    items = [1, 2, 1, 3, 2, 4]
    assert list(unique_everseen(items)) == [1, 2, 3, 4]

