import unittest

from textnode import TextNode, TextType
from functions import *


class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_split_nodes_delim(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text_type, new_nodes[2].text_type)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
    


if __name__ == "__main__":
    unittest.main()