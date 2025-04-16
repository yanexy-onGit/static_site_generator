import unittest

from functions import *


class TestFunctions(unittest.TestCase):    
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
        # print(f"html as returned:\n{html}")
            
        
        


if __name__ == "__main__":
    unittest.main()