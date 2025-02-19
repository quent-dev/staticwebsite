import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextToHTML(unittest.TestCase):
    def test_normal_text_to_html(self):
        text = TextNode("test", TextType.TEXT)
        html_node = text_node_to_html_node(text)
        self.assertEqual(
            html_node.tag , 
            None
        )
        self.assertEqual(
            html_node.value,
            "test"
        )
        self.assertEqual(
            html_node.children,
            None
        )
        self.assertEqual(
            html_node.props,
            None
        )


    def test_link_text_to_html(self):
        text = TextNode("test", TextType.LINK, "url.com")
        html_node = text_node_to_html_node(text)
        self.assertEqual(
            html_node.tag , 
            "a"
        )
        self.assertEqual(
            html_node.value,
            "test"
        )
        self.assertEqual(
            html_node.children,
            None
        )
        self.assertEqual(
            html_node.props,
            {
                "href": "url.com"
            }
        )



    def test_image_text_to_html(self):
        text = TextNode("test", TextType.IMAGE, "url.com")
        html_node = text_node_to_html_node(text)
        self.assertEqual(
            html_node.tag , 
            "img"
        )
        self.assertEqual(
            html_node.value,
            None
        )
        self.assertEqual(
            html_node.children,
            None
        )
        self.assertEqual(
            html_node.props,
            {
                "src": "url.com",
                "alt": "test"
            }
        )


    def test_invalid_text_to_html(self):
        with self.assertRaises(AttributeError):
            text = TextNode("test", TextType.OTHER, "url.com")



        
