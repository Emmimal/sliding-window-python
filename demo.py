"""Run the sliding window tools on a fake request log and print a report."""

from rate_limiter import SlidingWindowRateLimiter
from sample_data import make_requests, per_minute
from sliding_window import (
    busiest_window,
    longest_distinct_run,
    longest_run_with_at_most_k_distinct,
    max_events_in_window,
    shortest_burst,
)

MINUTES = 240


def main() -> None:
    requests = make_requests(MINUTES)
    totals, errors = per_minute(requests, MINUTES)
    print(f"{len(requests):,} requests over {MINUTES} minutes")

    total, start = busiest_window(totals, 5)
    print(f"Busiest 5 minutes: minute {start} to {start + 4}, {total} requests")

    burst = shortest_burst(errors, 40)
    if burst is not None:
        length, start = burst
        print(
            f"Shortest stretch with 40+ errors: {length} minutes, "
            f"starting at minute {start}"
        )

    timestamps = [request.timestamp for request in requests]
    print(f"Most requests in any 10 seconds: {max_events_in_window(timestamps, 10)}")

    users = [request.user for request in requests]
    length, start = longest_distinct_run(users)
    print(
        f"Longest run with no repeated user: {length} requests, "
        f"starting at line {start}"
    )

    endpoints = [request.endpoint for request in requests]
    length, start = longest_run_with_at_most_k_distinct(endpoints, 2)
    print(
        f"Longest run touching at most 2 endpoints: {length} requests, "
        f"starting at line {start}"
    )

    limiter = SlidingWindowRateLimiter(limit=14, window_seconds=10)
    rejected = sum(not limiter.allow(timestamp) for timestamp in timestamps)
    print(f"Rate limiter (14 per 10 s) would reject {rejected} requests")


if __name__ == "__main__":
    main()
