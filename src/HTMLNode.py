

class HTMLNode:
    def __init__(self, tag: str | None=None, value: str | None=None, children: list | None=None, props: dict | None=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""
        return f' href="{self.props["href"]}" target="{self.props["target"]}"'

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
