import unittest
from HTMLNode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multi_children(self):
        child_1 = LeafNode("i", "Eldest")
        child_2 = LeafNode("b", "Middle")
        child_3 = LeafNode("span", "Youngest")
        parent_node = ParentNode("p", [child_1, child_2, child_3])
        self.assertEqual(parent_node.to_html(), "<p><i>Eldest</i><b>Middle</b><span>Youngest</span></p>")

if __name__ == "__main__":
    unittest.main()
