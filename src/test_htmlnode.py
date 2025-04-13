import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        # print("empty html node: " + str(node))
        self.assertEqual(str(node), str(node2))
    def test_diff_tag(self):
        value = "heading"
        node1 = HTMLNode(tag="h1", value=value)
        node2 = HTMLNode(tag="h2", value=value)
        # print("h1 html node: " + str(node1))
        # print("h2 html node: " + str(node1))
        self.assertNotEqual(str(node1), str(node2))
    def test_diff_props(self):
        tag = "a"
        props = { "href": "https://www.ebay.de", "target": "_blank" }
        node1 = HTMLNode(tag=tag, props=props)
        node2 = HTMLNode(tag=tag, props={ **props, "class": "event" })
        # print("props as returned by `props_to_html()` method:\n" + node2.props_to_html())
        self.assertNotEqual(node1.props_to_html, node2.props_to_html)


if __name__ == "__main__":
    unittest.main()