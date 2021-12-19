from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
import io
from collections.abc import Generator
import operator
from re import S

class PacketType(Enum):
    SUM = auto()
    PRODUCT = auto()
    MIN = auto()
    MAX = auto()
    LITERAL = auto()
    GT = auto()
    LT = auto()
    EQ = auto()

packet_type_map: dict[str, PacketType] = {
    '000': PacketType.SUM,
    '001': PacketType.PRODUCT,
    '010': PacketType.MIN,
    '011': PacketType.MAX,
    '100': PacketType.LITERAL,
    '101': PacketType.GT,
    '110': PacketType.LT,
    '111': PacketType.EQ
}

class LengthType(Enum):
    BITS = auto()
    NUMBER = auto()

lenth_type_mapping: dict[str, LengthType] = {
    '0': LengthType.BITS,
    '1': LengthType.NUMBER
}

@dataclass
class Packet:
    version: int = None
    packet_type: PacketType = None
    length_type: LengthType = None
    length: int = None
    sub_packets: list[Packet] = None
    value: int = None


bin_hex_map = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}


class BitsDecoder:

    @staticmethod
    def _hex_to_bin(messaage: io.StringIO) -> Generator[str, None, None]:
        while char := messaage.read(1):
            yield bin_hex_map[char]

    @staticmethod
    def _read_bytes(stream: io.StringIO, bytes: int) -> str:
        return stream.read(bytes)
        
    @staticmethod
    def _bytes_to_int(str) -> int:
        return int(str, base=2)

    @staticmethod
    def _bytes_to_packet_type(bytes: str) -> PacketType:
        try:
            return packet_type_map[bytes]
        except KeyError:
            return PacketType.OPERATOR

    @staticmethod
    def _read_packet(stream: io.StreamIO) -> Packet:
        packet = Packet()
        version_string =BitsDecoder._read_bytes(stream, 3)
        if version_string == '':
            return None
        packet.version = BitsDecoder._bytes_to_int(version_string)
        packet.packet_type = BitsDecoder._bytes_to_packet_type(BitsDecoder._read_bytes(stream, 3))
        match packet.packet_type:
            case PacketType.LITERAL:
                print(f"Literal Packet version { packet.version }. ", end="")
                literal_value = ""
                continuation_bit = BitsDecoder._bytes_to_int(BitsDecoder._read_bytes(stream, 1))
                while continuation_bit:
                    literal_value += BitsDecoder._read_bytes(stream, 4)
                    continuation_bit = BitsDecoder._bytes_to_int(BitsDecoder._read_bytes(stream, 1))
                literal_value += BitsDecoder._read_bytes(stream, 4)
                packet.value = BitsDecoder._bytes_to_int(literal_value)
                print(f"Value: {packet.value}")
            case default:
                print(f"Operator Packet ({packet.packet_type}), version { packet.version }. ")
                packet.length_type = lenth_type_mapping[BitsDecoder._read_bytes(stream, 1)]
                match packet.length_type:
                    case LengthType.NUMBER:
                        number_of_packets = BitsDecoder._bytes_to_int(BitsDecoder._read_bytes(stream, 11))
                        print(f"{number_of_packets} sub-packets")
                        packet.sub_packets = []
                        while number_of_packets > 0:
                            packet.sub_packets.append(BitsDecoder._read_packet(stream))
                            number_of_packets -= 1
                    case LengthType.BITS:
                        number_of_bytes = BitsDecoder._bytes_to_int(BitsDecoder._read_bytes(stream, 15))
                        print(f"{number_of_bytes} bytes of subpackets.")
                        packet.sub_packets = []
                        packet_stream = io.StringIO(BitsDecoder._read_bytes(stream, number_of_bytes))
                        packet_stream.seek(0)
                        sub_packet = BitsDecoder._read_packet(packet_stream)
                        while sub_packet:
                            packet.sub_packets.append(sub_packet)
                            sub_packet = BitsDecoder._read_packet(packet_stream)
        return packet 

    @staticmethod
    def parse_packet(message: io.StringIO) -> Packet:
        bin_message = BitsDecoder._hex_to_bin(message)
        bin_message_stream = io.StringIO()
        for char in bin_message:
            bin_message_stream.write(char)

        bin_message_stream.seek(0)
        while char := bin_message_stream.read():
            print(char, end="")
        print()

        bin_message_stream.seek(0)
        return BitsDecoder._read_packet(bin_message_stream)

    @staticmethod
    def sum_versions(message: io.StringIO) -> int:
        packet = BitsDecoder.parse_packet(message)

        def version_sum(packet: Packet) -> int:
            retval = packet.version
            if packet.sub_packets:
                for sub_packet in packet.sub_packets:
                    retval += version_sum(sub_packet)
            return retval

        return version_sum(packet)

    @staticmethod
    def _evaluate(packet: Packet) -> int:
        print(f"Evaluate: {packet}")

        if packet.sub_packets:
                sub_packets = [BitsDecoder._evaluate(p) for p in packet.sub_packets]

        match packet.packet_type:
            case PacketType.LITERAL:
                return packet.value
            case PacketType.SUM:
                return sum(sub_packets)
            case PacketType.PRODUCT:
                return reduce(operator.mul, sub_packets, 1)
            case PacketType.MIN:
                return min(sub_packets)
            case PacketType.MAX:
                return max(sub_packets)
            case PacketType.GT:
                return 1 if sub_packets[0] > sub_packets[1] else 0
            case PacketType.LT:
                return 1 if sub_packets[0] < sub_packets[1] else 0
            case PacketType.EQ:
                return 1 if sub_packets[0] == sub_packets[1] else 0


    @staticmethod
    def evaluate(message: io.StringIO) -> int:
        packet = BitsDecoder.parse_packet(message)
        return BitsDecoder._evaluate(packet)