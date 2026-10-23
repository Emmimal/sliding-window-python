import random

import pytest

from brute_force import (
    busiest_window_brute,
    longest_distinct_brute,
    longest_k_distinct_brute,
    max_events_brute,
    shortest_burst_brute,
)
from sliding_window import (
    busiest_window,
    longest_distinct_run,
    longest_run_with_at_most_k_distinct,
    max_events_in_window,
    moving_average,
    shortest_burst,
    windows,
)

# --- busiest_window -------------------------------------------------------


def test_busiest_window_example() -> None:
    assert busiest_window([2, 1, 5, 1, 3, 2], 3) == (9, 2)


@pytest.mark.parametrize(
    ("counts", "size", "expected"),
    [
        ([5], 1, (5, 0)),
        ([1, 2, 3], 3, (6, 0)),
        ([-1, -2, -3], 2, (-3, 0)),
        ([4, 4, 4, 4], 2, (8, 0)),  # tie: earliest window wins
    ],
)
def test_busiest_window_edge_cases(
    counts: list[int], size: int, expected: tuple[int, int]
) -> None:
    assert busiest_window(counts, size) == expected


@pytest.mark.parametrize(("counts", "size"), [([], 1), ([1, 2], 3), ([1, 2], 0)])
def test_busiest_window_rejects_bad_size(counts: list[int], size: int) -> None:
    with pytest.raises(ValueError):
        busiest_window(counts, size)


def test_busiest_window_agrees_with_brute_force_on_random_input() -> None:
    rng = random.Random(42)
    for _ in range(1_000):
        counts = [rng.randint(-10, 10) for _ in range(rng.randint(1, 15))]
        size = rng.randint(1, len(counts))
        assert busiest_window(counts, size) == busiest_window_brute(counts, size)


# --- windows and moving_average ---------------------------------------------


def test_windows_matches_the_documented_recipe_example() -> None:
    assert list(windows("ABCDEFG", 3)) == [
        ("A", "B", "C"),
        ("B", "C", "D"),
        ("C", "D", "E"),
        ("D", "E", "F"),
        ("E", "F", "G"),
    ]


@pytest.mark.parametrize("items", [[], [1], [1, 2]])
def test_windows_yields_nothing_when_input_is_shorter_than_size(
    items: list[int],
) -> None:
    assert list(windows(items, 3)) == []


def test_windows_rejects_bad_size_immediately() -> None:
    with pytest.raises(ValueError):
        windows([1, 2, 3], 0)  # no need to iterate to see the error


def test_windows_works_on_a_generator() -> None:
    stream = (n * n for n in range(5))
    assert list(windows(stream, 2)) == [(0, 1), (1, 4), (4, 9), (9, 16)]


def test_windows_agrees_with_slicing_on_random_input() -> None:
    rng = random.Random(1)
    for _ in range(300):
        items = [rng.randint(0, 9) for _ in range(rng.randint(0, 12))]
        size = rng.randint(1, 5)
        expected = [tuple(items[i : i + size]) for i in range(len(items) - size + 1)]
        assert list(windows(items, size)) == expected


def test_moving_average_example() -> None:
    assert list(moving_average([1, 3, 2, 6, -1, 4], 3)) == pytest.approx(
        [2.0, 11 / 3, 7 / 3, 3.0]
    )


def test_moving_average_works_on_a_generator() -> None:
    stream = (n for n in range(1, 6))
    assert list(moving_average(stream, 2)) == pytest.approx([1.5, 2.5, 3.5, 4.5])


def test_moving_average_matches_direct_calculation() -> None:
    rng = random.Random(3)
    for _ in range(300):
        values = [rng.randint(-9, 9) for _ in range(rng.randint(0, 12))]
        size = rng.randint(1, 5)
        expected = [
            sum(values[i : i + size]) / size for i in range(len(values) - size + 1)
        ]
        assert list(moving_average(values, size)) == pytest.approx(expected)


# --- shortest_burst -----------------------------------------------------------


def test_shortest_burst_example() -> None:
    assert shortest_burst([2, 3, 1, 2, 4, 3], 7) == (2, 4)


