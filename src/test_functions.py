import unittest

from functions import *


class TestFunctions(unittest.TestCase):
    def test_extract_title(self):
        md = [
            "# this is my title\n# and second one",
            "`code`\n\nsome other paragraph\n\n#  my title",
            "## second level heading \n\n# title"
        ]
        bad_md = []
        expected_return = [
            "this is my title",
            " my title",
            "title"
        ]
        for i in range(len(md)):
            self.assertEqual(extract_title(md[i]), expected_return[i])
        for string in md:
            extract_title(string)
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
    def test_example(self):
        example_md = (
            """
            # Tolkien Fan Club

            ![JRR Tolkien sitting](/images/tolkien.png)

            Here's the deal, **I like Tolkien**.

            > "I am in fact a Hobbit in all but size."
            >
            > -- J.R.R. Tolkien

            ## Blog posts

            - [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
            - [Why Tom Bombadil Was a Mistake](/blog/tom)
            - [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

            ## Reasons I like Tolkien

            - You can spend years studying the legendarium and still not understand its depths
            - It can be enjoyed by children and adults alike
            - Disney _didn't ruin it_ (okay, but Amazon might have)
            - It created an entirely new genre of fantasy

            ## My favorite characters (in order)

            1. Gandalf
            2. Bilbo
            3. Sam
            4. Glorfindel
            5. Galadriel
            6. Elrond
            7. Thorin
            8. Sauron
            9. Aragorn

            Here's what `elflang` looks like (the perfect coding language):

            ```
            func main(){
                fmt.Println("Aiya, Ambar!")
            }
            ```

            Want to get in touch? [Contact me here](/contact).

            This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev).
            """
        )
        node = markdown_to_html_node(example_md)
        html = node.to_html()
        print(html)
            
        
        


if __name__ == "__main__":
    unittest.main()