from msgspec import Struct
from msgspec.json import decode, encode


class Metadata(Struct, omit_defaults=True):
    length: int
    filename: str | None = None


def encode_meta(length: int, filename: str | None = None):
    return encode(Metadata(length, filename))


def decode_meta(data: bytes):
    return decode(data, type=Metadata)
