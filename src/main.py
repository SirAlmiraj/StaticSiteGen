from textnode import TextNode
from HTMLNode import HTMLNode

def main():
    test_node = TextNode("This is some achor text", "link", "https://www.boot.dev")
    print(test_node)
    props = {"href":"nono", "target": "Yesyes",}
    test_html = HTMLNode("Borgor", "69", None, props)
    print(test_html)


main()

