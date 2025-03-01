import unittest
from main import extract_title
from block_markdown import BlockType, block_to_block_type, markdown_to_blocks

class TestExtractTitle(unittest.TestCase):
    def test_valid_title(self):
        markdown = """# My Title

Some other content
"""
        self.assertEqual(extract_title(markdown), "My Title")

    def test_title_not_first(self):
        markdown = """Some content

# My Title
"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_no_title(self):
        markdown = """## Not a title

Some content
"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_multiple_h1(self):
        markdown = """# First Title

# Second Title
"""
        self.assertEqual(extract_title(markdown), "First Title")

    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_title_with_whitespace(self):
        markdown = """#   My Title   \n\nSome content"""
        self.assertEqual(extract_title(markdown), "My Title")

    def test_title_with_special_chars(self):
        markdown = """# My Title: With Special Chars!@#$%^&*()\n\nContent"""
        self.assertEqual(extract_title(markdown), "My Title: With Special Chars!@#$%^&*()")

if __name__ == "__main__":
    unittest.main()

