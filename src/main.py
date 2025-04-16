from sys import argv

from functions import *

def main():
    basepath = "/"
    dest_dir_path = "public"
    if len(argv)>1:
        basepath = argv[1]
        dest_dir_path = "docs"
    mv_contents_static_to_(dest_dir_path)
    generate_pages_recursive("content", dest_dir_path=dest_dir_path, basepath=basepath)

if __name__ == "__main__":
    main()