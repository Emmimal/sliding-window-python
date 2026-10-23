import pytest

from brute_force import shortest_burst_brute
from pitfalls import (
    busiest_total_off_by_one,
    longest_distinct_no_guard,
    shortest_burst_unchecked,
)
from sliding_window import busiest_window, longest_distinct_run


def test_shrinking_window_gives_a_wrong_answer_with_negative_numbers() -> None:
    # 2 + 3 = 5 is a window of length 2, but the shrinking rule never sees it.
    counts = [2, -1, 2, 3]
    assert shortest_burst_brute(counts, 5) == (2, 2)
    assert shortest_burst_unchecked(counts, 5) == 4


def test_off_by_one_drops_the_wrong_item() -> None:
    counts = [2, 1, 5, 1, 3, 2]
    total, _ = busiest_window(counts, 3)
    assert total == 9
    assert busiest_total_off_by_one(counts, 3) != 9


def test_missing_guard_lets_left_move_backwards() -> None:
    # In "abba", the last "a" was last seen at index 0, outside the window.
    length, _ = longest_distinct_run("abba")
    assert length == 2
    assert longest_distinct_no_guard("abba") == 3


@pytest.mark.parametrize("counts", [[3, 1, 2], [0, 0, 5]])
def test_unchecked_version_is_fine_when_counts_are_not_negative(
    counts: list[int],
) -> None:
    expected = shortest_burst_brute(counts, 3)
    assert expected is not None
    assert shortest_burst_unchecked(counts, 3) == expected[0]
