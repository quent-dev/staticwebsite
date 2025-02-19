import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noteq_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.google.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "http://www.google.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("test", TextType.BOLD, "url.com")
        self.assertEqual(
            "TextNode(test, bold, url.com)", repr(node)
        )
        



if __name__ == "__main__":
    unittest.main()
