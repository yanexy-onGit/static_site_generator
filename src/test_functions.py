import unittest

from textnode import TextNode, TextType
from functions import *


class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_split_nodes_delim(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text_type, new_nodes[2].text_type)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
    def test_extr_md_img(self):
        md = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_return = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(extract_markdown_images(md), expected_return)
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extr_md_links(self):
        md = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_return = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(extract_markdown_links(md), expected_return)
    def test_split_nodes_link(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        expected_return = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            )
        ]
        self.assertListEqual(split_nodes_link([node, node]), expected_return)
    def test_split_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_return = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected_return)

    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        md = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

            - This is the first list item in a list block
            - This is a list item
            - This is another list item
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ]
        )
    def test_block_to_block_type(self):
        md_headings = [
            "## h2 heading",
            "######      6th level heading"
        ]
        bad_headings = [
            " # not a heading",
            "##also not a heading",
            "#      \n",
            "####### there is no lvl 7 heading!!"
        ]
        for h in md_headings:
            self.assertEqual(block_to_block_type(h), BlockType.H)
        for no_h in bad_headings:
            self.assertEqual(block_to_block_type(no_h), BlockType.P)
        md_code = [
            """```
                    <html><head></head><body></body>
            ```""",
            "```\nbla\n     something\n```"
        ]
        bad_code = []
        for code in md_code:
            self.assertEqual(block_to_block_type(code), BlockType.CODE)
        for no_code in bad_code:
            self.assertEqual(block_to_block_type(no_code), BlockType.P)
        md_blockquote = [
            ">something\n> and more\n>and so on",
            "> also fiiine"
        ]
        bad_quote = [
            "> starts out well\n > but then :(",
            " > but there is no leading whitespace expected ;("
        ]
        for quote in md_blockquote:
            self.assertEqual(block_to_block_type(quote), BlockType.BQ)
        for no_quote in bad_quote:
            self.assertEqual(block_to_block_type(no_quote), BlockType.P)
        md_ul = [
            "- just one point",
            "- one line\n-  second line\n- 1\n-  ",
        ]
        bad_ul = [
            " - first point",
            "-no gap :(",
            "- gap in first line but then\n-no gap ;("
        ]
        for ul in md_ul:
            self.assertEqual(block_to_block_type(ul), BlockType.UL)
        for no_ul in bad_ul:
            self.assertEqual(block_to_block_type(no_ul), BlockType.P)
        md_ol = [
            "666. just one point",
            "1. one line\n3.  second line\n4807. 1\n6.  ",
        ]
        bad_ol = [
            " 1. first point",
            "1.no gap :(",
            "1. gap in first line but then\n2.no gap ;(",
            "0. no zero indexing"
        ]
        for ol in md_ol:
            self.assertEqual(block_to_block_type(ol), BlockType.OL)
        for no_ol in bad_ol:
            self.assertEqual(block_to_block_type(no_ol), BlockType.P)
    def test_strip_block_denotation_md(self):
        blocks_to_denotate = [
            (" nothing more than\na paragraph", BlockType.P),
            ("1. one line\n3.  second line\n4807. 1\n6.  ", BlockType.OL),
            ("- one line\n-  second line\n- 1\n-  ", BlockType.UL),
            (">something\n> and more\n>and so on", BlockType.BQ),
            ("> also fiiine", BlockType.BQ),
            ("```\nbla\n     something\n```", BlockType.CODE),
            ("## h2 heading", BlockType.H),
            ("######      6th level heading", BlockType.H),
        ]
        expected_returns = [
            " nothing more than\na paragraph",
            "one line\nsecond line\n1\n",
            "one line\nsecond line\n1\n",
            "something\n and more\nand so on",
            " also fiiine",
            "bla\n     something",
            "h2 heading",
            "6th level heading",
        ]
        returns = [strip_block_denotation_md(*inp_tup) for inp_tup in blocks_to_denotate]
        self.assertListEqual(returns, expected_returns)
    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    def test_codeblock(self):
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"
        # print(f"html as returned:\n{html}")
        # print(f"html as expected:\n" + expected_html)
        self.assertEqual(
            html,
            expected_html
        )
    def test_plentiful(self):
        md =(
            """
            # first heading

            ## 2nd heading

            ####### first paragraph
            and it goes on.

            and there is some inline `code` and nothing else
            (inside a paragraph)

            >but we can
            >also write
            >block quotes

            2. i think
            2. this turned out
            4. rather well
            666.  what do you say ?

            - but lists exist also like so
            - right?
        
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        print(f"html as returned:\n{html}")
            
        
        


if __name__ == "__main__":
    unittest.main()