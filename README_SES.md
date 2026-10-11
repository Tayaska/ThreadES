# Експертна система: сонячні електростанції (СЕС)

База знань про СЕС у вигляді триплетів (суб'єкт, предикат, об'єкт) і механізм логічного виведення нових фактів. Побудовано на основі проєкту [ThreadES](https://github.com/vkopey/ThreadES).

## Файли
- `ses_kb.csv` - база знань про СЕС: типи (мережева, автономна, гібридна), склад, інвертори, типи панелей, переваги й недоліки.
- `ses_engine.py` - удосконалений механізм виведення. Виправлено помилку з `example3.py` (нові факти визначались за кількістю предикатів, тому цикл виконувався лише раз). Правила: `rule1` транзитивність, `rule2` симетричність, `rule3` інверсія, `rule4` успадкування властивості; `reasoner_explain` повертає пояснення виведення.
- `ses_cards.py` - виведення нових фактів і "картка сутності" з поясненням.
- `ses_graph.py` - граф бази знань (NetworkX + Matplotlib): суцільні дуги - вихідні факти, пунктирні - виведені.
- `ses_graph_tests.py` - тести графа.
- `ses_graph_*.png` - приклади готових зображень графа.
- `ses_tests.py` - тести бази знань про СЕС.
- `ses_engine_tests.py` - тести механізму виведення.
- `example3.py` - оригінальний модуль з ThreadES (потрібен, бо з нього імпортуються `kb2tree` і `tree2kb`).

## Запуск
```
python ses_cards.py "гібридна СЕС"
python -m unittest ses_tests ses_engine_tests ses_graph_tests
python ses_graph.py                 # зберігає ses_graph.png
python ses_graph.py "гібридна СЕС"  # граф однієї сутності
```
Граф потребує `networkx` і `matplotlib` (`pip install networkx matplotlib`).
У JupyterLite (https://jupyter.org/try-jupyter/lab/): перетягніть усі файли в File Browser і виконайте в ноутбуці
```python
import ses_cards
ses_cards.card("гібридна СЕС")
```
Граф у ноутбуці (спершу `%pip install networkx matplotlib`):
```python
import ses_graph
ses_graph.draw()                                      # ієрархія типів СЕС
ses_graph.draw(center="гібридна СЕС")                 # усе про одну сутність
ses_graph.draw(predicates=["перевага", "недолік"])    # переваги й недоліки
```
