import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from rawconvert import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from text_to_node import *

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
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_image1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link1(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_image2(self):
        node = TextNode("Single image ![here](https://i.image.link)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("Single image ", TextType.TEXT, None), TextNode("here", TextType.IMAGES, "https://i.image.link")],
            new_nodes,
        )

    def test_t2t(self):
        result = text_to_textnode()
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINKS, "https://boot.dev"),
        ], result)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = """
# Header type

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[1])
        header = block_to_block_type(blocks[0])
        un_list = block_to_block_type(blocks[3])
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        self.assertEqual(header, BlockType.HEADING)
        self.assertEqual(un_list, BlockType.UNORDERED_LIST)

    def test_block_to_block_type2(self):
        md = """
> monkey

>monkey 2 electric boogaloo

```
coding wohoo
line1 
lime2 
end code
```

1. item1 
2. items
3. items3 
"""
        blocks = markdown_to_blocks(md)
        print(blocks)
        quote_space = block_to_block_type(blocks[0])
        quote = block_to_block_type(blocks[1])
        code_block = block_to_block_type(blocks[2])
        order = block_to_block_type(blocks[3])
        self.assertEqual([quote_space, quote], [BlockType.QUOTE, BlockType.QUOTE])
        self.assertEqual(code_block, BlockType.CODE)
        self.assertEqual(order, BlockType.ORDERED_LIST)

if __name__ == "__main__":
    unittest.main()
