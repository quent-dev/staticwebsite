class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        stri = ""
        if self.props is not None:
            for prop in self.props:
                stri += " " + prop + "=" + "'" + self.props[prop]+ "'"
            return stri
        return " None"

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children},{self.props_to_html()})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html() if self.props is not None else ""}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag needed for parent node")
        if self.children is None:
            raise ValueError("children needed for parent node")
        else:
            innerText = ""
            for child in self.children:
                innerText += child.to_html()
            return f"<{self.tag}{self.props_to_html() if self.props is not None else ""}>{innerText}</{self.tag}>"

