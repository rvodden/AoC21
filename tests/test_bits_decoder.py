import io
import pytest
from bits_decoder import BitsDecoder


class TestBitsDecoder:

    message_examples = [
        ("D2FE28", 6),
        ("38006F45291200", 9),
        ("EE00D40C823060", 14),
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    ]

    @pytest.mark.parametrize("message,version_sum", message_examples)
    def test_sum_versions(self, message, version_sum):
        assert BitsDecoder.sum_versions(io.StringIO(message)) == version_sum

    value_examples = [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1)
    ] 

    @pytest.mark.parametrize("message,value", value_examples)
    def test_evaluation(self, message, value):
        assert BitsDecoder.evaluate(io.StringIO(message)) == value