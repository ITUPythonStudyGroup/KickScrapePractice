import copy

p1 = {
    'a': 'Fun',
    'b': 'Eng',
    'd': {
        'd1': 1,
        'd3': 3
    },
    'e': "abe"
}

p2 = {
    'a': 'Fun',
    'c': 20,
    'd': {
        'd1': 1,
        'd2': 2
    },
    'e': "mad"
}

def delta(a,b):
    delta = {}
    bset = copy.deepcopy(b)
    diffSet(a,bset)
    delta['set'] = bset

    diffDelete(a,b)
    delta['delete'] = a

    return delta

# remove all a in b
def diffSet(a,b):
    for key in a.keys():
        if key in b:
            if type(b[key]) is dict:
                diffSet(a[key], b[key])
            elif b[key] != a[key]:
                b[key] = a[key]
            else:
                b.pop(key, None)

# remove all of b in a
def diffDelete(a,b):
    for key in b.keys():
        if key in a:
            if type(a[key]) is dict:
                diffDelete(a[key], b[key])
            else:
                a.pop(key, None)

print(delta(p1,p2))
