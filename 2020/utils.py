import functools
import time
from itertools import chain, combinations, zip_longest


def print_time_taken(func):
    @functools.wraps(func)
    def _wrapped_func(*args, **kwargs):
        start_time = time.time()
        retval = func(*args, **kwargs)
        time_taken = time.time() - start_time
        if time_taken > 1.0:
            time_str = f"{time_taken:.2f}s"
        elif time_taken > 0.001:
            time_str = f"{time_taken*1000:.2f}ms"
        elif time_taken > 0.000001:
            time_str = f"{time_taken*1000000:.2f}µs"
        else:
            time_str = f"{time_taken*1000000000:.2f}ns"
        print(f"Time taken: {time_str}\n")
        return retval

    return _wrapped_func


def flatten(list_of_lists):
    # flatten([ [1, 2, 3], [4, 5, 6] ]) --> 1, 2, 3, 4, 5, 6
    return chain.from_iterable(list_of_lists)


def grouper(iterable, n, fillvalue=None):
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def powerset(iterable):
    # powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
