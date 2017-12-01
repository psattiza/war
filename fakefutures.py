class FakeFuture():
    def __init__(self, result):
        self._result = result

    def result(self, *args, **kwargs):
        return self._result

class FakePoolExecutor():
    def __init__(self, *args, **kwargs):
        return

    def map(self, fn, *iterables, timeout=None, chunksize=1):
        return map(fn, *iterables)

    def shutdown(self, wait=True):
        return

    def submit(self, fn, *args, **kwargs):
        return FakeFuture(fn(*args, **kwargs))

    def __enter__(self, *args, **kwargs):
        return

    def __exit__(self, *args, **kwargs):
        return
