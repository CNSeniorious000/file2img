from msgspec import Struct
from msgspec.json import decode, encode


class Metadata(Struct):
    length: int


def encode_meta(length: int):
    return encode(Metadata(length))


def decode_meta(data: bytes):
    return decode(data, type=Metadata)
