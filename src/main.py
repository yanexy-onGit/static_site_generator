from sys import argv

from functions import *

def main():
    repo_name = None
    dest_dir_path = "public"
    if len(argv)>1:
        repo_name = argv[1]
        dest_dir_path = "docs"
    mv_contents_static_to_(dest_dir_path)
    generate_pages_recursive("content", dest_dir_path=dest_dir_path, repo_name=repo_name)

if __name__ == "__main__":
    main()