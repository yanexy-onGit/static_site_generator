from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if not isinstance(self.value, str):
            raise ValueError("leaf node must have a value")
        if not isinstance(self.tag, str):
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"