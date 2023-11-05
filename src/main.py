from pathlib import Path

from typer import Typer

from .core import file2img, img2file

app = Typer()


@app.command()
def encode(input_path: Path, output_path: Path = None, file_format: str = "png"):
    """convert a file to an image"""

    return file2img(input_path, output_path or input_path.with_suffix(f".{file_format}"), file_format)


@app.command()
def decode(input_path: Path, output_path: Path):
    """convert an image to a file"""

    return img2file(input_path, output_path)


if __name__ == "__main__":
    app()
