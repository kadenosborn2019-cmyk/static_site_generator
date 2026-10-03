import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        htmlnode = HTMLNode("<a>", None, None, {
    "href": "https://www.google.com",
    "target": "_blank",
})
        htmlnode2 = HTMLNode("<a>", None, None, {
    "href": "https://www.google.com",
    "target": "_blank",
})
        self.assertEqual(htmlnode, htmlnode2)


    def test_HTMLNode_default_is_None(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )


    def test_not_eq(self):
        node = HTMLNode("<a>", "test anchor string", None, )
        node2 = HTMLNode("<h>", "test anchor string", None, )
        self.assertNotEqual(node,node2)


    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})"
        )


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


    def test_leaf_to_html_empty_tag(self):
        node = LeafNode("", "this is some anchor text")
        self.assertEqual(node.to_html(), "this is some anchor text")


    def test_leaf_to_html_none_tag(self):
        node = LeafNode(None, "this is some anchor text")
        self.assertEqual(node.to_html(),"this is some anchor text")

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


    def test_to_html_with_no_children(self):
        parent_node = ParentNode("p",[])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_multiple_children(self):
        child_node = LeafNode("span","child")
        grand_child = LeafNode("b", "grandchild")
        child2_node = ParentNode("span",[grand_child])
        parent_node = ParentNode("div",[child_node, child2_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span><span><b>grandchild</b></span></div>",
        )

        
if __name__ == "__main__":
    unittest.main()
