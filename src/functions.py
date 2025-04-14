from textnode import TextType
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