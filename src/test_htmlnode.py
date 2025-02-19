import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode 


class TestHTMLNode(unittest.TestCase):
    def test_tag_value(self):
        node = HTMLNode("p","test paragraph" )
        self.assertEqual(
            repr(node), "HTMLNode(p, test paragraph, None, None)" 
                         )

    def test_values(self):
        node = HTMLNode("p","test paragraph" )
        self.assertEqual(
            node.tag, 
            "p"
                         )
        self.assertEqual(
            node.value, 
            "test paragraph"
                         )
        self.assertEqual(
            node.children,
            None
        )
        self.assertEqual(
            node.props,
            None
        )

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("p","test paragraph", None, props)
        self.assertEqual(
            repr(node), "HTMLNode(p, test paragraph, None, href='https://www.google.com' target='_blank')" 
                         )


class TestLeafNode(unittest.TestCase):

    def test_to_html(self):
        leaf = LeafNode("p", "test test")
        self.assertEqual(
            leaf.to_html(),
            "<p>test test</p>"
        )

    def test_raw_value(self):
        leaf = LeafNode(None,"test raw value")
        self.assertEqual(
            leaf.to_html(),
            "test raw value"
        )

    def test_value_error(self):
        leaf = LeafNode("h1", None)
        with self.assertRaisesRegex(ValueError,"all leaf nodes must have a value"):
            leaf.to_html()

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        leaf = LeafNode("h1", "Title of the blog", props)
        self.assertEqual(
            leaf.to_html(),
            "<h1 href='https://www.google.com' target='_blank'>Title of the blog</h1>"
        )


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_nestedParent_to_html(self):
        node = ParentNode(
    "p",
    [
        ParentNode("span", 
                [
                   LeafNode("p", "test level2", {
            "href": "https://www.google.com",
            "target": "_blank",
        }
),
                   LeafNode("a", "test level2 no props")
                   ]
                   ), 
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><span><p href='https://www.google.com' target='_blank'>test level2</p><a>test level2 no props</a></span>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_emptyParent_to_html(self):
        node = ParentNode(
    "p",
    [
        ParentNode("span", None),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
        )
        with self.assertRaisesRegex(ValueError, "children needed for parent node"):
            node.to_html()



if __name__ == "__main__":
    unittest.main()
