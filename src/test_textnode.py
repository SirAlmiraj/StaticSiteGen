import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from rawconvert import split_nodes_delimiter, extract_markdown_images

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node that is diff", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_urlne(self):
        node = TextNode("The URL man", TextType.BOLD, "https://something.com")
        node2 = TextNode("The URL man", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("Italian text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italian text")

    def test_split_bold(self):
        node = TextNode("Testing the **bold** split!", TextType.TEXT)
        split_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_node, [TextNode("Testing the ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" split!", TextType.TEXT)])

    def test_split_italic(self):
        node = TextNode("Testing the _italic_ split!", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_node, [TextNode("Testing the ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" split!", TextType.TEXT)])

    def test_split_multi(self):
        node1 = TextNode("First `code` test!", TextType.TEXT)
        node2 = TextNode("Second `italic` test!", TextType.TEXT)
        node3 = TextNode("Third `bold` test!", TextType.TEXT)
        
        answer = [TextNode("First ", TextType.TEXT), TextNode("code", TextType.CODE), 
                  TextNode(" test!", TextType.TEXT), TextNode("Second ", TextType.TEXT), 
                  TextNode("italic", TextType.CODE), TextNode(" test!", TextType.TEXT), 
                  TextNode("Third ", TextType.TEXT), TextNode("bold", TextType.CODE), 
                  TextNode(" test!", TextType.TEXT)]

        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        self.assertEqual(new_nodes, answer)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_images("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

if __name__ == "__main__":
    unittest.main()
