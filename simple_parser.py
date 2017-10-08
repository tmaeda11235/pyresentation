from prompter import Prompter
from typing import Union


Marker = Union[str, bool]


class Parser:
    tag = list()
    befor_tag = str()
    befor_level = int()
    now_tag = str()
    now_level = int()
    gain = int()

    def __init__(self, text: str) -> None:
        self.indent = self.init_indent(text)
        self.marker = self.init_marker(text)
        self.text = self.init_text(text, self.marker)
        if not self.blankline():
            self.update_level(self.indent, self.marker)
            self.update_gain()
            self.update_tag(self.marker)

    def init_indent(self, text: str) -> int:
        return len(text) - len(text.lstrip())

    def init_marker(self, text: str) -> int:
        split = text.split(":")
        if split[-1] in Prompter.marker.keys():
            return split[-1]
        elif split[-1] == "":
            return True
        else:
            return False

    def init_text(self, text: str, marker: Marker) -> str:
        strip = text.lstrip()
        if not marker:
            return strip
        else:
            split = strip.split(":")
            return ":".join(split[:-1])

    def blankline(self) -> bool:
        return not any((self.text, self.marker))

    @classmethod
    def update_tag(cls, marker: Marker) -> None:
        if cls.now_tag != str():
            cls.tag.append(cls.now_tag)
        cls.befor_tag = cls.now_tag
        if marker is True:
            cls.now_tag = Prompter.marker[str(cls.now_level)]
        elif isinstance(marker, str):
            cls.now_tag = Prompter.marker[marker]
        else:
            cls.now_tag = str()

    @classmethod
    def update_level(cls, indent: int, marker: Marker) -> None:
        cls.befor_level = cls.now_level
        cls.now_level = indent // 4 + bool(marker)

    @classmethod
    def update_gain(cls) -> None:
        cls.gain = cls.now_level - cls.befor_level

    @classmethod
    def tag_pop(cls):
        return cls.tag.pop()

    def __str__(self) -> str:
        param = ("text:{}".format(self.text),
                 "level:{}".format(self.now_level),
                 "gein:{}".format(self.gain),
                 "tag:{}".format(self.tag),
                 "now_tag:{}".format(self.now_tag))
        return "\n".join(param)


if __name__ == "__main__":
    Prompter()
    test = ("    hello world:",
            "     ",
            "heyper heyper",
            "headline:",
            "    hoge:i",)
    for t in test:
        print("{:=^50}".format(t))
        print(Parser(t))
