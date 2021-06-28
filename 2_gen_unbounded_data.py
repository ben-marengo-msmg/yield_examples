from __future__ import annotations

from collections import Iterator


def infinite_sequence() -> Iterator[int]:
    num = 0
    while True:
        yield num
        num += 1


gen = infinite_sequence()
for n in gen:
    print(n)
    if n >= 7:
        break


print("out of for loop")

print(next(gen))
print(next(gen))
print(next(gen))


# do we actually need a loop?
def silly_iterator() -> Iterator[str]:
    yield "Look, you stupid b***ard, you’ve got no arms left!"
    yield "Yes I have."
    yield "Look!"
    yield "It’s just a flesh wound"


silly = silly_iterator()
print(next(silly))
print(next(silly))
print(next(silly))
print(next(silly))
print(next(silly))
print(next(silly))
