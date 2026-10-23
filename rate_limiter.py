"""A sliding window rate limiter built on a deque."""

from collections import deque


class SlidingWindowRateLimiter:
    """Allow at most `limit` requests in any `window_seconds` stretch of time."""

    def __init__(self, limit: int, window_seconds: float) -> None:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
        self.limit = limit
        self.window_seconds = window_seconds
        self._accepted: deque[float] = deque()
        self._latest = float("-inf")

    def allow(self, timestamp: float) -> bool:
        """Return True and record the request if it fits in the window."""
        if timestamp < self._latest:
            raise ValueError("timestamps must not go backwards")
        self._latest = timestamp

        # Drop requests that have slid out of the window. Each request is
        # added once and removed at most once, so this stays cheap.
        cutoff = timestamp - self.window_seconds
        while self._accepted and self._accepted[0] <= cutoff:
            self._accepted.popleft()

        if len(self._accepted) < self.limit:
            self._accepted.append(timestamp)
            return True
        return False
