from collections import OrderedDict
from math import copysign
import os

PATH = './uf50-218/uf50-0133.cnf'


def abs_qtd_desc(l):
    m = {}
    for i in l:
        for j in i:
            m[abs(j)] = m.get(abs(j), 0) - 1
    return m


class CNF():

    def __init__(self, cnf=None, path=None, mapf=None):
        if not cnf and not path:
            raise Exception('Either cnf or path need to be specified')

        if path:
            self._cnf = self.read_cnf(path)
        elif cnf:
            self._cnf = cnf

        if mapf:
            self.map_var = self.map_index(mapf(self._cnf))
            self._cnf = [tuple(self.map_var[abs(j)] * int(copysign(1, j))
                               for j in i) for i in self._cnf]
        else:
            self.map_var = None

    @property
    def cnf(self):
        return self._sort_clauses(self._clause(i for i in clause)
                                  for clause in self._cnf)

    @property
    def ncnf(self):
        return self._sort_clauses(self._clause(-i for i in clause)
                                  for clause in self._cnf)

    @staticmethod
    def map_index(ld):
        d = sorted(ld.items(), key=lambda x: x[1])
        return dict([(d[i][0], i + 1) for i in range(len(d))])

    @property
    def vars(self):
        var = []
        if self.cnf:
            for i in self.cnf:
                for j in i:
                    var.append(j)
        return set(var)

    @staticmethod
    def _clause(t):
        return tuple(sorted(t, key=lambda x: abs(x)))

    @staticmethod
    def _sort_clauses(l):
        clauses = sorted(l, key=lambda x: (
            [abs(i) for i in x], [i for i in x]))
        return clauses

    def read_cnf(self, path=None):
        l = set()
        if path and os.path.exists(path):
            with open(path) as f:
                d = f.readlines()
                l = [tuple(int(n) for n in line[:-2].split())
                     for line in d if line[0] not in ('c', 'p', '%', '0', '\n')]
        return l

    def solve(self):
        pass

#     @staticmethod
#     def order(l, discriminate=True):
#         dv = {}
#         for t in l:
#             for v in t:
#                 if discriminate:
#                     dv[v] = dv.get(v, 0) + 1
#                 else:
#                     dv[abs(v)] = dv.get(abs(v), 0) + 1
#         ol = sorted(dv.items(), key=lambda i: (i[1], i[0]), reverse=True)
#         #xl = [(ol[i][0],i) for i in range(len(ol))]
#         return OrderedDict(ol)

#     def sort(self, discriminate=True):
#         l = self.cnf
#         d = self.order(self.cnf, discriminate)
#         if discriminate:
#             l = sorted([tuple(sorted(t, key=lambda x: d[x]))
#                         for t in l], key=lambda x: (d[x[0]], d[x[2]], d[x[1]]))
#         else:
#             l = sorted([tuple(sorted(t, key=lambda x: d[abs(x)])) for t in l],
#                        key=lambda x: (d[abs(x[0])], d[abs(x[1])], d[abs(x[2])]))
#             #l = sorted([tuple(sorted(t, key=lambda x: d[abs(x)])) for t in l], key=lambda x: d[abs(x[-1])])
#         return [(d[i[0]], d[i[1]], d[i[2]]) for i in l]


# def count_similar(l, n, discriminate=True, print_values=False):
#     if isinstance(n, int):
#         n = [n]
#     i, j = 0, 0
#     d = {}
#     for i in range(len(l)):
#         vn = 0
#         for j in range(len(l)):
#             if i == j:
#                 continue
#             a = l[i]
#             b = l[j]
#             sa = set([x for x in a]) if discriminate else set(
#                 [abs(x) for x in a])
#             sb = set([x for x in b]) if discriminate else set(
#                 [abs(x) for x in b])
#             ic = len(sa.intersection(sb))
#             if ic in n:
#                 vn += 1
#                 if print_values:
#                     print(a, b)
#         d[i] = vn
#         if print_values:
#             print('-' * 30, i, d[i])
#     return OrderedDict(
#         sorted(
#             d.items(),
#             key=lambda i: (
#                 i[1],
#                 i[0]),
#             reverse=True))


c = CNF(path=PATH, mapf=abs_qtd_desc)
