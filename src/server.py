from mimetypes import guess_type
from typing import Literal
from urllib.parse import quote

from fastapi import FastAPI, File, Response, UploadFile

from .core import decode, encode

app = FastAPI()


@app.post("/encode_file_to_image")
def file2img(file: UploadFile = File(), file_format: Literal["webp", "png"] = "png"):
    data_in = file.file.read()
    data_out = encode(data_in, file_format, file.filename)
    headers = {"x-size-input": str(len(data_in)), "x-size-out": str(len(data_out)), "content-disposition": f"inline; filename={quote(file.filename)}.{file_format}"}
    return Response(data_out, media_type=f"image/{file_format}", headers=headers)


@app.post("/decode_image_to_file")
def img2file(img: bytes = File()):
    data, meta = decode(img)
    filename = meta.filename
    return Response(
        data,
        media_type=guess_type(filename)[0] if filename else "application/octet-stream",
        headers={"content-disposition": f"{'inline' if filename.startswith('text') else 'attachment'}; filename={quote(filename)}"} if filename else {},
    )
