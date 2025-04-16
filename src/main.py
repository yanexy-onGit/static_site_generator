from functions import *

def main():
    mv_contents_static_to_public()
    generate_pages_recursive("content")

if __name__ == "__main__":
    main()