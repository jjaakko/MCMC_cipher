from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, List
from custom_types import CountDict
import alphabets


def get_count(text: str, alphabets) -> DefaultDict[str, int]:
    counts: CountDict = defaultdict(lambda: 0)
    letters: str = text.strip()
    for i in range(len(letters) - 1):
        key = get_key(letters, i, alphabets)
        counts[key] += 1

    return counts


def get_key(letters: str, i: int, alphabets: List[str]):
    letter_i = letters[i] if letters[i] in alphabets else " "
    letter_j = letters[i + 1] if letters[i + 1] in alphabets else " "
    key = letter_i + letter_j
    return key


def get_count_from_file(filename: Path, language_code: str) -> defaultdict:
    counts: defaultdict = defaultdict(lambda: 0)
    alphabets_list = alphabets.get(language_code)
    with open(filename) as f:
        for line in f:
            line_stripped = line.strip().upper()
            for i in range(len(line_stripped) - 1):
                key = get_key(line_stripped, i, alphabets_list)
                counts[key] += 1
    return counts
