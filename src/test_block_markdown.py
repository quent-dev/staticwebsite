import unittest
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type


class BlockTest(unittest.TestCase):
    def test_simple_block(self):
        document = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
        """

        self.assertListEqual(
            markdown_to_blocks(document),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
        )
        

    def test_heading_blocks(self):
        # Test different heading levels
        test_cases = [
            ("# Heading 1", BlockType.HEADING),
            ("## Heading 2", BlockType.HEADING),
            ("### Heading 3", BlockType.HEADING),
            ("#### Heading 4", BlockType.HEADING),
            ("##### Heading 5", BlockType.HEADING),
            ("###### Heading 6", BlockType.HEADING),
        ]
        
        for test_input, expected in test_cases:
            with self.subTest(test_input=test_input):
                self.assertEqual(block_to_block_type(test_input), expected)
    
    def test_code_blocks(self):
        # Test valid code blocks
        test_cases = [
            ("```\ncode here\n```", BlockType.CODE),
            ("```python\ndef hello():\n    print('Hello')\n```", BlockType.CODE),
            # Test code block that should be treated as paragraph
            ("```\nunclosed code block", BlockType.PARAGRAPH),
            ("```\ncode here\n", BlockType.PARAGRAPH),
        ]
        
        for test_input, expected in test_cases:
            with self.subTest(test_input=test_input):
                self.assertEqual(block_to_block_type(test_input), expected)
    
    def test_quote_blocks(self):
        # Test valid quote blocks
        test_cases = [
            ("> Single line quote", BlockType.QUOTE),
            ("> First line\n> Second line\n> Third line", BlockType.QUOTE),
            # Test quotes that should be treated as paragraphs
            ("> First line\nSecond line without >", BlockType.PARAGRAPH),
            ("> Mixed quote\nNormal text", BlockType.PARAGRAPH),
        ]
        
        for test_input, expected in test_cases:
            with self.subTest(test_input=test_input):
                self.assertEqual(block_to_block_type(test_input), expected)
    
    def test_paragraph_blocks(self):
        # Test regular paragraphs
        test_cases = [
            ("Regular paragraph text", BlockType.PARAGRAPH),
            ("Multiple line\nparagraph text", BlockType.PARAGRAPH),
            ("Text with #but not at start", BlockType.PARAGRAPH),
            ("Text with > but not at start", BlockType.PARAGRAPH),
            ("Text with ```but not properly formatted```", BlockType.PARAGRAPH),
        ]
        
        for test_input, expected in test_cases:
            with self.subTest(test_input=test_input):
                self.assertEqual(block_to_block_type(test_input), expected)

    def test_unordered_lists_asterisk(self):
        test_cases = [
            # Single item list
            ("* Single item", BlockType.UNORDERED_LIST),
            
            # Multi-item list
            ("* First item\n* Second item\n* Third item", BlockType.UNORDERED_LIST),
            
            # Invalid formats
            ("*No space", BlockType.PARAGRAPH),
            ("* First item\nSecond item", BlockType.PARAGRAPH),
            ("* First item\n - Mixed markers", BlockType.PARAGRAPH),
            ("* First item\n*No space", BlockType.PARAGRAPH),
        ]
        for test_input, expected in test_cases:
            with self.subTest(test_input=test_input):
                self.assertEqual(block_to_block_type(test_input), expected)

    def test_unordered_lists_hyphen(self):
        test_cases = [
            # Single item list
            ("- Single item", BlockType.UNORDERED_LIST),
            
            # Multi-item list
            ("- First item\n- Second item\n- Third item", BlockType.UNORDERED_LIST),
            
            # Invalid formats
            ("-No space", BlockType.PARAGRAPH),
            ("- First item\nSecond item", BlockType.PARAGRAPH),
            ("- First item\n* Mixed markers", BlockType.PARAGRAPH),
            ("- First item\n-No space", BlockType.PARAGRAPH),
        ]
        for test_input, expected in test_cases:
            with self.subTest(test_input=test_input):
                self.assertEqual(block_to_block_type(test_input), expected)

    def test_ordered_lists(self):
        test_cases = [
            # Single item list
            ("1. Single item", BlockType.ORDERED_LIST),
            
            # Multi-item list
            ("1. First item\n2. Second item\n3. Third item", BlockType.ORDERED_LIST),
            
            # Invalid formats
            ("1.No space", BlockType.PARAGRAPH),
            ("1. First item\nSecond item", BlockType.PARAGRAPH),
            ("1. First item\n3. Wrong number", BlockType.PARAGRAPH),
            ("1. First item\n2.No space", BlockType.PARAGRAPH),
            ("2. Starting with wrong number", BlockType.PARAGRAPH),
        ]
        for test_input, expected in test_cases:
            with self.subTest(test_input=test_input):
                self.assertEqual(block_to_block_type(test_input), expected)

    def test_list_edge_cases(self):
        test_cases = [
            # Empty list items
            ("* ", BlockType.UNORDERED_LIST),
            ("- ", BlockType.UNORDERED_LIST),
            ("1. ", BlockType.ORDERED_LIST),
            
            # Lists with blank lines (should be paragraphs)
            ("* First\n\n* Second", BlockType.PARAGRAPH),
            ("- First\n\n- Second", BlockType.PARAGRAPH),
            ("1. First\n\n2. Second", BlockType.PARAGRAPH),
            
            # Mixed list styles (should be paragraphs)
            ("* First\n- Second", BlockType.PARAGRAPH),
            ("- First\n* Second", BlockType.PARAGRAPH),
            ("1. First\n* Second", BlockType.PARAGRAPH),
            
            # Invalid ordered list numbers
            ("1. First\n3. Third", BlockType.PARAGRAPH),
            ("2. Wrong start", BlockType.PARAGRAPH),
            ("1. First\n2. Second\n2. Duplicate", BlockType.PARAGRAPH),
        ]
        for test_input, expected in test_cases:
            with self.subTest(test_input=test_input):
                self.assertEqual(block_to_block_type(test_input), expected)

