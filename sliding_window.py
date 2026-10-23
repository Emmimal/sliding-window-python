"""A small toolkit of sliding window solutions."""

from collections import Counter, deque
from collections.abc import Hashable, Iterable, Iterator, Sequence
from itertools import islice


def busiest_window(counts: Sequence[int], size: int) -> tuple[int, int]:
    """Return (total, start) for the window of `size` items with the largest sum.

    On a tie, the earliest window wins. Raises ValueError for a bad size.
    """
    if size < 1 or size > len(counts):
        raise ValueError("size must be between 1 and len(counts)")

    window_total = sum(counts[:size])
    best_total, best_start = window_total, 0

    for right in range(size, len(counts)):
        # Add the item that enters, drop the item that leaves.
        window_total += counts[right] - counts[right - size]
        if window_total > best_total:
            best_total, best_start = window_total, right - size + 1

    return best_total, best_start


def windows[T](iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    """Yield every window of `size` neighboring items, one tuple at a time.

    Works on any iterable, including generators, and holds only `size`
    items in memory.
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    return _windows(iterable, size)


def _windows[T](iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    iterator = iter(iterable)
    window = deque(islice(iterator, size - 1), maxlen=size)
    for item in iterator:
        window.append(item)
        yield tuple(window)


def moving_average(values: Iterable[float], size: int) -> Iterator[float]:
    """Yield the average of every window of `size` values from a stream."""
    if size < 1:
        raise ValueError("size must be at least 1")

    window: deque[float] = deque(maxlen=size)
    total = 0.0

    for value in values:
        if len(window) == size:
            total -= window[0]  # This item is about to be pushed out.
        window.append(value)
        total += value
        if len(window) == size:
            yield total / size


def shortest_burst(counts: Sequence[int], target: int) -> tuple[int, int] | None:
    """Return (length, start) of the shortest window whose sum is >= target.

    Returns None when no window reaches the target. Every count must be
    zero or more: the shrinking rule below is wrong for negative numbers,
    so they are rejected instead of giving a quiet wrong answer.
    """
    if target < 1:
        raise ValueError("target must be at least 1")
    if any(count < 0 for count in counts):
        raise ValueError("counts must not be negative")

    left = 0
    window_total = 0
    best: tuple[int, int] | None = None

    for right, value in enumerate(counts):
        window_total += value

        # The window is big enough, so shrink it as far as we can.
        while window_total >= target:
            length = right - left + 1
            if best is None or length < best[0]:
                best = (length, left)
            window_total -= counts[left]
            left += 1

    return best


def max_events_in_window(timestamps: Sequence[float], span: float) -> int:
    """Return the most events that fall inside any window `span` seconds long.

    `timestamps` must be sorted. A window covers [start, start + span).
    """
    if span <= 0:
        raise ValueError("span must be positive")

    left = 0
    best = 0

    for right, timestamp in enumerate(timestamps):
        # The window is defined by time, so the left edge moves until
        # the oldest event is less than `span` seconds old.
        while timestamp - timestamps[left] >= span:
            left += 1
        best = max(best, right - left + 1)

    return best


def longest_distinct_run(items: Sequence[Hashable]) -> tuple[int, int]:
    """Return (length, start) of the longest run with no repeated item."""
    last_seen: dict[Hashable, int] = {}
    left = 0
    best_length, best_start = 0, 0

    for right, item in enumerate(items):
        # If the item is already inside the window, jump left past its old spot.
        if item in last_seen and last_seen[item] >= left:
            left = last_seen[item] + 1
        last_seen[item] = right

        if right - left + 1 > best_length:
            best_length, best_start = right - left + 1, left

    return best_length, best_start


def longest_run_with_at_most_k_distinct(
    items: Sequence[Hashable], k: int
) -> tuple[int, int]:
    """Return (length, start) of the longest run with at most k different items."""
    if k < 1:
        raise ValueError("k must be at least 1")

    counts: Counter[Hashable] = Counter()
    left = 0
    best_length, best_start = 0, 0

    for right, item in enumerate(items):
        counts[item] += 1

        # Too many kinds of items: shrink from the left.
        while len(counts) > k:
            leaving = items[left]
            counts[leaving] -= 1
            if counts[leaving] == 0:
                del counts[leaving]
            left += 1

        if right - left + 1 > best_length:
            best_length, best_start = right - left + 1, left

    return best_length, best_start
