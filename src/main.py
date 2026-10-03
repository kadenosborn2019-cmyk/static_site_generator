from textnode import TextNode, TextType
import os.path
import shutil
from generate_public_content import static_to_public_content, generate_pages_recursive

def main():
    print("Hello world")
    test_node = TextNode("This is some anchor text",TextType.LINK, "https://www.boot.dev")
    print(test_node)
    dest_path = "./public"
    src_path = "./static"
    if os.path.exists("/home/kaden/Projects/static_site_generator/public"):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    static_to_public_content(src_path, dest_path)
    from_path = "./content"
    template_path = "./template.html"
    dest_path_html = "./public/"
    generate_pages_recursive(from_path, template_path, dest_path_html)
    
if __name__ == "__main__":
    main()
