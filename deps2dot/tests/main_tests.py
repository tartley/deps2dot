from unittest import TestCase

from deps2dot.main import get_node, get_tree


class MainTest(TestCase):

    def test_get_node_empty(self):
        root = {}
        self.assertIs(
            get_node(root, []),
            root
        )

    def test_get_node_toplevel(self):
        one = {}
        root = {'a': one}
        self.assertIs(
            get_node(root, ['a']),
            one
        )

    def test_get_tree_one_module_one_package(self):
        self.assertEqual(
            get_tree([
                (('root', 'a.py'), (None, None)),
                (('root', 'b'), (None, None)),
            ]),
            {
                'a.py': None,
                'b': {},
            }
        )

    def test_get_tree_module_in_a_package(self):
        self.assertEqual(
            get_tree([
                (('root', 'a'), (None, None)),
                (('root', 'a/b.py'), (None, None)),
            ]),
            {
                'a': {
                    'b.py': None,
                },
            }
        )

    def test_get_tree_nested_packages(self):
        self.assertEqual(
            get_tree([
                (('root', 'a.py'), (None, None)),
                (('root', 'b'), (None, None)),
                (('root', 'b/c.py'), (None, None)),
                (('root', 'b/d'), (None, None)),
                (('root', 'b/d/e.py'), (None, None)),
                (('root', 'b/f.py'), (None, None)),
                (('root', 'g.py'), (None, None)),
            ]),
            {
                'a.py': None,
                'b': {
                    'c.py': None,
                    'd': {
                        'e.py': None,
                    },
                    'f.py': None,
                },
                'g.py': None,
            }
        )

