class HTMLTag:
    """A convenience class for creating HTML tags, can be used in a with statement, which will close the tag."""

    def __init__(self, parent: "HTML", tag: str, closing: bool = True, **kwargs):
        self.parent = parent
        self.tag = tag
        self.closing = closing
        self.kwargs = kwargs
        attributes = "".join(f' {k}="{v}"' for k, v in self.kwargs.items())
        self.parent.push(f"<{self.tag}{attributes}>", depth=self.closing)

    def __enter__(self):
        pass

    def __exit__(self, *args):
        if self.closing:
            self.parent.push(f"</{self.tag}>", depth=-self.closing)


class HTML:
    """A convenience class to create HTML code, in order be able to close the tags and add the necessary syntax.

    Originally, this was used a lot more, however at this point it is only needed for a single with statement.
    """

    tags: list[str] = []
    depth = 0

    def push(self, tag: str, depth=0):
        if depth < 0:
            self.depth += depth
        self.tags.append("  " * self.depth + tag)
        if depth > 0:
            self.depth += depth

    def tag(self, tag: str, closing: bool = True, **kwargs):
        return HTMLTag(self, tag, closing, **kwargs)

    def __str__(self):
        return "\n".join(self.tags)
