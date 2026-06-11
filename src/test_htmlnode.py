import unittest
from HTMLNode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_pth(self):
        h_node = HTMLNode("T1", "v1", None, {"href":"test", "target":"pls",})
        self.assertEqual(h_node.props_to_html(), ' href="test" target="pls"')

    def test_pth2(self):
        h_node2 = HTMLNode(None, None, None, {"href":"Baka", "target":"yaroga",})
        test2 = h_node2.props_to_html()
        self.assertEqual(test2, ' href="Baka" target="yaroga"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Touch me!", {"href": "https://Fakelink.co.uk"})
        self.assertEqual(node.to_html(), '<a href="https://Fakelink.co.uk">Touch me!</a>')


if __name__ == "__main__":
    unittest.main()
