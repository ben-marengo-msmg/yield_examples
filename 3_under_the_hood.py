class MyInfiniteIterator:
    def __init__(self, start_at: int = 0, end_at: int = 0):
        self.n = start_at
        self.end_at = end_at

    def __next__(self):
        self.n = self.n + 1
        if self.n > self.end_at:
            raise StopIteration()

        return self.n

    def __iter__(self):
        return self


inf_iter = MyInfiniteIterator(5, 10)


print(list(inf_iter))

