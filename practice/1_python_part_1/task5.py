"""
Write function which receives line of space sepparated words.
Remove all duplicated words from line.
Restriction:
Examples:
    >>> remove_duplicated_words('cat cat dog 1 dog 2')
    'cat dog 1 2'
    >>> remove_duplicated_words('cat cat cat')
    'cat'
    >>> remove_duplicated_words('cat cat cat')
    '1 2 3'
"""


def remove_duplicated_words(line: str) -> str:
    return ' '.join(sorted(set(line.split(' ')), key=line.index))