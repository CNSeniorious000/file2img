from math import ceil
from pathlib import Path
from typing import Literal

import numpy as np
from imageio.v3 import imread, imwrite

from .metadata import decode_meta, encode_meta


def encode(data, file_format: Literal["png", "webp"], filename: str | None = None):
    data = encode_meta(len(data), filename) + b"\n" + data
    length = len(data)

    img_size = ceil((length / 3) ** 0.5)

    buffer = np.zeros((img_size, img_size, 3), np.uint8)
    buffer.ravel()[:length] = np.frombuffer(data, dtype=np.uint8)

    return imwrite("<bytes>", buffer, extension=f".{file_format}", lossless=True)


def decode(data):
    meta, data = bytes(imread(data)).split(b"\n", 1)

    meta = decode_meta(meta)

    return data[: meta.length], meta


def file2img(path_in: Path, path_out: Path, file_format: Literal["png", "webp"]):
    data = path_in.read_bytes()
    path_out.write_bytes(encode(data, file_format, path_in.name))


def img2file(path_in: Path, path_out: Path | None):
    data, meta = decode(path_in.read_bytes())
    (path_out or Path(meta.filename)).write_bytes(data)