@pytest.mark.parametrize(
    ("counts", "target", "expected"),
    [
        ([], 5, None),
        ([1, 1, 1], 10, None),
        ([10], 10, (1, 0)),
        ([1, 2, 3, 4, 5], 15, (5, 0)),
        ([0, 0, 7], 7, (1, 2)),
    ],
)
def test_shortest_burst_edge_cases(
    counts: list[int], target: int, expected: tuple[int, int] | None
) -> None:
    assert shortest_burst(counts, target) == expected


def test_shortest_burst_rejects_negative_counts() -> None:
    with pytest.raises(ValueError, match="negative"):
        shortest_burst([2, -1, 2, 3], 5)


def test_shortest_burst_rejects_bad_target() -> None:
    with pytest.raises(ValueError):
        shortest_burst([1, 2, 3], 0)


def test_shortest_burst_agrees_with_brute_force_on_random_input() -> None:
    rng = random.Random(7)
    for _ in range(1_000):
        counts = [rng.randint(0, 9) for _ in range(rng.randint(0, 14))]
        target = rng.randint(1, 30)
        assert shortest_burst(counts, target) == shortest_burst_brute(counts, target)


# --- max_events_in_window ---------------------------------------------------------


def test_max_events_in_window_example() -> None:
    assert max_events_in_window([0.0, 1.0, 1.5, 2.0, 9.0, 9.5], 2.0) == 3


@pytest.mark.parametrize(
    ("timestamps", "span", "expected"),
    [([], 5.0, 0), ([3.0], 5.0, 1), ([1.0, 1.0, 1.0], 0.5, 3), ([0.0, 2.0], 2.0, 1)],
)
def test_max_events_in_window_edge_cases(
    timestamps: list[float], span: float, expected: int
) -> None:
    assert max_events_in_window(timestamps, span) == expected


def test_max_events_agrees_with_brute_force_on_random_input() -> None:
    rng = random.Random(13)
    for _ in range(1_000):
        timestamps = sorted(rng.randint(0, 40) / 2 for _ in range(rng.randint(0, 15)))
        span = rng.randint(1, 10) / 2
        assert max_events_in_window(timestamps, span) == max_events_brute(
            timestamps, span
        )


# --- distinct runs ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abcabcbb", (3, 0)),
        ("bbbbb", (1, 0)),
        ("pwwkew", (3, 2)),
        ("", (0, 0)),
        ("abba", (2, 0)),
        ("dvdf", (3, 1)),
    ],
)
def test_longest_distinct_run(text: str, expected: tuple[int, int]) -> None:
    assert longest_distinct_run(text) == expected


def test_longest_distinct_run_works_on_user_ids() -> None:
    assert longest_distinct_run([7, 3, 7, 9, 4, 3]) == (4, 1)


def test_longest_distinct_agrees_with_brute_force_on_random_input() -> None:
    rng = random.Random(11)
    for _ in range(1_000):
        items = [rng.choice("abcd") for _ in range(rng.randint(0, 14))]
        assert longest_distinct_run(items) == longest_distinct_brute(items)


@pytest.mark.parametrize(
    ("text", "k", "expected"),
    [("eceba", 2, (3, 0)), ("aa", 1, (2, 0)), ("", 2, (0, 0)), ("abc", 5, (3, 0))],
)
def test_longest_run_with_at_most_k_distinct(
    text: str, k: int, expected: tuple[int, int]
) -> None:
    assert longest_run_with_at_most_k_distinct(text, k) == expected


def test_longest_run_with_at_most_k_distinct_rejects_bad_k() -> None:
    with pytest.raises(ValueError):
        longest_run_with_at_most_k_distinct("abc", 0)


def test_longest_k_distinct_agrees_with_brute_force_on_random_input() -> None:
    rng = random.Random(5)
    for _ in range(1_000):
        items = [rng.choice("abcde") for _ in range(rng.randint(0, 14))]
        k = rng.randint(1, 4)
        assert longest_run_with_at_most_k_distinct(
            items, k
        ) == longest_k_distinct_brute(items, k)
