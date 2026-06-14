from enum import Enum 
from HTMLNode import LeafNode

class TextType(Enum):
    TEXT = "" #"plain"
    BOLD = "**" #"**Boldtext**"
    ITALIC = "_" #"_Italic_"
    CODE = "`" #"`Code`"
    LINKS = "a" #"[anchor](url)"
    IMAGES = "img" #"![alt](url)"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self,other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

#Changing a text node into a html LeafNode
def text_node_to_html_node(text_node: TextNode)->LeafNode:
    # if the text node is an empty/ None node raise exception
    if text_node.text_type == None:
        raise Exception("The node doesn't exist")
    
    # match text type and return the right leaf node class
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None ,text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode(TextType.CODE.value, text_node.text, None)
        case TextType.LINKS:
            return LeafNode(TextType.LINKS.value, text_node.text, self.url)
        case TextType.IMAGES:
            return LeafNode(TextType.IMAGES.value, "", self.url)
