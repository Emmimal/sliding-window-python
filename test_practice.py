import random

import pytest

from practice import contains_anagram, longest_ones_after_flips, max_vowels_in_window


@pytest.mark.parametrize(
    ("text", "k", "expected"),
    [("abciiidef", 3, 3), ("aeiou", 2, 2), ("leetcode", 3, 2), ("xyz", 2, 0)],
)
def test_max_vowels_in_window(text: str, k: int, expected: int) -> None:
    assert max_vowels_in_window(text, k) == expected


def test_max_vowels_rejects_bad_k() -> None:
    with pytest.raises(ValueError):
        max_vowels_in_window("abc", 4)


@pytest.mark.parametrize(
    ("text", "pattern", "expected"),
    [
        ("eidbaooo", "ab", True),
        ("eidboaoo", "ab", False),
        ("abc", "", True),
        ("ab", "abc", False),
        ("cbaebabacd", "abc", True),
    ],
)
def test_contains_anagram(text: str, pattern: str, expected: bool) -> None:
    assert contains_anagram(text, pattern) is expected


def test_contains_anagram_agrees_with_sorting_on_random_input() -> None:
    rng = random.Random(9)
    for _ in range(500):
        text = "".join(rng.choice("abc") for _ in range(rng.randint(0, 10)))
        pattern = "".join(rng.choice("abc") for _ in range(rng.randint(0, 4)))
        k = len(pattern)
        expected = k == 0 or any(
            sorted(text[i : i + k]) == sorted(pattern) for i in range(len(text) - k + 1)
        )
        assert contains_anagram(text, pattern) is expected


@pytest.mark.parametrize(
    ("bits", "flips", "expected"),
    [
        ([1, 1, 0, 0, 1, 1, 1, 0, 0, 1], 2, 7),
        ([0, 0, 0], 0, 0),
        ([1, 1], 0, 2),
        ([], 3, 0),
    ],
)
def test_longest_ones_after_flips(bits: list[int], flips: int, expected: int) -> None:
    assert longest_ones_after_flips(bits, flips) == expected


def test_longest_ones_agrees_with_brute_force_on_random_input() -> None:
    rng = random.Random(21)
    for _ in range(500):
        bits = [rng.randint(0, 1) for _ in range(rng.randint(0, 12))]
        flips = rng.randint(0, 3)
        best = 0
        for i in range(len(bits)):
            for j in range(i, len(bits)):
                if bits[i : j + 1].count(0) <= flips:
                    best = max(best, j - i + 1)
        assert longest_ones_after_flips(bits, flips) == best
