from collections import OrderedDict

PATH = '/home/eol/Documents/github/3sat/uuf50-218/uuf50-0133.cnf'

def read_cnf(path):
    with open(path) as f:
        d = f.readlines()
        l = [tuple([int(n) for n in line[:-2].split()]) for line in d if line[0] not in ('c', 'p', '%', '0', '\n')]
        return l

def count_vars(l):
    dv = {}
    for t in l:
        for v in t:
            dv[abs(v)] = dv.get(abs(v), 0) + 1
    return OrderedDict(sorted(dv.items(), key=lambda i: (i[1], i[0]), reverse=True))

def order_tuples(l):
    d = count_vars(l)
    l = [tuple(sorted(t, key=lambda x: d[abs(x)], reverse=True)) for t in l]
    return l

def print_cnf(l):
    c = count_vars(l)
    for k in c.keys():
        t = l[k]

def count_similar(l, n, discriminate=True, print_values=False):
    if isinstance(n, int): n = [n]
    i,j=0,0
    d = {}
    for i in range(len(l)):
        vn = 0
        for j in range(len(l)):
            if i==j:
                continue
            a = l[i]
            b = l[j]
            sa = set([x for x in a]) if discriminate else set([abs(x) for x in a])
            sb = set([x for x in b]) if discriminate else set([abs(x) for x in b])
            ic = len(sa.intersection(sb))
            if ic in n: 
                vn+=1
                if print_values: print(a, b)
        d[i] = vn
        if print_values: print('-'*30, i, d[i])
    return OrderedDict(sorted(d.items(), key=lambda i: (i[1], i[0]), reverse=True))

l = order_list(read_cnf(PATH))

