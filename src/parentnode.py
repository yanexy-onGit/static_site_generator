from collections.abc import Iterable
from functools import reduce

from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if not isinstance(self.tag, str):
            raise ValueError("parent node must include a html tag")
        if not isinstance(self.children, Iterable) or not len(self.children):
            raise ValueError("parent node must have a non-empty list of children")
        return f"<{self.tag}{self.props_to_html()}>{reduce(lambda a, b: a+b.to_html(), self.children, "")}</{self.tag}>"