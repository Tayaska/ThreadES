#encoding: utf-8
"""Удосконалена версія механізму виведення (example3.py).

Зміни порівняно з example3.py:
1. Виправлено помилку: правила визначали наявність нових фактів за len(d)
   (кількість предикатів), тому цикл виведення виконувався лише раз і
   транзитивне замикання було неповним. Тепер порівнюється кількість фактів.
2. Правила не падають із KeyError, якщо предиката немає в БЗ.
3. Нові правила:
   rule3 - інверсна властивість: (x,p,y)->(y,q,x)
   rule4 - успадкування властивості: (x,sub,y)&(y,p,z)->(x,p,z)
4. reasoner_explain - повертає нові факти разом із назвою правила, що їх вивело.
"""
from example3 import kb2tree, tree2kb


def _size(d):
    """Загальна кількість фактів у дереві"""
    return sum(len(v) for v in d.values())


def rule1(d, p):
    """Транзитивна властивість p: (x,p,y)&(y,p,z)->(x,p,z)"""
    if p not in d:
        return False
    n = len(d[p])
    for t in d[p].copy():
        for r in d[p].copy():
            if t[2] == r[0]:
                d[p].add((t[0], p, r[2]))
    return len(d[p]) != n


def rule2(d, p):
    """Симетрична властивість p: (x,p,y)->(y,p,x)"""
    if p not in d:
        return False
    n = len(d[p])
    for t in d[p].copy():
        d[p].add((t[2], p, t[0]))
    return len(d[p]) != n


def rule3(d, p, q):
    """Інверсна властивість: (x,p,y)->(y,q,x)"""
    if p not in d:
        return False
    d.setdefault(q, set())
    n = len(d[q])
    for t in d[p].copy():
        d[q].add((t[2], q, t[0]))
    return len(d[q]) != n


def rule4(d, sub, p):
    """Успадкування властивості p вздовж відношення sub:
    (x,sub,y)&(y,p,z)->(x,p,z)"""
    if sub not in d or p not in d:
        return False
    n = len(d[p])
    for t in d[sub].copy():
        for r in d[p].copy():
            if t[2] == r[0]:
                d[p].add((t[0], p, r[2]))
    return len(d[p]) != n


def reasoner(F, rules, *args):
    """Виводить нові факти з множини триплетів F. Цикл повторюється,
    поки виводяться нові факти. Повертає множину старих і нових фактів."""
    d = kb2tree(F)
    n = 1
    while n:
        n = 0
        for r, a in zip(rules, args):
            n += r(d, *a)
    return tree2kb(d)


def reasoner_explain(F, rules, *args):
    """Те саме, що reasoner, але повертає словник {новий_факт: назва_правила}
    (пояснення виведення)."""
    d = kb2tree(F)
    known = tree2kb(d)
    why = {}
    n = 1
    while n:
        n = 0
        for r, a in zip(rules, args):
            n += r(d, *a)
            cur = tree2kb(d)
            for t in cur - known:
                why[t] = "%s%s" % (r.__name__, a)
            known = cur
    return why


if __name__ == "__main__":
    F = {(1, 2, 3), (3, 2, 4), (4, 2, 5), (5, 2, 6), (1, 0, 7), (8, 0, 9)}
    A = reasoner(F, [rule1, rule2], (2,), (0,))
    print(sorted(A - F))
