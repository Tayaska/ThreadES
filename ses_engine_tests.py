#encoding: utf-8
"""Тести: python -m unittest ses_engine_tests"""
import unittest
from ses_engine import reasoner, rule1, rule2, rule3, rule4


class T(unittest.TestCase):
    def test_transitive_full_closure(self):
        F = {(1, 2, 3), (3, 2, 4), (4, 2, 5), (5, 2, 6)}
        A = reasoner(F, [rule1], (2,))
        self.assertEqual(len(A), 10)  # 4 вихідні + 6 виведених
        self.assertIn((1, 2, 6), A)

    def test_original_example(self):
        F = {(1, 2, 3), (3, 2, 4), (5, 2, 6), (1, 0, 7), (8, 0, 9)}
        A = reasoner(F, [rule1, rule2], (2,), (0,))
        self.assertEqual(A - F, {(9, 0, 8), (1, 2, 4), (7, 0, 1)})

    def test_missing_predicate(self):
        self.assertEqual(reasoner({(1, 0, 2)}, [rule1], (99,)), {(1, 0, 2)})

    def test_inverse(self):
        A = reasoner({("a", "is", "b")}, [rule3], ("is", "has"))
        self.assertIn(("b", "has", "a"), A)

    def test_inheritance(self):
        F = {("x", "sub", "y"), ("y", "prop", "z")}
        self.assertIn(("x", "prop", "z"), reasoner(F, [rule4], ("sub", "prop")))


if __name__ == "__main__":
    unittest.main()
