from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE_TEXT = "code"
    LINK  = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text: str , text_type: str, url = None): 
        self.text = text  ## set to the text content of the node
        self.text_type = text_type ## the type of text that is also a memeber of the enum
        self.url = url ## the url of the image or link, if the text is a link default to none if nothing is passed in

        
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node) -> LeafNode:
     if not TextNode:
         raise ValueError("argument is not a textnode")
     match(text_node.text_type):
         case(TextType.TEXT):
             return LeafNode(None,f"{text_node.text}")
         case(TextType.BOLD):
             return LeafNode("b", f"{text_node.text}")
         case(TextType.ITALIC):
             return LeafNode("i", f"{text_node.text}")
         case(TextType.CODE_TEXT):
             return LeafNode("code", f"{text_node.text}")
         case(TextType.LINK):
             return LeafNode("a", f"{text_node.text}", {"href" :f"{text_node.url}"})
         case(TextType.IMAGE):
             return LeafNode("img", "",{"src": f"{text_node.url}", "alt":f"{text_node.text}"})
