"""Time the sliding window tools against the obvious alternatives."""

import math
import random
from collections import deque
from collections.abc import Callable
from time import perf_counter

from brute_force import busiest_window_brute
from sliding_window import busiest_window, moving_average


def timed(func: Callable[..., object], *args: object) -> float:
    """Return how many seconds one call to func(*args) takes."""
    start = perf_counter()
    func(*args)
    return perf_counter() - start


def moving_average_slices(values: list[int], size: int) -> list[float]:
    """Recompute every window from a slice."""
    return [sum(values[i : i + size]) / size for i in range(len(values) - size + 1)]


def moving_average_indexes(values: list[int], size: int) -> list[float]:
    """Running total with index arithmetic."""
    total = sum(values[:size])
    averages = [total / size]
    for right in range(size, len(values)):
        total += values[right] - values[right - size]
        averages.append(total / size)
    return averages


def report_recompute_vs_sliding() -> None:
    print("Busiest window: recompute vs sliding (window = half the data)")
    print(f"{'n':>7}  {'size':>6}  {'recompute':>10}  {'sliding window':>14}")
    for n in (5_000, 10_000, 20_000, 40_000):
        size = n // 2
        counts = list(range(n))
        slow = timed(busiest_window_brute, counts, size)
        fast = timed(busiest_window, counts, size)
        print(f"{n:>7,}  {size:>6,}  {slow:>9.4f}s  {fast:>13.6f}s")


def moving_average_stream(values: list[int], size: int) -> list[float]:
    """The deque generator, collected into a list so it can be timed."""
    return list(moving_average(values, size))


def report_moving_average_styles() -> None:
    print()
    print("Moving average over 200,000 values: three ways")
    print(f"{'size':>6}  {'slices':>9}  {'indexes':>9}  {'deque generator':>15}")
    values = list(range(200_000))
    for size in (10, 100, 1_000):
        slices = timed(moving_average_slices, values, size)
        indexes = timed(moving_average_indexes, values, size)
        stream = timed(moving_average_stream, values, size)
        print(f"{size:>6,}  {slices:>8.4f}s  {indexes:>8.4f}s  {stream:>14.4f}s")


def report_float_drift() -> None:
    print()
    print("Float drift after 1,000,000 updates (window of 100)")
    rng = random.Random(1)
    values = [rng.random() * 1000 for _ in range(1_000_000)]
    size = 100
    window: deque[float] = deque(maxlen=size)
    total = 0.0
    for value in values:
        if len(window) == size:
            total -= window[0]
        window.append(value)
        total += value
    print(f"running total: {total!r}")
    print(f"exact total:   {math.fsum(window)!r}")


if __name__ == "__main__":
    report_recompute_vs_sliding()
    report_moving_average_styles()
    report_float_drift()
