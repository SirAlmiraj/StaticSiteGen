

class HTMLNode:
    def __init__(self, tag: str | None=None, value: str | None=None, children: list | None=None, props: dict | None=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        #makes the html link from the given props dict
        if self.props == None:
            return ""
        if len(self.props) == 2:
            return f' href="{self.props["href"]}" target="{self.props["target"]}"'

        return f' href="{self.props["href"]}"'


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None=None, value: str | None=None, props: dict | None=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("LeafNode must have value")
        if self.tag == None:
            return self.value

        html_string: str = None
        if self.props == None:
            html_string = f"<{self.tag}>{self.value}</{self.tag}>"
            return html_string
        else:
            link = self.props_to_html()
            html_string = f"<{self.tag}{link}>{self.value}</{self.tag}>"
            return html_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict | None=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        final_str = ""
        if self.tag == None:
            raise ValueError("Parent requires a tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("Parent requires children")
        for c in self.children:
            final_str += c.to_html()
        return f"<{self.tag}>{final_str}</{self.tag}>"




