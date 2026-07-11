from textnode import TextNode
from HTMLNode import HTMLNode
from text_to_node import generate_page_recursive, generate_page
import os
import shutil
import sys

def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    public_path = "./docs/"
    static_path = "./static/"
    static_public_copy(static_path, public_path)
    generate_page_recursive("content/", "template.html", public_path, basepath)

def static_public_copy(src, pub):
    if os.path.exists(pub):
        print(f"Removing files from {pub}")
        shutil.rmtree(pub)
    print("Creating dir")
    os.mkdir(pub)

    for i in os.listdir(src):
        src_path = os.path.join(src, i)
        dst_path = os.path.join(pub, i)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            static_public_copy(src_path, dst_path)



main()

