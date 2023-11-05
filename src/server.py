from typing import Literal

from fastapi import FastAPI, File, Response

from .core import decode, encode

app = FastAPI()


@app.post("/encode_file_to_image")
def file2img(file: bytes = File(), file_format: Literal["webp", "png"] = "png"):
    return Response(encode(file, file_format), media_type=f"image/{file_format}")


@app.post("/decode_image_to_file")
def img2file(img: bytes = File()):
    return Response(decode(img), media_type="application/octet-stream")
