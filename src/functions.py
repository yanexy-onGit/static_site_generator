from functools import reduce
from enum import Enum
from re import match, fullmatch, sub, findall, split as regex_split

from textnode import TextType, TextNode
from leafnode import LeafNode
from parentnode import ParentNode

class TagType():
    NO_TAG = None
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "link"
    IMG = "img"

class BlockType(Enum):
    P = "p"
    H = "h"
    CODE = "code"
    BQ = "blockquote"
    UL = "ul"
    OL = "ol"


# for text_to_children function
def text_node_to_html_node(text_node):
    return_dict_plain = {
        TextType.PLAIN: TagType.NO_TAG,
        TextType.BOLD: TagType.BOLD,
        TextType.ITALIC: TagType.ITALIC,
        TextType.CODE: TagType.CODE,
    }
    def get_plain_leaf(text_type):
        text = text_node.text
        if text_type != TextType.CODE:
            text = sub(r"\s+", " ", text_node.text)
        return LeafNode(return_dict_plain[text_type], text)
    if text_node.text_type in return_dict_plain.keys():
        return get_plain_leaf(text_node.text_type)
    match text_node.text_type:
        case TextType.LINK:
            return LeafNode(TagType.LINK, text_node.text, props={ "href": text_node.url })
        case TextType.IMG:
            return LeafNode(TagType.IMG, None, props={ "src": text_node.url, "alt": text_node.text })
    raise Exception("text_node.text_type invalid")

# for text_to_textnodes function
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def split_one_node(node):
        if node.text_type == TextType.IMG:
            return [node]
        return_nodes = []
        idx = -1
        for chunk in node.text.split(delimiter):
            idx += 1
            if not len(chunk):
                continue
            if idx % 2:
                return_nodes.append(TextNode(chunk, text_type))
            else:
                return_nodes.append(TextNode(chunk, node.text_type, node.url))
        return return_nodes
    return reduce(lambda a, b: a + b, [split_one_node(node) for node in old_nodes])

# for split_nodes_image function > for text_to_textnodes function
def extract_markdown_images(md):
    return findall(r"!\[([^\]]*)\]\(([^\)]+)\)", md)

# for split_nodes_link function > for text_to_textnodes function
def extract_markdown_links(md):
    return findall(r"(?<!!)\[([^\]]*)\]\(([^\)]+)\)", md)

# for text_to_textnodes function
def split_nodes_link(old_nodes):
    def split_one_node(node):
        return_nodes = []
        text_nodes = [TextNode(chunk, node.text_type, node.url) for chunk in regex_split(r"(?<!!)\[[^\]]*\]\([^\)]+\)", node.text)]
        link_tuples = extract_markdown_links(node.text)  
        for i in range(len(text_nodes)):
            t_node = text_nodes[i]
            if len(t_node.text):
                return_nodes.append(t_node)
            if i < len(link_tuples):
                link_tup = link_tuples[i]
                return_nodes.append(TextNode(link_tup[0], TextType.LINK, link_tup[-1]))
        return return_nodes
    return reduce(lambda a, b: a+b, [split_one_node(node) for node in old_nodes])

# for text_to_textnodes function
def split_nodes_image(old_nodes):
    def split_one_node(node):
        return_nodes = []
        text_nodes = [TextNode(chunk, node.text_type, node.url) for chunk in regex_split(r"!\[[^\]]*\]\([^\)]+\)", node.text)]
        img_tuples = extract_markdown_images(node.text)  
        for i in range(len(text_nodes)):
            t_node = text_nodes[i]
            if len(t_node.text):
                return_nodes.append(t_node)
            if i < len(img_tuples):
                img_tup = img_tuples[i]
                return_nodes.append(TextNode(img_tup[0], TextType.IMG, img_tup[-1]))
        return return_nodes
    return reduce(lambda a, b: a+b, [split_one_node(node) for node in old_nodes])

# for text_to_children function
def text_to_textnodes(text):
    nodes = split_nodes_link(split_nodes_image([TextNode(text, TextType.PLAIN)]))
    text_type_delim_dict = {
        TextType.BOLD: "**",
        TextType.ITALIC: "_",
        TextType.CODE: "`"
    }
    for text_t, delim in text_type_delim_dict.items():
        nodes = split_nodes_delimiter(nodes, delim, text_t)
    return nodes

# for markdown_to_html_node function
def markdown_to_blocks(md):
    return list(filter(lambda string: len(string), ["\n".join([line.strip() for line in block.strip().split("\n")]) for block in md.split("\n\n")]))

# for markdown_to_html_node function
def block_to_block_type(md_block):
    if match(r"#{1,6}\s+\S", md_block) != None:
        return BlockType.H
    if match(r"```(.|\n)*```", md_block) != None:
        return BlockType.CODE
    if fullmatch(r">.*(?:\n>.*)*", md_block) != None:
        return BlockType.BQ
    if fullmatch(r"- .*(?:\n- .*)*", md_block) != None:
        return BlockType.UL
    if fullmatch(r"[1-9]\d*\. .*(?:\n[1-9]\d*\. .*)*", md_block) != None:
        return BlockType.OL   
    return BlockType.P

# for markdown_to_html_node function
def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

# for markdown_to_html_node function
def strip_block_denotation_md(block, type):
    match type:
        case BlockType.P:
            return block
        case BlockType.OL:
            return sub(r"\n[1-9]\d*\. +", "\n", sub(r"^[1-9]\d*\. +", "", block))
        case BlockType.UL:
            return sub(r"\n- +", "\n", sub(r"^- +", "", block))
        case BlockType.BQ:
            return sub(r"\n>", "\n", sub(r"^>", "", block))
        case BlockType.CODE:
            return sub(r"^```\n", "", sub(r"\n```$", "", block))
        case BlockType.H:
            return sub(r"^#{1,6}\s+", "", block)
    raise Exception("invalid type (block_type)")

def markdown_to_html_node(md):
    md_blocks = markdown_to_blocks(md)
    main_node_children = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        html_tag = block_type.value
        if block_type==BlockType.H:
            html_tag += str(len(match(r"#{1,6}", block).group()))
        text = strip_block_denotation_md(block, block_type)
        html_block_children = []
        if block_type==BlockType.OL or block_type==BlockType.UL:
            html_block_children = [ParentNode(tag="li", children=text_to_children(bullet_text)) for bullet_text in text.split("\n")]
        elif block_type==BlockType.CODE:
            main_node_children.append(ParentNode("pre", [text_node_to_html_node(TextNode(text, TextType.CODE))]))
            continue
        else:
            html_block_children = text_to_children(text)
        main_node_children.append(ParentNode(tag=html_tag, children=html_block_children))
    return ParentNode("div", children=main_node_children)      