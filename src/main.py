from sys import argv

from functions import *

def main():
    dest_dir_path = len(argv)>1 and "docs" or "public"
    mv_contents_static_to_(dest_dir_path)
    generate_pages_recursive("content", dest_dir_path=dest_dir_path)

if __name__ == "__main__":
    main()