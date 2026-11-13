"""COUNT THE LETTERS — frequency analysis of substitution ciphers.

WHEN TO TRY: Each plaintext letter is always replaced by the same symbol.
Frequency gives CLUES, not an automatic, guaranteed solution.

Use the attached English wordlist if you want to estimate letter frequencies.
Then compare patterns and experiment with your own letter mapping.
"""

from collections import Counter
from pathlib import Path

CIPHERTEXT = (
    "qnb{vsi-fihczlnb-dlyi-vsi-fibv-plaahib-fi-zv-l-"
    "hzici-plaahi-mr-l-frtbbihb-plaahi}"
)
WORDLIST = Path(__file__).resolve().parent / "data" / "wordlist.txt"


def letter_frequencies(text):
    # Ignore punctuation and treat UPPER/lowercase as the same letter.
    letters = [letter.lower() for letter in text if letter.isascii() and letter.isalpha()]
    counts = Counter(letters)
    total = len(letters)
    if total == 0:
        return []

    return [(letter, round(100 * count / total, 2))
            for letter, count in counts.most_common()]


def apply_my_guesses(ciphertext, guesses):
    # Example guesses: {'q':'c', 'n':'n', 'b':'s'}.
    # Don't overwrite letters that still have no guess.
    return "".join(guesses.get(letter, letter.upper()) for letter in ciphertext)


def main():
    print("CIPHERTEXT frequencies:")
    print(letter_frequencies(CIPHERTEXT))

    if WORDLIST.exists():
        print("\nComputing ENGLISH frequencies from the wordlist...")
        with WORDLIST.open("r", encoding="utf-8", errors="ignore") as file:
            english_frequencies = letter_frequencies(file.read())
        print(english_frequencies)

    # Fill this dict when you have evidence from word shapes.
    # For example, the first three cipher letters qnb may represent cns.
    guesses = {"q": "c", "n": "n", "b": "s"}
    print("\nCurrent guesses (unmapped letters UPPERCASE):")
    print(apply_my_guesses(CIPHERTEXT, guesses))


if __name__ == "__main__":
    main()
