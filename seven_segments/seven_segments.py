import numpy as np


class SevenSegments:

    @staticmethod
    def frequency(inp: list[list[list[str]]]) -> int:
        out = sum([1 if len(j) in [2, 3, 4, 7] else 0 for i in inp for j in i[1]])
        print(out)
        return out

    @staticmethod
    def sum(inp: list[list[list[str]]]) -> int:
        retval = 0

        def _sort_sym(s: str) -> str:
            return ''.join(sorted(s))

        for row in inp:
            mapping = SevenSegments._decode([_sort_sym(r) for r in row[0]])
            retval += int(''.join([str(mapping[_sort_sym(r)]) for r in row[1]]))
        return retval

    @staticmethod
    def _decode(row: list[str]) -> dict[str, int]:
        symbol_digit_map = {}
        digit_symbol_map = {}

        # 1, 4 7 & 8 have a unique number of segments:

        def _length_to_digit(length, digit):
            # maps a string of length {length} to {digit}
            for x in row:
                if len(x) == length:
                    symbol_digit_map[x] = digit
                    digit_symbol_map[digit] = x

        # find 1:
        length_digit_map = {
            2: 1,
            4: 4,
            3: 7,
            7: 8
        }

        for length, digit in length_digit_map.items():
            _length_to_digit(length, digit)

        row = [x for x in row if len(x) not in length_digit_map.keys()]

        def _count_segments_in_common(d1: str, d2: str) -> int:
            # counts the number of characters which d1 and d2 have in common
            return sum([c in d1 for c in d2])

        def _length_and_subdigit_to_digit(length: int, subdigit, digit):
            # if symbol is of length {length} and has all of the
            # characters of the symbol associated with subdigit
            # then the symbol maps to digit
            for x in row:
                if len(x) != length:
                    continue
                if _count_segments_in_common(x, digit_symbol_map[subdigit]) == len(digit_symbol_map[subdigit]):
                    symbol_digit_map[x] = digit
                    digit_symbol_map[digit] = x
                    return

        def _length_and_not_subdigit_to_digit(length: int, subdigit, digit):
            # if symbol is of length {length} and has none of the
            # characters of the symbol associated with subdigit
            # then the symbol maps to digit
            for x in row:
                if len(x) != length:
                    continue
                if _count_segments_in_common(x, digit_symbol_map[subdigit]) < len(digit_symbol_map[subdigit]):
                    symbol_digit_map[x] = digit
                    digit_symbol_map[digit] = x
                    return

        # 3 is 5 long, and has all the 1 segments lit
        _length_and_subdigit_to_digit(5, 1, 3)
        row.remove(digit_symbol_map[3])

        # 6 is 6 long, and does not have all the 1 segments lit
        _length_and_not_subdigit_to_digit(6, 1, 6)
        row.remove(digit_symbol_map[6])

        # 9 is 6 long, and has all the 3 segments lit
        _length_and_subdigit_to_digit(6, 3, 9)
        row.remove(digit_symbol_map[9])

        # 0 is 6 long, and does not have all the 3 segments lit
        _length_and_not_subdigit_to_digit(6, 3, 0)
        row.remove(digit_symbol_map[0])

        # 5 shares 3 elements with 4

        for x in row:
            if _count_segments_in_common(x, digit_symbol_map[4]) == 3:
                symbol_digit_map[x] = 5
                digit_symbol_map[5] = x
                continue
            # otherwise its a 2
            symbol_digit_map[x] = 2
            digit_symbol_map[2] = x

        return symbol_digit_map
