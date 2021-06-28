from __future__ import annotations

from typing import List, Iterator


def read_file(file_name: str) -> List[str]:
    file = open(file_name)
    result = file.read().split("\n")
    return result


txt = read_file('file.txt')

print(txt)

# what if file was larger than the amount of memory you have?


# can create a generator
def generate_file_rows(file_name: str) -> Iterator[str]:
    for row in open(file_name, "r"):
        yield row


txt = generate_file_rows('file.txt')

print(txt)
print(list(txt))

# what if we call it again?
print(list(txt))
