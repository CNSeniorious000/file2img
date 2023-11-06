from mimetypes import guess_type
from typing import Optional
from urllib.parse import quote

from fastapi import FastAPI, File, Response, UploadFile
from httpx import Client
from pydantic import HttpUrl
from starlette.middleware.cors import CORSMiddleware

from .core import Format, decode, encode

app = FastAPI()
client = Client(http2=True)


def _encode_data(data_in: bytes, file_format: str, filename: str):
    data_out = encode(data_in, file_format, filename)
    headers = {"x-size-input": str(len(data_in)), "x-size-out": str(len(data_out)), "content-disposition": f"inline; filename={quote(filename)}.{file_format}"}
    return Response(data_out, media_type=f"image/{file_format}", headers=headers)


def _decode_data(data_in: bytes):
    data, meta = decode(data_in)
    filename = meta.filename
    return Response(
        data,
        media_type=guess_type(filename)[0] if filename else "application/octet-stream",
        headers={"content-disposition": f"{'inline' if filename.startswith('text') else 'attachment'}; filename={quote(filename)}"} if filename else {},
    )


@app.post("/encode")
def file2img(file: UploadFile = File(), file_format: Format = "png"):
    data_in = file.file.read()
    return _encode_data(data_in, file_format, file.filename)


@app.post("/decode")
def img2file(img: bytes = File()):
    return _decode_data(img)


@app.get("/encode")
def url2img(url: HttpUrl, file_format: Format = "png", filename: Optional[str] = None):
    res = client.get(str(url))
    filename = filename or (res.headers.get("content-disposition") or "").split(";", 1)[-1].split("=", 1)[-1].strip('"') or str(res.url).strip("/").rsplit("/", 1)[-1]
    return _encode_data(res.read(), file_format, filename)


@app.get("/decode")
def url2file(url: HttpUrl):
    data_in = client.get(str(url), headers={"accept": "image/*"}).read()
    return _decode_data(data_in)


app.add_middleware(CORSMiddleware, allow_origins="*", allow_credentials=True, allow_methods="*", allow_headers="*")
