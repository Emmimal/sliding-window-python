# Sliding Window Technique in Python

[![tests](https://github.com/Emmimal/sliding-window-python/actions/workflows/tests.yml/badge.svg)](https://github.com/Emmimal/sliding-window-python/actions/workflows/tests.yml)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

Companion code for the tutorial **[Sliding Window Technique in Python: Complete Guide](https://emitechlogic.com/sliding-window-technique-in-python/)** on EmiTechLogic.

The tutorial builds a small monitoring toolkit for a request log. Every function is tested against a slow brute-force version on thousands of random inputs, and every speed claim is measured.

![A window of size 3 sliding across the list 2, 1, 5, 1, 3, 2. At each of four steps, one number enters on the right and one leaves on the left, and the sum updates from 8 to 7, then 9, then 6.](images/window-diagram.svg)

## What's inside

| File | What it does |
|---|---|
| `sliding_window.py` | The toolkit: fixed windows, `deque` generators, variable windows, time windows, and distinct-item windows |
| `rate_limiter.py` | `SlidingWindowRateLimiter`, a rate limiter built on a `deque` |
| `sample_data.py` | Builds a repeatable fake request log (steady traffic, a spike, and an incident) |
| `brute_force.py` | Slow, obviously correct versions. They are the speed baseline and the test oracle |
| `pitfalls.py` | Deliberately buggy versions, kept so the tests can show how they fail |
| `practice.py` | Solutions to the three practice problems |
| `demo.py` | Runs every tool on the sample log and prints a report |
| `benchmark.py` | Times the sliding window against the alternatives |
| `test_*.py` | The `pytest` suite (78 tests) |

The toolkit functions:

| Function | Window type | Question it answers |
|---|---|---|
| `busiest_window(counts, size)` | Fixed | Which `size` neighbors have the largest sum? |
| `windows(iterable, size)` | Fixed, streaming | Yield every window from any iterable, holding only `size` items |
| `moving_average(values, size)` | Fixed, streaming | Average of every window of a stream |
| `shortest_burst(counts, target)` | Variable | Shortest stretch whose sum reaches `target` |
| `max_events_in_window(timestamps, span)` | Variable, by time | Most events inside any `span` seconds |
| `longest_distinct_run(items)` | Variable, dictionary | Longest run with no repeated item |
| `longest_run_with_at_most_k_distinct(items, k)` | Variable, `Counter` | Longest run with at most `k` different items |
| `SlidingWindowRateLimiter(limit, window_seconds).allow(t)` | Variable, by time | May this request go through? |

## Requirements

Python 3.12 or later. The code uses the `def windows[T](...)` generics syntax from Python 3.12. It has no runtime dependencies, and `pytest` is the only thing you need to run the tests.

It is tested in CI on Python 3.12, 3.13, 3.14 and 3.15.

## Quick start

```console
$ git clone https://github.com/Emmimal/sliding-window-python.git
$ cd sliding-window-python
$ python -m venv venv
$ source venv/bin/activate
(venv) $ python -m pip install -r requirements.txt
(venv) $ python -m pytest
```

On Windows, activate the environment with `venv\Scripts\activate` instead.

## Try it

```pycon
>>> from sliding_window import busiest_window, shortest_burst, windows
>>> busiest_window([2, 1, 5, 1, 3, 2], 3)
(9, 2)
>>> shortest_burst([2, 3, 1, 2, 4, 3], 7)
(2, 4)
>>> list(windows("ABCDE", 3))
[('A', 'B', 'C'), ('B', 'C', 'D'), ('C', 'D', 'E')]
```

`busiest_window` returns `(total, start)`, so `(9, 2)` means the best window sums to 9 and starts at index 2. `shortest_burst` returns `(length, start)`, or `None` when no window reaches the target.

A rate limiter that allows 3 requests in any 10 seconds:

```pycon
>>> from rate_limiter import SlidingWindowRateLimiter
>>> limiter = SlidingWindowRateLimiter(limit=3, window_seconds=10)
>>> [limiter.allow(t) for t in (0, 1, 2, 3, 10)]
[True, True, True, False, True]
```

## Run the demo

```console
(venv) $ python demo.py
5,375 requests over 240 minutes
Busiest 5 minutes: minute 101 to 105, 457 requests
Shortest stretch with 40+ errors: 7 minutes, starting at minute 150
Most requests in any 10 seconds: 28
Longest run with no repeated user: 67 requests, starting at line 2798
Longest run touching at most 2 endpoints: 9 requests, starting at line 849
Rate limiter (14 per 10 s) would reject 163 requests
```

The request log uses a fixed random seed, so you should see exactly this output. The numbers match the story built into the data: a traffic spike at minutes 100 to 107, and an incident with many errors from minute 150.

## Run the benchmark

```console
(venv) $ python benchmark.py
```

Here is one run on Python 3.14:

```text
Busiest window: recompute vs sliding (window = half the data)
      n    size   recompute  sliding window
  5,000   2,500     0.0367s       0.000234s
 10,000   5,000     0.1490s       0.000448s
 20,000  10,000     0.6000s       0.000637s
 40,000  20,000     2.3256s       0.001542s
```

Your times will differ, and single runs are noisy, so treat the shape as the result. Each time `n` doubles, recomputing every window takes about four times as long (O(n²) when the window grows with the data), while the sliding window grows roughly in step with `n`.

The benchmark also compares three ways to compute a moving average and checks floating-point drift. See the tutorial for what those show.

## How the tests work

Every fast function is checked three ways:

1. **Examples** from the tutorial.
2. **Edge cases**: empty input, one item, a window the size of the whole input, ties, and no valid window.
3. **Random comparison against brute force**, using `random.Random(seed)` with a fixed seed, so a failure is reproducible and shows the same input every time.

The tests in `test_pitfalls.py` do the opposite: they show buggy versions failing, such as the shrinking window returning a wrong answer when numbers can be negative.

## Design notes

- **`shortest_burst` rejects negative numbers** with a `ValueError`. The standard shrinking rule assumes that dropping an item never raises the total. With negative numbers that is false, and the loop silently returns a wrong answer. For data that can be negative, use a prefix sum with a dictionary.
- **`windows` checks its arguments at the call**, not at the first iteration. It is a normal function that returns a generator, so a bad `size` raises right away.
- **`SlidingWindowRateLimiter` keeps at most `limit` timestamps**, so memory use does not grow with traffic. It expects timestamps in non-decreasing order and raises `ValueError` otherwise.

## Development

Install the dev tools and run the same checks as CI:

```console
(venv) $ python -m pip install -e ".[dev]"
(venv) $ python -m pytest
(venv) $ ruff check .
(venv) $ ruff format --check .
(venv) $ mypy
```

`mypy` runs in `--strict` mode.

## Project layout

```text
sliding-window-python/
├── .github/workflows/tests.yml
├── images/
│   ├── window-diagram.svg
│   ├── deque-window-diagram.svg
│   ├── variable-window-diagram.svg
│   └── negative-numbers-diagram.svg
├── sample_data.py
├── sliding_window.py
├── rate_limiter.py
├── brute_force.py
├── pitfalls.py
├── practice.py
├── benchmark.py
├── demo.py
├── test_sliding_window.py
├── test_rate_limiter.py
├── test_pitfalls.py
├── test_practice.py
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

## Related reading

- [Two Pointers in Python: A Complete Problem-Solving Guide](https://emitechlogic.com/two-pointers-in-python/), the previous article in the series
- [Data Structures & Algorithms with Python](https://emitechlogic.com/data-structures-and-algorithms-with-python/), the full roadmap
- [`itertools` recipes](https://docs.python.org/3/library/itertools.html), including the `sliding_window()` recipe that `windows()` is based on

## License

[MIT](LICENSE) © 2026 Emmimal P. Alexander
