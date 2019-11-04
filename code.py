from collections import namedtuple
from itertools import permutations
from typing import List, Tuple
from bitstring import BitArray

from ops import get_residue, to_list, get_patterns, xor

Code = namedtuple('Code', ['encoded_len', 'data_len', 'poly'])


def encode(data: List[int], code: Code = Code(7, 4, [1, 0, 1, 1])) -> List[int]:
    assert len(data) <= code.data_len

    if len(data) < code.data_len:
        data = [0] * (code.data_len - len(data)) + data

    encoded_data = data + [0] * (code.encoded_len - code.data_len)
    # print(f'Encoded data: {encoded_data}')

    # print(data)

    residue = get_residue(encoded_data, code.poly)
    # print(f'Residue: {residue}')
    add_len = code.encoded_len - code.data_len
    encoded_data = data + residue[-add_len:]

    # print(encoded_data)
    return encoded_data


def decode(data: List[int], code: Code = Code(7, 4, [1, 0, 1, 1])) -> Tuple[List[int], bool]:
    assert len(data) == code.encoded_len

    has_error = any(get_residue(data, code.poly))
    return data[:code.data_len], has_error


def generate_noised_data(data: List[int], noise_size: int) -> List[List[int]]:
    # print('Generating noised data')
    # print(f'{data}: {noise_size}')

    # print('Getting patterns')
    # noise_patterns = list(set(permutations(base_noise)))
    noise_patterns = get_patterns(len(data), noise_size)
    # print(noise_patterns)
    # print('Got patterns')

    def noisify(noise_pattern: List[int]):
        # print(f'Noisifying using {noise_pattern}')
        return xor(data, noise_pattern)

    return [noisify(pattern) for pattern in noise_patterns]


def get_statistics(data: List[int], code: Code = Code(7, 4, [1, 0, 1, 1]), poly: List[int] = None) -> Tuple[List[int], List[int]]:
    encoded = encode(data, code)
    combinations = []
    detected = []
    for i in range(1, code.encoded_len + 1):
        noised_data = generate_noised_data(encoded, i)
        combinations.append(len(noised_data))
        for n_data in noised_data:
            dec, err = decode(n_data, code)
            if not err and i == 1:
                print(dec, err, data, n_data)
        detected.append(sum([decode(n_data, code)[1] for n_data in noised_data]))

    return combinations, detected

