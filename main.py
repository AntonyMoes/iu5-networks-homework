from ops import get_residue, xor
from code import Code, encode, decode, get_statistics, generate_noised_data
from typing import List


def print_statistics(data: List[int], code: Code = Code(7, 4, [1, 0, 1, 1])):
    print('| Error size | Combinations | Detected | Detection capability |')
    print('|------------|--------------|----------|----------------------|')
    for i, (combinations, detected) in enumerate(zip(*get_statistics(data, code))):
        print('| {:^10} | {:^12} | {:^8} | {:^20.3f} |'.format(i + 1, combinations, detected, detected / combinations))


def test():
    assert xor([1, 1, 0, 1], [1, 0, 0, 1]) == [0, 1, 0, 0]
    assert get_residue([0, 1, 1, 1, 0, 0, 0], [1, 0, 1, 1]) == [0, 0, 1, 0]

    data = [0, 1, 1, 1]
    encoded = encode(data)

    assert encoded == [0, 1, 1, 1, 0, 1, 0]
    assert encode([1, 1, 1]) == [0, 1, 1, 1, 0, 1, 0]

    decoded, err = decode(encoded)
    assert (decoded, err) == (data, False)

    # assert set(generate_noised_data([0, 0, 1], 1)) == {[1, 0, 1], [0, 1, 1], [0, 0, 0]}

    # code = Code(15, 11, [1, 0, 0, 1, 1])
    # data = [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]
    # print(data)
    #
    # encoded = encode(data, code)
    #
    # n_encoded = encoded.copy()
    # n_encoded[10] = 0
    # print(encoded)
    # print(n_encoded)
    #
    # print(get_residue(encoded, code.poly))
    # print(get_residue(n_encoded, code.poly))
    #
    # print(decode(encoded, code))
    # print(decode(n_encoded, code))


if __name__ == '__main__':
    # test()

    data = [0, 1, 1, 1]
    print_statistics(data, code=Code(7, 4, [1, 0, 1, 1]))

    # print()
    #
    # data_additional = [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]
    # print_statistics(data_additional, code=Code(15, 11, [1, 0, 0, 1, 1]))




