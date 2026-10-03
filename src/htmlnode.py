

class HTMLNode():
    def __init__(
        self,
        tag: str|None = None,
        value:str|None= None,
        children: list["HTMLNode"]|None= None,
        props: dict[str,str]|None= None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")


    def props_to_html(self) -> str:
        if not self.props:
            return ""
        html_string:str = ""
        for key, value in self.props.items():
            html_string += (f' {key}="{value}"')
        return html_string


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        else:
            return False

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value,None, props)

    def to_html(self):
        if self.value is None :
            raise ValueError("Leaf Node has no value parameter")

        elif not self.tag:
            return f"{self.value}"

        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"], props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("no tag argument provided")
        if not self.children:
            raise ValueError("no children argument provided")
        html_string = ""
        for node in self.children:
            html_string += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
