from textnode import TextNode, TextType
from rawconvert import *
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = ''
    HEADING = '#'
    CODE = '```'
    QUOTE = '>'
    UNORDERED_LIST = '-'
    ORDERED_LIST = '1.'

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





