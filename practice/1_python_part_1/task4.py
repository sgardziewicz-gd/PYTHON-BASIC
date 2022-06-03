"""
Write function which receives list of integers. Calculate power of each integer and
subtract difference between original previous value and it's power. For first value subtract nothing.
Restriction:
Examples:
    >>> calculate_power_with_difference([1, 2, 3])
    [1, 4, 7]  # because [1^2, 2^2 - (1^2 - 1), 3^2 - (2^2 - 2)]
"""
from typing import List


def calculate_power_with_difference(ints: List[int]) -> List[int]:
    powers = []
    previous_difference = [0]
    result = []

    for number in ints:
        powers.append(number**2)

    for index, number in enumerate(ints[:-1]):
        previous_difference.append(powers[index] - number)
    
    zipped = zip(powers, previous_difference)
    for powers, previous_difference in zipped:
        result.append(powers - previous_difference)
    
    return result