def empty(seq):
    try:
        return all(map(empty, seq))
    except TypeError:
        return False
