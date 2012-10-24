"Combines two dicts that have the same value for a set key"
def join_dict(d1, d2, combine_func):
    resultant = {}
    keys1 = set(d1.keys())
    keys2 = set(d2.keys())

    #Get keys common to both
    common_keys = keys1.intersection(keys2)

    for key in common_keys:
        resultant[key] = combine_func(d1[key],d2[key])

    return resultant

"Add two things together with the + operator"
def add(a, b):
    return a+b
