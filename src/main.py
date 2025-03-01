import os
import shutil
from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from markdown_to_html import markdown_to_html
from textnode import TextType, TextNode
import sys

def main(basepath):
    # Delete all files from ../public
    public_dir = os.path.join(os.path.dirname(__file__), '../docs')
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
        os.makedirs(public_dir)

    # Copy static files to public
    static_dir = os.path.join(os.path.dirname(__file__), '../static')
    if os.path.exists(static_dir):
        print(f"Copying static files from {static_dir} to {public_dir}")
        copy_static(static_dir, public_dir)
    else:
        print(f"Static directory {static_dir} does not exist")
    
    cwd = os.path.dirname(__file__)
    # Generate all pages recursively
    content_dir = os.path.join(cwd, "../content")
    template_path = os.path.join(cwd, "../template.html")
    dest_dir = os.path.join(cwd, "../docs")
    generate_pages_recursive(content_dir, template_path, dest_dir, basepath)



def copy_static(src, dst):
    """Recursively copy files from src to dst with debug prints"""
    if not os.path.exists(dst):
        os.makedirs(dst)
        print(f"Created directory: {dst}")

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isdir(src_path):
            print(f"Copying directory: {src_path} -> {dst_path}")
            copy_static(src_path, dst_path)
        else:
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy2(src_path, dst_path)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if len(blocks) == 0:
        raise Exception("Empty markdown")
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING and block.startswith("# "):
            return block[2:].strip()
        else:
            raise Exception("Markdown file has no title")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as template:
        template_content = template.read()

    html = markdown_to_html(markdown)
    title = extract_title(markdown)

    dest_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/',f'href="{basepath}').replace("src='/",f"src='{basepath}")

    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created directory: {dest_dir}")
    
    # Write the content to destination file
    with open(dest_path, "w") as file:
        file.write(dest_content)
    print(f"Successfully wrote file: {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """Recursively generate HTML pages from markdown files"""
    if not os.path.exists(dir_path_content):
        raise Exception(f"Content directory does not exist: {dir_path_content}")
    
    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
        print(f"Created destination directory: {dest_dir_path}")

    # Walk through content directory
    for root, dirs, files in os.walk(dir_path_content):
        # Calculate relative path for destination
        rel_path = os.path.relpath(root, dir_path_content)
        dest_path = os.path.join(dest_dir_path, rel_path)
        
        # Create corresponding directories in destination
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            print(f"Created directory: {dest_path}")

        # Process markdown files
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                # Change .md to .html for destination
                dest_file_path = os.path.join(dest_path, file[:-3] + ".html")
                print(f"Generating page: {from_path} -> {dest_file_path}")
                generate_page(from_path, template_path, dest_file_path, basepath)

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        basepath = "/"
    else:
        basepath = args[1]
    print(basepath)
    main(basepath)
