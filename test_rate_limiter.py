import random

import pytest

from brute_force import rate_limit_brute
from rate_limiter import SlidingWindowRateLimiter


def test_allows_up_to_the_limit_then_rejects() -> None:
    limiter = SlidingWindowRateLimiter(limit=3, window_seconds=10)
    decisions = [limiter.allow(t) for t in (0, 1, 2, 3, 4)]
    assert decisions == [True, True, True, False, False]


def test_old_requests_slide_out_of_the_window() -> None:
    limiter = SlidingWindowRateLimiter(limit=2, window_seconds=10)
    assert limiter.allow(0) is True
    assert limiter.allow(5) is True
    assert limiter.allow(9) is False
    # The request at t=0 is exactly 10 seconds old, so it no longer counts.
    assert limiter.allow(10) is True


def test_rejected_requests_do_not_use_up_the_limit() -> None:
    limiter = SlidingWindowRateLimiter(limit=1, window_seconds=10)
    assert limiter.allow(0) is True
    assert [limiter.allow(t) for t in (1, 2, 3)] == [False, False, False]
    assert limiter.allow(10) is True


def test_rejects_timestamps_that_go_backwards() -> None:
    limiter = SlidingWindowRateLimiter(limit=2, window_seconds=10)
    limiter.allow(5)
    with pytest.raises(ValueError, match="backwards"):
        limiter.allow(4)


@pytest.mark.parametrize(("limit", "window"), [(0, 10), (1, 0), (1, -5)])
def test_rejects_bad_settings(limit: int, window: float) -> None:
    with pytest.raises(ValueError):
        SlidingWindowRateLimiter(limit, window)


def test_memory_stays_bounded_by_the_limit() -> None:
    limiter = SlidingWindowRateLimiter(limit=5, window_seconds=10)
    for t in range(10_000):
        limiter.allow(t / 10)
    assert len(limiter._accepted) <= 5


def test_agrees_with_brute_force_on_random_traffic() -> None:
    rng = random.Random(8)
    for _ in range(500):
        timestamps = sorted(rng.randint(0, 60) / 2 for _ in range(rng.randint(0, 25)))
        limit = rng.randint(1, 4)
        window = rng.randint(1, 8) / 2
        limiter = SlidingWindowRateLimiter(limit, window)
        fast = [limiter.allow(t) for t in timestamps]
        assert fast == rate_limit_brute(timestamps, limit, window)
