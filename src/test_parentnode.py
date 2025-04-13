import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_value_node = LeafNode(None, "hello parent and ")
    child_node = ParentNode("span", [child_value_node, grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span>hello parent and <b>grandchild</b></span></div>",
    )


if __name__ == "__main__":
    unittest.main()