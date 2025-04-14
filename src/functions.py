from functools import reduce
from re import findall, split as regex_split

from textnode import TextType, TextNode
from leafnode import LeafNode

class TagType():
    NO_TAG = None
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "link"
    IMG = "img"

def text_node_to_html_node(text_node):
    return_dict_plain = {
        TextType.PLAIN: TagType.NO_TAG,
        TextType.BOLD: TagType.BOLD,
        TextType.ITALIC: TagType.ITALIC,
        TextType.CODE: TagType.CODE,
    }
    def get_plain_leaf(text_type):
        return LeafNode(return_dict_plain[text_type], text_node.text)
    if text_node.text_type in return_dict_plain.keys():
        return get_plain_leaf(text_node.text_type)
    match text_node.text_type:
        case TextType.LINK:
            return LeafNode(TagType.LINK, text_node.text, props={ "href": text_node.url })
        case TextType.IMG:
            return LeafNode(TagType.IMG, None, props={ "src": text_node.url, "alt": text_node.text })
    raise Exception("text_node.text_type invalid")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def split_one_node(node):
        return_nodes = []
        idx = -1
        for chunk in node.text.split(delimiter):
            idx += 1
            if not len(chunk):
                continue
            if idx % 2:
                return_nodes.append(TextNode(chunk, text_type))
            else:
                return_nodes.append(TextNode(chunk, node.text_type))
        return return_nodes
    return reduce(lambda a, b: a + b, [split_one_node(node) for node in old_nodes])

def extract_markdown_images(md):
    return findall(r"!\[([^\]]*)\]\(([^\)]+)\)", md)

def extract_markdown_links(md):
    return findall(r"(?<!!)\[([^\]]*)\]\(([^\)]+)\)", md)

def split_nodes_link(old_nodes):
    def split_one_node(node):
        return_nodes = []
        text_nodes = [TextNode(chunk, node.text_type) for chunk in regex_split(r"(?<!!)\[[^\]]*\]\([^\)]+\)", node.text)]
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

def split_nodes_image(old_nodes):
    def split_one_node(node):
        return_nodes = []
        text_nodes = [TextNode(chunk, node.text_type) for chunk in regex_split(r"!\[[^\]]*\]\([^\)]+\)", node.text)]
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
