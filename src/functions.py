from os import mkdir, listdir
from os.path import exists, join, isfile
from shutil import rmtree, copy
from re import search, sub
from functools import reduce

from parentnode import ParentNode
from sub_functions import * 

def generate_pages_recursive(dir_path_content="content", template_path="template.html", dest_dir_path="public", basepath="/"):
    md_path_file_tups = []
    def crawl_for_md_files(dir):
        for node in listdir(dir):
            node_path = join(dir, node)
            if isfile(node_path):
                if search(r"\.md", node) != None:
                    md_path_file_tups.append((sub(r"^[^/]*/?", "", dir), node_path))
            else:
                crawl_for_md_files(node_path)
    crawl_for_md_files(dir_path_content)
    for dir_path, file in md_path_file_tups:
        generate_page(file, template_path, join(dest_dir_path, dir_path), basepath)

def generate_page(from_path, template_path="template.html", dest_path="public/index.html", basepath="/"):
    if not exists(from_path):
        raise Exception("'from_path' invalid")
    if not exists(template_path):
        raise Exception("'template_path' invalid")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = template = None
    with open(from_path) as md_file:
        md = md_file.read()
    html_content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    with open(template_path) as template_file:
        template = template_file.read()
    full_html = sub(r"\{\{ Title \}\}", title, sub(r"\{\{ Content \}\}", html_content, template))
    dest_dir_path = reduce(lambda tail, head: (
            len(join(tail, head)) and (exists(join(tail, head)) or print(f"creating: {join(tail, head)}") or mkdir(join(tail, head))),
            join(tail, head)
        )[-1],
        sub(r"[^/]*\.\S*$", "", dest_path.strip("/")).split("/"),
        ""
    )
    html_file_name = (search(r"[^/]+\.html$", dest_path) or search(r"", "")).group() or "index.html"
    with open(join(dest_dir_path, html_file_name), "w") as html_file:
        html_file.write(full_html)

def markdown_to_html_node(md):
    md_blocks = markdown_to_blocks(md)
    main_node_children = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        html_tag = block_type.value
        if block_type==BlockType.H:
            html_tag += str(len(match(r"#{1,6}", block).group()))
        text = strip_block_denotation_md(block, block_type).strip(" ")
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

def mv_contents_static_to_(dest_dir_path="public"):
    rmtree(dest_dir_path, ignore_errors=True)
    mkdir(dest_dir_path)
    def copy_over(arg_from, arg_to):
        if not exists(arg_from) or not exists(arg_to):
            raise ValueError("invalid path")
        for node in listdir(arg_from):
            node_path = join(arg_from, node)
            if isfile(node_path):
                print(f"moving {node_path}")
                copy(node_path, arg_to)
            else:
                dst_dir_path = join(arg_to, node)
                mkdir(dst_dir_path)
                copy_over(node_path, dst_dir_path)
    copy_over("static", dest_dir_path)

def extract_title(md):
    search_title_res = search(r"(?m)(?<=^# )[^\n$]*", md)
    if search_title_res==None:
        raise Exception("no title")
    return search_title_res.group()