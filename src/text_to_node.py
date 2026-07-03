from textnode import TextNode, TextType
from rawconvert import *

def text_to_textnode()->list[TextNode]:
    final_list = []
    start = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)

    bold = split_nodes_delimiter([start], "**", TextType.BOLD)
    final_list = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    final_list = split_nodes_delimiter(final_list, "`", TextType.CODE)
    final_list = split_nodes_image(final_list)
    final_list = split_nodes_link(final_list)
    return final_list

def markdown_to_blocks(markdown):
    final_list = []
    split_sec = markdown.split("\n\n")
    
    for section in split_sec:
        if section == "":
            continue
        clean = section.strip()
        final_list.append(clean)

    return final_list


