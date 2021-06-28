from __future__ import annotations

from collections import Iterator
from contextlib import contextmanager
from io import TextIOWrapper


@contextmanager
def writable_file(file_path: str) -> Iterator[TextIOWrapper]:
    f = open(file_path, mode="w")
    try:
        yield f
    finally:
        f.close()


with writable_file("hello.txt") as file:
    file.write("Hello, World!")



