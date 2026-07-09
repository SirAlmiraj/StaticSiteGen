from textnode import TextNode, TextType, text_node_to_html_node
from HTMLNode import HTMLNode, ParentNode, LeafNode
from rawconvert import *
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = ''
    HEADING = '#'
    CODE = '```'
    QUOTE = '>'
    UNORDERED_LIST = '-'
    ORDERED_LIST = '1.'

def text_to_textnode(start)->list[TextNode]:
    final_list = []
    start = TextNode(start, TextType.TEXT)

    bold = split_nodes_delimiter([start], "**", TextType.BOLD)
    final_list = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    final_list = split_nodes_delimiter(final_list, "`", TextType.CODE)
    final_list = split_nodes_image(final_list)
    final_list = split_nodes_link(final_list)
    return final_list

def markdown_to_html_node(markdown):
    block_list = []
    blocks = markdown_to_blocks(markdown)

    for b in blocks:
        block_type = block_to_block_type(b)
        match block_type:
            case BlockType.PARAGRAPH:
                temp_split = b.split('\n')
                b = " ".join(temp_split)
                children = text_to_children(b)
                html_node = ParentNode('p', children, None)
            case BlockType.HEADING:
                b = b.strip(BlockType.Heading.value)
                children = text_to_children(b)
                num_heading = count_heading(b)
                html_node = ParentNode(f"h{num_heading}", children, None)
            case BlockType.QUOTE:
                children = []
                clean_line = []
                lines = b.split('\n')
                for l in lines:
                    clean_line.append(l.strip(BlockType.QUOTE.value))
                final_line = " ".join(clean_line)
                children = text_to_children(final_line)
                html_node = ParentNode('blockquote', children, None)
            case BlockType.UNORDERED_LIST:
                items = b.split('\n')
                parent_list = []
                for i in items:
                    children = text_to_children(i.strip(BlockType.UNORDERED_LIST))
                    parent = ParentNode('li', children, None)
                    parent_list.append(parent)
                html_node = ParentNode('ul', parent_list, None)
            case BlockType.ORDERED_LIST:
                items = b.split('\n')
                parent_list = []
                for i in items:
                    children = text_to_children(i[3:])
                    parent = ParentNode('li', children, None)
                    parent_list.append(parent)
                html_node = ParentNode('ol', parent_list, None)
            case BlockType.CODE:
                b = b.strip('```')
                code_text = TextNode(b[1:], TextType.CODE)
                code_html_node = text_node_to_html_node(code_text)
                #child = LeafNode('code', code_html_node, None)
                html_node = ParentNode('pre', [code_html_node], None)
        block_list.append(html_node)

    return ParentNode('div', block_list, None)


def text_to_children(text: string):
    final_list = []
    list_text_node = text_to_textnode(text)
    for t in list_text_node:
        final_list.append(text_node_to_html_node(t))
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

def block_to_block_type(block):
    local_type = ""
    check = block[:2]

    count = 0
    for c in block:
        if c == '#':
            count += 1
        elif c == ' ' and count < 7:
            return BlockType.HEADING
        elif count > 6 or c != "#":
            count = 0
            break

    if block[:3] == '```' and block[(len(block)-3):] == '```':
        return BlockType.CODE

    elif block[0] == ">" or check == "> ":
        return BlockType.QUOTE

    hold = block.split('\n')
    for s in hold:
        if s[:2] != '- ':
            break
        count += 1
        if count == len(hold):
            count = 0
            return BlockType.UNORDERED_LIST

    count = 0
    for s in hold:
        if s[:3] == f"{count+1}. ":
            count += 1
            if count == len(hold):
                return BlockType.ORDERED_LIST
            continue
        break

    return BlockType.PARAGRAPH

def count_heading(heading: string):
    count = 0
    for c in heading:
        if c == '#':
            count += 1
        elif c == ' ' and count < 7:
            return count
        elif count > 6 or c != "#":
            raise Exception("This is not a heading")





