from textnode import TextNode
from HTMLNode import HTMLNode
import os
import shutil

def main():
    public_path = "./public/"
    static_path = "./static/"
    static_public_copy(static_path, public_path)

def static_public_copy(src, pub):
    public_path = "./public/"
    static_path = "./static/"

    if os.path.exists(pub):
        print(f"Removing files from {public_path}")
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

def recur_copy(stat: string, pub: string):
    pass


main()

