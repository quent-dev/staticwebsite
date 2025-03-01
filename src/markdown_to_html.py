from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import  LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_html(document):
    html_nodes = []
    html = ""
    # Split doc into blocks
    blocks = markdown_to_blocks(document)

    for block in blocks:
        block_type = block_to_block_type(block)
        html_nodes.append(block_to_html(block, block_type))
        
    for node in html_nodes:
        if node is not None:
            html += node.to_html()
                

    return html

def text_to_children(text):
    match block_to_block_type(text):
        case BlockType.UNORDERED_LIST:
            lines = text.split("\n")
            children = [line[2:] for line in lines]

        case BlockType.ORDERED_LIST:
            lines = text.split("\n")
            children = [line[3:] for line in lines]

        case BlockType.PARAGRAPH:
            text_nodes = text_to_textnodes(text)
            children = [ text_node_to_html_node(node) for node in text_nodes]

    return children
            




def block_to_html(block, block_type):
    lines = block.split("\n")
    match block_type:
        case BlockType.HEADING:
            heading_marker = block.split(" ",1)
            heading_level = len(heading_marker[0])
            return LeafNode(f"h{heading_level}", heading_marker[1])
 
        case BlockType.QUOTE:
            lines = [line[2:] for line in lines]
            return LeafNode("blockquote","\n".join(lines))

        case BlockType.CODE:
            return LeafNode("code", "\n".join(lines[1:-1]))

        case BlockType.UNORDERED_LIST:
            children = text_to_children(block)
            children_nodes = [ParentNode("li", text_to_children(child)) for child in children]
            return ParentNode("ul", children_nodes)

        case BlockType.ORDERED_LIST:
            children = text_to_children(block)
            children_nodes = [ParentNode("li", text_to_children(child)) for child in children]
            return ParentNode("ol", children_nodes)

        case BlockType.PARAGRAPH:
            children = text_to_children(block)
            return ParentNode("p", children)

        
markdown_test = """
# heading 1

paragraph with **bolded text** and 
line returns

- unorderedlsit1
- unorderedlist2
"""

#print(markdown_to_html(markdown_test))

