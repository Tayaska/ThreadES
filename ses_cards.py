#encoding: utf-8
"""Демо: база знань про сонячні електростанції (СЕС).
Запуск: python ses_cards.py ["назва сутності"]"""
import sys
import pandas
from ses_engine import reasoner_explain, rule1, rule2, rule3, rule4

IS_A = "є різновидом"

df = pandas.read_csv('ses_kb.csv')
F = {tuple(r) for r in df[["s", "p", "o"]].itertuples(index=False)}

rules = [rule1, rule4, rule4, rule4, rule2, rule3]
args = [(IS_A,),                          # A<B<C => A<C
        (IS_A, "складається з"),          # підтип успадковує складові
        (IS_A, "виробляє"),               # ... і що виробляє
        (IS_A, "недолік"),                # ... і недоліки
        ("альтернатива",),                # симетричність
        (IS_A, "має різновид")]           # інверсія

why = reasoner_explain(F, rules, *args)
ALL = F | set(why)


def card(entity):
    """Картка сутності: усі факти про неї (вихідні та виведені)."""
    print("\n== %s ==" % entity)
    for s, p, o in sorted(ALL, key=lambda t: (t[1], t[2])):
        if s == entity:
            mark = "  (виведено: %s)" % why[(s, p, o)] if (s, p, o) in why else ""
            print("  %s: %s%s" % (p, o, mark))


if __name__ == "__main__":
    print("Фактів у БЗ: %d, виведено нових: %d" % (len(F), len(why)))
    for e in (sys.argv[1:] or ["домашня мережева СЕС", "автономна СЕС"]):
        card(e)
