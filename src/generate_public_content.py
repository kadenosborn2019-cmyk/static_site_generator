import os.path
import shutil
from block_markdown import markdown_to_html_node

def static_to_public_content(src_path:str, dest_path: str):
    path_abs = os.path.abspath(src_path)
    list_dirs = os.listdir(path_abs)
    for dir in list_dirs:
        if os.path.isfile(os.path.join(path_abs, dir)):
            if os.path.exists(dest_path):
                shutil.copy(os.path.join(path_abs, dir), os.path.abspath(dest_path))
        elif os.path.isdir(os.path.join(path_abs, dir)):
           if os.path.exists(dest_path):
               os.mkdir(os.path.join(dest_path,dir))
               static_to_public_content(os.path.join(path_abs, dir), os.path.join(dest_path, dir))
           else:
               raise Exception(f"path does not exist {dest_path}")
def extract_title(markdown):
    markdown_split: list[str] = markdown.split("\n")
    for line in markdown_split:
        if line.startswith("# "):
             split_string1, split_string2 = line.split("#", 1)
             striped_string = split_string2.strip()
             return striped_string
    raise Exception("no h1 header found in file")

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(template_path) as template_path_file:
        with open(from_path) as from_path_file:
            from_path_read = from_path_file.read()
            template_path_read = template_path_file.read()
            from_path_html_node = markdown_to_html_node(from_path_read)
            from_html = from_path_html_node.to_html()
            html_title = extract_title(from_path_read)
            template_titled =template_path_read.replace("{{ Title }}", f"{html_title}" )
            template_content_filled = template_titled.replace("{{ Content }}", f"{from_html}")
            href_template_fix = template_content_filled.replace('href="/', f'href="{base_path}')
            src_template_fix = href_template_fix.replace('src="/',f'src="{base_path}')
            dest_path_abs = os.path.abspath(dest_path)
            if not os.path.exists(os.path.dirname(dest_path_abs)):
                os.makedirs(os.path.dirname(dest_path_abs))
            with open(dest_path, "w") as f:
                f.write(src_template_fix)
                f.close()
            template_path_file.close()
            from_path_file.close()
                
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for dir in os.listdir(dir_path_content):
        print(f"Found entry: {dir} in {dir_path_content}")
        if os.path.isfile(os.path.join(dir_path_content, dir)):
            if os.path.join(dir_path_content,dir).endswith(".md"):
                generate_page(os.path.join(dir_path_content,dir),template_path, (os.path.join(dest_dir_path,dir)).replace(".md", ".html"), base_path)
        else:
            generate_pages_recursive(os.path.join(dir_path_content,dir), template_path, os.path.join(dest_dir_path, dir), base_path)
            
