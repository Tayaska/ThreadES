#encoding: utf-8
"""Тести графа БЗ про СЕС: python -m unittest ses_graph_tests
(пропускаються, якщо не встановлено networkx або matplotlib)"""
import unittest

try:
    import ses_graph as g
except ImportError:
    g = None


@unittest.skipIf(g is None, "потрібні networkx і matplotlib")
class T(unittest.TestCase):
    def test_default_is_hierarchy(self):
        G = g.build_graph()
        self.assertTrue(all(d["predicate"] == "є різновидом" for _, _, d in G.edges(data=True)))
        self.assertTrue(G.has_edge("гібридна СЕС", "сонячна електростанція"))

    def test_inferred_edges_are_marked(self):
        G = g.build_graph()
        d = G.get_edge_data("домашня мережева СЕС", "сонячна електростанція")
        self.assertTrue(list(d.values())[0]["inferred"])
        d = G.get_edge_data("домашня мережева СЕС", "мережева СЕС")
        self.assertFalse(list(d.values())[0]["inferred"])

    def test_without_inferred(self):
        G = g.build_graph(inferred=False)
        self.assertFalse(G.has_edge("домашня мережева СЕС", "сонячна електростанція"))

    def test_center_only_touching_edges(self):
        G = g.build_graph(center="гібридна СЕС")
        for u, v in G.edges():
            self.assertIn("гібридна СЕС", (u, v))

    def test_unknown_center(self):
        with self.assertRaises(KeyError):
            g.build_graph(center="немає такої")


if __name__ == "__main__":
    unittest.main()
