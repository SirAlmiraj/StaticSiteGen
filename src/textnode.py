from enum import Enum 

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "**Boldtext**"
    ITALIC = "_Italic_"
    CODE = "`Code`"
    LINKS = "[anchor](url)"
    IMAGES = "![alt](url)"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self,other):
        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
