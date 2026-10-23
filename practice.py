"""Practice problems for the sliding window technique."""

from collections import Counter


def max_vowels_in_window(text: str, k: int) -> int:
    """Return the most vowels in any substring of length k."""
    vowels = set("aeiou")
    if k <= 0 or k > len(text):
        raise ValueError("k must be between 1 and len(text)")

    count = sum(1 for char in text[:k] if char in vowels)
    best = count

    for right in range(k, len(text)):
        if text[right] in vowels:
            count += 1
        if text[right - k] in vowels:
            count -= 1
        best = max(best, count)

    return best


def contains_anagram(text: str, pattern: str) -> bool:
    """Return True if some window of text is an anagram of pattern."""
    k = len(pattern)
    if k == 0:
        return True
    if k > len(text):
        return False

    need = Counter(pattern)
    window = Counter(text[:k])
    if window == need:
        return True

    for right in range(k, len(text)):
        window[text[right]] += 1
        leaving = text[right - k]
        window[leaving] -= 1
        if window[leaving] == 0:
            del window[leaving]
        if window == need:
            return True

    return False


def longest_ones_after_flips(bits: list[int], flips: int) -> int:
    """Return the longest run of 1s after flipping at most `flips` zeros."""
    left = 0
    zeros = 0
    best = 0

    for right, bit in enumerate(bits):
        if bit == 0:
            zeros += 1
        while zeros > flips:
            if bits[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)

    return best
