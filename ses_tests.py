#encoding: utf-8
"""Тести БЗ про СЕС: python -m unittest ses_tests"""
import unittest
import ses_cards as d


class T(unittest.TestCase):
    def test_transitive(self):
        self.assertIn(("домашня мережева СЕС", "є різновидом", "сонячна електростанція"), d.ALL)

    def test_inherits_components_from_all_ancestors(self):
        e = "домашня мережева СЕС"
        for c in ("двонаправлений лічильник", "інвертор", "сонячна панель"):
            self.assertIn((e, "складається з", c), d.ALL)

    def test_no_foreign_components(self):
        self.assertNotIn(("домашня мережева СЕС", "складається з", "акумуляторна батарея"), d.ALL)

    def test_symmetric_alternative(self):
        self.assertIn(("полікристалічна панель", "альтернатива", "монокристалічна панель"), d.ALL)

    def test_inverse(self):
        self.assertIn(("інвертор", "має різновид", "мікроінвертор"), d.ALL)


if __name__ == "__main__":
    unittest.main()
