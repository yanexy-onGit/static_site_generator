from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        return (
            "" if self.props == None else reduce(lambda string, key: string + " "  + key + f'="{self.props[key]}"', self.props.keys(), "")
        ) 

    def __repr__(self):
        tag = "" if self.tag == None else self.tag
        val_part = "" if self.value == None else ' value="' + (self.value[:6] + ("..." if len(self.value) > 6 else "")) + '"'
        kids_part = "" if self.children == None else ' children="' + f'"{len(self.children)}"' + '"'
        return (
            f'<{tag}{val_part}{kids_part}{self.props_to_html()}>'
        )