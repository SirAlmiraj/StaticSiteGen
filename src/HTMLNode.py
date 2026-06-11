

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
        if len(self.props) == 1:
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






