#encoding: utf-8
"""Візуалізація графа бази знань про СЕС (NetworkX + Matplotlib).

Вузли - суб'єкти й об'єкти фактів, дуги - предикати.
Суцільні дуги - вихідні факти, пунктирні - факти, виведені механізмом виведення.

Приклади:
    import ses_graph
    ses_graph.draw()                                    # ієрархія "є різновидом"
    ses_graph.draw(center="гібридна СЕС")               # усе про одну сутність
    ses_graph.draw(predicates=["перевага", "недолік"])  # лише переваги й недоліки
"""
import textwrap
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from ses_cards import F, why, ALL

IS_A = "є різновидом"
COLORS = ["#1f77b4", "#2ca02c", "#d62728", "#ff7f0e", "#9467bd",
          "#8c564b", "#17becf", "#7f7f7f", "#bcbd22"]


def build_graph(predicates=None, center=None, inferred=True):
    """Будує орієнтований мультиграф із фактів БЗ.
    predicates - які предикати брати (за замовчуванням тільки "є різновидом");
    center - показати лише дуги, що торкаються цієї сутності (усі предикати,
             якщо predicates не задано);
    inferred - чи додавати виведені факти (позначаються атрибутом inferred=True)."""
    facts = ALL if inferred else F
    if predicates is None and center is None:
        predicates = [IS_A]
    G = nx.MultiDiGraph()
    for s, p, o in sorted(facts):
        if predicates is not None and p not in predicates:
            continue
        if center is not None and center not in (s, o):
            continue  # для сутності беремо лише дуги, що її торкаються
        G.add_edge(s, o, key=p, predicate=p, inferred=(s, p, o) in why)
    if center is not None and center not in G:
        raise KeyError("Сутності немає в графі: %s" % center)
    return G


def layout(G, center=None, hierarchy=False):
    """Розташування вузлів: ієрархія - шарами зверху вниз, сутність - у центрі
    з сусідами по колу, інакше - силова розкладка."""
    if center is not None:
        others = sorted(n for n in G.nodes if n != center)
        return nx.shell_layout(G, nlist=[[center], others])
    if hierarchy:
        D = nx.DiGraph(G).reverse()  # корені (найзагальніші поняття) - у верхньому шарі
        if nx.is_directed_acyclic_graph(D):
            for i, gen in enumerate(nx.topological_generations(D)):
                for n in gen:
                    D.nodes[n]["layer"] = i
            pos = nx.multipartite_layout(D, subset_key="layer", align="horizontal")
            return {n: (x, -y) for n, (x, y) in pos.items()}
    return _component_grid(G)


def _component_grid(G):
    """Кожна зв'язна група фактів - в окремій клітинці сітки, щоб дуги
    не проходили позаду чужих вузлів. Ширина колонки й висота рядка
    підлаштовуються під найбільшу групу в них."""
    comps = sorted(nx.weakly_connected_components(G), key=lambda c: (-len(c), sorted(c)[0]))
    cols = max(1, round(len(comps) ** 0.5 * 1.4))

    def radius(n):  # чим більша група, тим більший радіус її розкладки
        return 1.25 * (1 + 0.35 * max(0, n - 3) ** 0.7)

    rows = (len(comps) + cols - 1) // cols
    colw = [0.0] * cols
    rowh = [0.0] * rows
    for i, c in enumerate(comps):
        w = 2 * radius(len(c)) * 1.15 + 0.9
        colw[i % cols] = max(colw[i % cols], w)
        rowh[i // cols] = max(rowh[i // cols], w)
    xs = [sum(colw[:j]) + colw[j] / 2 for j in range(cols)]
    ys = [-(sum(rowh[:j]) + rowh[j] / 2) for j in range(rows)]

    pos = {}
    for i, comp in enumerate(comps):
        H = nx.Graph(G.subgraph(comp))
        r = radius(len(H))
        if len(H) == 1:
            local = {next(iter(H)): (0.0, 0.0)}
        elif len(H) == 2:
            a_, b_ = sorted(H)
            local = {a_: (-0.6, 0.0), b_: (0.6, 0.0)}
        else:
            hub = max(sorted(H), key=H.degree)
            local = nx.spring_layout(H, seed=3, k=1.2, iterations=200, fixed=[hub],
                                     pos={hub: (0.0, 0.0)})
            m = max((x * x + y * y) ** 0.5 for x, y in local.values()) or 1.0
            local = {n: (x / m, y / m) for n, (x, y) in local.items()}  # у межах радіуса 1
        dx, dy = xs[i % cols], ys[i // cols]
        for n, (x, y) in local.items():
            pos[n] = (x * r + dx, y * r + dy)
    return pos


def draw(predicates=None, center=None, inferred=True, save=None, figsize=None):
    """Малює граф. save - ім'я файлу PNG, куди зберегти зображення."""
    G = build_graph(predicates, center, inferred)
    preds = sorted({d["predicate"] for _, _, d in G.edges(data=True)})
    color = {p: COLORS[i % len(COLORS)] for i, p in enumerate(preds)}
    hierarchy = predicates is None or list(predicates) == [IS_A]
    pos = layout(G, center, hierarchy)
    size = 5600
    if figsize is None:
        figsize = (15, 9)
        if not hierarchy and center is None and pos:  # сітка груп: розмір за площею
            xs_ = [x for x, _ in pos.values()]
            ys_ = [y for _, y in pos.values()]
            figsize = (min(24, max(12, 1.7 * (max(xs_) - min(xs_)) + 3)),
                       min(15, max(7, 1.7 * (max(ys_) - min(ys_)) + 2.5)))

    fig, ax = plt.subplots(figsize=figsize)
    node_colors = ["#ffd54f" if n == center else "#fff59d" for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=size,
                           edgecolors="#999", ax=ax)
    labels = {n: textwrap.fill(n, 15, break_long_words=False) for n in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7.5, ax=ax)
    for p in preds:
        for dashed in (False, True):
            edges = [(u, v) for u, v, d in G.edges(data=True)
                     if d["predicate"] == p and d["inferred"] == dashed]
            if edges:
                nx.draw_networkx_edges(
                    G, pos, edgelist=edges, edge_color=color[p], ax=ax,
                    style="dashed" if dashed else "solid", node_size=size,
                    arrows=True, arrowsize=14, width=1.4,
                    connectionstyle="arc3,rad=0.32" if dashed else "arc3,rad=0.08")
    handles = [Line2D([0], [0], color=color[p], lw=2, label=p) for p in preds]
    if any(d["inferred"] for _, _, d in G.edges(data=True)):
        handles += [Line2D([0], [0], color="k", lw=2, label="вихідний факт"),
                    Line2D([0], [0], color="k", lw=2, ls="--", label="виведений факт")]
    ax.legend(handles=handles, loc="upper right", fontsize=8)
    ax.set_title("Граф бази знань про СЕС" + (": %s" % center if center else ""))
    ax.margins(0.12)
    ax.axis("off")
    fig.tight_layout()
    if save:
        fig.savefig(save, dpi=130)
    plt.close(fig)  # щоб ноутбук не показував рисунок вдруге (авто-показ + значення клітинки)
    return fig


if __name__ == "__main__":
    import sys
    import matplotlib
    center = sys.argv[1] if len(sys.argv) > 1 else None
    out = "ses_graph.png"
    if "agg" not in matplotlib.get_backend().lower():
        matplotlib.use("Agg")
    draw(center=center, save=out)
    print("Збережено:", out)
