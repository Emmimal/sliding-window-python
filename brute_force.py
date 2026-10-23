"""Slow but obviously correct solutions, used as a baseline and as a test oracle."""

from collections.abc import Hashable, Sequence


def busiest_window_brute(counts: Sequence[int], size: int) -> tuple[int, int]:
    """Return (total, start) of the largest window sum, earliest on a tie."""
    if size < 1 or size > len(counts):
        raise ValueError("size must be between 1 and len(counts)")
    best_total, best_start = sum(counts[:size]), 0
    for start in range(1, len(counts) - size + 1):
        total = sum(counts[start : start + size])
        if total > best_total:
            best_total, best_start = total, start
    return best_total, best_start


def shortest_burst_brute(counts: Sequence[int], target: int) -> tuple[int, int] | None:
    """Return (length, start) of the shortest window with sum >= target."""
    best: tuple[int, int] | None = None
    for start in range(len(counts)):
        total = 0
        for end in range(start, len(counts)):
            total += counts[end]
            if total >= target:
                length = end - start + 1
                if best is None or length < best[0]:
                    best = (length, start)
                break
    return best


def max_events_brute(timestamps: Sequence[float], span: float) -> int:
    """Return the most events inside any window that starts at an event."""
    best = 0
    for i, start in enumerate(timestamps):
        count = sum(1 for later in timestamps[i:] if later - start < span)
        best = max(best, count)
    return best


def longest_distinct_brute(items: Sequence[Hashable]) -> tuple[int, int]:
    """Return (length, start) of the longest run with no repeated item."""
    best_length, best_start = 0, 0
    for start in range(len(items)):
        seen: set[Hashable] = set()
        for end in range(start, len(items)):
            if items[end] in seen:
                break
            seen.add(items[end])
            if end - start + 1 > best_length:
                best_length, best_start = end - start + 1, start
    return best_length, best_start


def longest_k_distinct_brute(items: Sequence[Hashable], k: int) -> tuple[int, int]:
    """Return (length, start) of the longest run with at most k different items."""
    best_length, best_start = 0, 0
    for start in range(len(items)):
        seen: set[Hashable] = set()
        for end in range(start, len(items)):
            seen.add(items[end])
            if len(seen) > k:
                break
            if end - start + 1 > best_length:
                best_length, best_start = end - start + 1, start
    return best_length, best_start


def rate_limit_brute(
    timestamps: Sequence[float], limit: int, window: float
) -> list[bool]:
    """Decide each request by counting accepted requests from scratch."""
    accepted: list[float] = []
    decisions: list[bool] = []
    for timestamp in timestamps:
        recent = sum(1 for earlier in accepted if earlier > timestamp - window)
        if recent < limit:
            accepted.append(timestamp)
            decisions.append(True)
        else:
            decisions.append(False)
    return decisions
