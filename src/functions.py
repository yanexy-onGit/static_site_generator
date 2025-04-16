from os import mkdir, listdir
from os.path import exists, join, isfile
from shutil import rmtree, copy

from parentnode import ParentNode
from sub_functions import * 

def markdown_to_html_node(md):
    md_blocks = markdown_to_blocks(md)
    main_node_children = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        html_tag = block_type.value
        if block_type==BlockType.H:
            html_tag += str(len(match(r"#{1,6}", block).group()))
        text = strip_block_denotation_md(block, block_type)
        html_block_children = []
        if block_type==BlockType.OL or block_type==BlockType.UL:
            html_block_children = [ParentNode(tag="li", children=text_to_children(bullet_text)) for bullet_text in text.split("\n")]
        elif block_type==BlockType.CODE:
            main_node_children.append(ParentNode("pre", [text_node_to_html_node(TextNode(text, TextType.CODE))]))
            continue
        else:
            html_block_children = text_to_children(text)
        main_node_children.append(ParentNode(tag=html_tag, children=html_block_children))
    return ParentNode("div", children=main_node_children)

def mv_contents_static_to_public():
    public_dir_path = "public"
    rmtree(public_dir_path, ignore_errors=True)
    mkdir(public_dir_path)
    def copy_over(arg_from, arg_to):
        if not exists(arg_from) or not exists(arg_to):
            raise ValueError("invalid path")
        for node in listdir(arg_from):
            node_path = join(arg_from, node)
            if isfile(node_path):
                copy(node_path, arg_to)
            else:
                dst_dir_path = join(arg_to, node)
                mkdir(dst_dir_path)
                copy_over(node_path, dst_dir_path)
    copy_over("static", public_dir_path)




