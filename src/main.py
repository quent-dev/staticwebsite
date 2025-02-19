from textnode import TextType, TextNode

def main():
    node = TextNode("This is a text node", TextType.BOLD, "google.com")
    print(node)

main()
