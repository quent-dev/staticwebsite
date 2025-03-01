from enum import Enum

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    blocks = []

    for line in lines:
        if len(line) > 0:
            blocks.append(line.strip())
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if not block:
        return BlockType.PARAGRAPH
    lines = block.split("\n")
    first_line = lines[0].lstrip()

    if first_line.startswith("#"):
        heading_match = first_line.split(" ", 1)
        if len(heading_match) > 1 and all(char == "#" for char in heading_match[0]) and len(heading_match[0]) <= 6:
            return BlockType.HEADING
        return BlockType.PARAGRAPH 

    if first_line.startswith("```"):
        if len(lines) >= 2 and lines[-1].strip() == "```":
            return BlockType.CODE
        return BlockType.PARAGRAPH

    if first_line.startswith(">"):
        if len(lines) == 1:
            return BlockType.QUOTE
        else:
            for line in lines[1:]:
                if not line.startswith(">"):
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE

    if first_line.startswith("* "):
        if len(lines) == 1:
            return BlockType.UNORDERED_LIST
        else:
            for line in lines [1:]:
                if not line.startswith("* "):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST

    if first_line.startswith("- "):
        if len(lines) == 1:
            return BlockType.UNORDERED_LIST
        else:
            for line in lines [1:]:
                if not line.startswith("- "):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST

    if first_line.startswith("1. "):
        if len(lines) == 1:
            return BlockType.ORDERED_LIST
        else:
            line_number = 2
            for line in lines[1:]:
                if not line.startswith(f"{line_number}. "):
                    return BlockType.PARAGRAPH
                line_number += 1
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH



