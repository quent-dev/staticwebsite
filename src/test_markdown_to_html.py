import unittest
from markdown_to_html import markdown_to_html

class TestMarkdownToHTML(unittest.TestCase):
    def test_heading(self):
        markdown = "# Heading 1"
        expected = "<h1>Heading 1</h1>"
        self.assertEqual(markdown_to_html(markdown), expected)

    def test_paragraph(self):
        markdown = "This is a paragraph"
        expected = "<p>This is a paragraph</p>"
        self.assertEqual(markdown_to_html(markdown), expected)

    def test_bold_text(self):
        markdown = "This is **bold** text"
        expected = "<p>This is <b>bold</b> text</p>"
        self.assertEqual(markdown_to_html(markdown), expected)

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2"
        expected = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        self.assertEqual(markdown_to_html(markdown), expected)

    def test_ordered_list(self):
        markdown = "1. First\n2. Second"
        expected = "<ol><li>First</li><li>Second</li></ol>"
        self.assertEqual(markdown_to_html(markdown), expected)

    def test_code_block(self):
        markdown = "```\ncode block\n```"
        expected = "<code>code block</code>"
        self.assertEqual(markdown_to_html(markdown), expected)


    def test_quote(self):
        markdown = "> This is a quote"
        expected = "<blockquote>This is a quote</blockquote>"
        self.assertEqual(markdown_to_html(markdown), expected)

    def test_mixed_content(self):
        markdown = """# Heading

This is a paragraph with **bold** text

- Item 1
- Item 2

> Quote"""
        expected = """<h1>Heading</h1><p>This is a paragraph with <b>bold</b> text</p><ul><li>Item 1</li><li>Item 2</li></ul><blockquote>Quote</blockquote>"""
        self.assertEqual(markdown_to_html(markdown), expected)


    
if __name__ == "__main__":
    unittest.main()

