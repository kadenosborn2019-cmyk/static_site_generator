import os.path
import shutil
import sys

from generate_public_content import static_to_public_content, generate_pages_recursive

def main():
    arg = sys.argv
    if len(arg) > 1:
        basepath = arg[1]
    else:
        basepath = "/"

    dest_path = "./docs"
    src_path = "./static"
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    static_to_public_content(src_path, dest_path)
    from_path = "./content"
    template_path = "./template.html"
    dest_path_html = "./docs"
    generate_pages_recursive(from_path, template_path, dest_path_html, basepath)
    
if __name__ == "__main__":
    main()
