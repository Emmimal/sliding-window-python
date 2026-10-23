"""Buggy versions of the sliding window, kept so tests can show how they fail."""

from collections.abc import Hashable, Sequence


def shortest_burst_unchecked(counts: Sequence[int], target: int) -> int:
    """Bug: the shrinking rule assumes counts are never negative.

    Same loop as shortest_burst(), without the check that rejects negative
    numbers. Returns the shortest length, or 0 when nothing reaches target.
    """
    left = 0
    window_total = 0
    best = 0

    for right, value in enumerate(counts):
        window_total += value
        while window_total >= target:
            length = right - left + 1
            if best == 0 or length < best:
                best = length
            window_total -= counts[left]
            left += 1

    return best


def busiest_total_off_by_one(counts: Sequence[int], size: int) -> int:
    """Bug: the item that leaves is at right - size + 1, not right - size."""
    window_total = sum(counts[:size])
    best = window_total

    for right in range(size, len(counts)):
        window_total += counts[right] - counts[right - size + 1]
        best = max(best, window_total)

    return best


def longest_distinct_no_guard(items: Sequence[Hashable]) -> int:
    """Bug: moves left backwards when the repeated item is outside the window."""
    last_seen: dict[Hashable, int] = {}
    left = 0
    best = 0

    for right, item in enumerate(items):
        if item in last_seen:
            left = last_seen[item] + 1  # Missing: max(left, ...)
        last_seen[item] = right
        best = max(best, right - left + 1)

    return best
