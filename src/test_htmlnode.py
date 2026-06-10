import unittest
from HTMLNode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_pth(self):
        h_node = HTMLNode("T1", "v1", None, {"href":"test", "target":"pls",})
        self.assertEqual(h_node.props_to_html(), ' href="test" target="pls"')

    def test_pth2(self):
        h_node2 = HTMLNode(None, None, None, {"href":"Baka", "target":"yaroga",})
        test2 = h_node2.props_to_html()
        self.assertEqual(test2, ' href="Baka" target="yaroga"')


if __name__ == "__main__":
    unittest.main()
