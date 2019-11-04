from typing import List
from bitstring import BitArray


def get_residue(divident: List[int], divider: List[int]):
    assert divider[0] != 0
    dlen = len(divider)

    pos = 0
    arr = divident[:dlen]

    def shift():
        new_arr = arr[1:]
        new_arr.append(divident[pos + dlen - 1])
        return new_arr

    while pos + dlen <= len(divident):
        # print(f'Gotta do {arr} ^ {divider}')

        new_arr = xor(arr, divider)
        if new_arr[0] != 1:
            # print(f'Division succussful: {new_arr}')
            arr = new_arr

        pos += 1
        if pos + dlen <= len(divident):
            arr = shift()

    return arr


def xor(a: List[int], b: List[int]):
    return [x ^ y for x, y in zip(a, b)]


def to_list(arr: BitArray) -> List[int]:
    return list(map(int, list(arr)))


def get_patterns(size: int, error_size: int) -> List[List[int]]:
    patterns = []
    for i in range(2 ** size):
        pattern = BitArray(uint=i, length=size)
        if pattern.count(1) == error_size:
            patterns.append(to_list(pattern))

    return patterns
