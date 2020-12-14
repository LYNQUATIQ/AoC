from itertools import chain, combinations, zip_longest


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
