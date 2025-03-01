from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            split_text = node.text.split(delimiter)

            if len(split_text) % 2 == 0:
                raise Exception("invalid Markdown delimiter")
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(split_text[i],TextType.TEXT))
                else:
                    split_nodes.append(TextNode(split_text[i],text_type))
            new_nodes.extend(split_nodes)

    return new_nodes
                

def extract_markdown_images(text):
    alt_pattern = r"!\[(.*?)\]"
    url_pattern = r"\((.*?)\)"

    alt_matches = re.findall(alt_pattern, text)
    url_matches = re.findall(url_pattern, text)

    return list(zip(alt_matches, url_matches))

def extract_markdown_link(text):
    alt_pattern = r"\[(.*?)\]"
    url_pattern = r"\((.*?)\)"

    alt_matches = re.findall(alt_pattern, text)
    url_matches = re.findall(url_pattern, text)

    return list(zip(alt_matches, url_matches))

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_info = extract_markdown_images(node.text)
        if len(image_info) == 0:
            new_nodes.append(node)
        else:
            text_to_parse= node.text
            for image in image_info:
                sections = text_to_parse.split(f"![{image[0]}]({image[1]})",1)
                if len(sections[0]) > 0:
                    new_nodes.append(TextNode(sections[0],TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE,image[1]))
                text_to_parse = sections[1]
            if text_to_parse != "":
                new_nodes.append(TextNode(text_to_parse, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_info = extract_markdown_link(node.text)
        if len(link_info) == 0:
            new_nodes.append(node)
        else:
            text_to_parse= node.text
            for link in link_info:
                sections = text_to_parse.split(f"[{link[0]}]({link[1]})",1)
                if len(sections[0]) > 0:
                    new_nodes.append(TextNode(sections[0],TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK,link[1]))
                text_to_parse = sections[1] 
            if text_to_parse != "":
                new_nodes.append(TextNode(text_to_parse, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes



