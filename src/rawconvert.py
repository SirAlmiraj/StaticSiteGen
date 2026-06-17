from textnode import TextNode, TextType
import re

#splits a Markdown text 
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    final_list = []

    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            final_list.append(n)
        if delimiter not in TextType:
            raise Exception("Invalid Markdown syntax")

        sl = n.text.split(delimiter)
        temp = []
        for s in range(len(sl)):
            if (s +1) % 2 == 0:
                temp.append(TextNode(sl[s], text_type))
            else:
                temp.append(TextNode(sl[s], TextType.TEXT))
        final_list.extend(temp)

    return final_list

def extract_markdown_images(text: str):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


