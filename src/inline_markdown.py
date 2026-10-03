import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
       if node.text_type is not TextType.TEXT:
           new_nodes.append(node)
       else:
           split_nodes = []
           split_nodes.extend(node.text.split(delimiter))
           empty_free_nodes = []
           if len(split_nodes) %2 != 0:
               for index, piece in enumerate(split_nodes):
                   if piece == "":
                       continue
                   if index %2 == 0:
                       empty_free_nodes.append(TextNode(split_nodes[index], TextType.TEXT))
                   else:
                        empty_free_nodes.append(TextNode(split_nodes[index], text_type))
               new_nodes.extend(empty_free_nodes)
           else:
               raise Exception("invalid markdown, unbalanced delimiters")
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        remaning_text = f"{node.text}"
        images_alt_and_url: list[tuple] = extract_markdown_images(node.text)
        if not images_alt_and_url:
            new_nodes.append(node)
            continue
        else:
            for image_alt, image_url in images_alt_and_url:
                before, after= remaning_text.split(f"![{image_alt}]({image_url})",1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(image_alt,TextType.IMAGE, image_url))
                remaning_text = after
            if remaning_text != "":
                new_nodes.append(TextNode(remaning_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        remaning_text = f"{node.text}"
        images_alt_and_url: list[tuple] = extract_markdown_links(node.text)
        if not images_alt_and_url:
            new_nodes.append(node)
            continue
        else:
            for link_alt, link_url in images_alt_and_url:
                before, after= remaning_text.split(f"[{link_alt}]({link_url})",1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(link_alt,TextType.LINK, link_url))
                remaning_text = after
            if remaning_text != "":
                new_nodes.append(TextNode(remaning_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text)-> list[TextNode]:
    text = [TextNode(text, TextType.TEXT,None)]
    bold_text = split_nodes_delimiter(text, "**", TextType.BOLD)
    italic_text = split_nodes_delimiter(bold_text, "_", TextType.ITALIC)
    code_text = split_nodes_delimiter(italic_text, "`", TextType.CODE_TEXT)
    image_text = split_nodes_image(code_text)
    link_text = split_nodes_link(image_text)
    return link_text
