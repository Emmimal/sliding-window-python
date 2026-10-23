"""Make a small, repeatable request log to run the sliding window tools on."""

import random
from dataclasses import dataclass

ENDPOINTS = ["/home", "/search", "/cart", "/checkout", "/login", "/api/items"]


@dataclass(frozen=True, slots=True)
class Request:
    """One line of the request log."""

    timestamp: float  # seconds since the log started
    user: int
    endpoint: str
    status: int


def make_requests(minutes: int = 240, seed: int = 42) -> list[Request]:
    """Return a fake request log, sorted by timestamp.

    Traffic is steady, with a spike around minute 100 and an incident
    from minute 150 to 159 where many requests fail.
    """
    rng = random.Random(seed)
    requests: list[Request] = []

    for minute in range(minutes):
        rate = 90 if 100 <= minute < 108 else 20
        error_chance = 0.35 if 150 <= minute < 160 else 0.02

        for _ in range(rng.randint(rate - 5, rate + 5)):
            requests.append(
                Request(
                    timestamp=minute * 60 + rng.random() * 60,
                    user=rng.randint(1, 400),
                    endpoint=rng.choice(ENDPOINTS),
                    status=500 if rng.random() < error_chance else 200,
                )
            )

    requests.sort(key=lambda request: request.timestamp)
    return requests


def per_minute(
    requests: list[Request], minutes: int = 240
) -> tuple[list[int], list[int]]:
    """Return (requests per minute, errors per minute) as two lists."""
    totals = [0] * minutes
    errors = [0] * minutes
    for request in requests:
        minute = int(request.timestamp // 60)
        totals[minute] += 1
        if request.status >= 500:
            errors[minute] += 1
    return totals, errors
