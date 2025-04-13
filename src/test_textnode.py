import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_diff_text(self):
        text1, text2 = ("bla", "cha")
        node1 = TextNode(text1, TextType.PLAIN)
        node2 = TextNode(text2, TextType.PLAIN)
        self.assertNotEqual(node1, node2)
    def test_diff_text_type(self):
        text_type1, text_type2 = (TextType.PLAIN, TextType.BOLD)
        node1 = TextNode("text", text_type1)
        node2 = TextNode("text", text_type2)
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()