from simple_parser import Parser
from prompter import Prompter


class Coder(Parser):

    def white_space(self, i=0) -> str:
        indent = self.indent
        add = i * 4
        return (indent + add) * " "

    def close_line(self) -> str:
        w = self.white_space
        text = self.text
        if self.gain < 0:
            rtn = []
            for i in range(abs(self.gain), 0, -1):
                rtn.append("\n" + w(i - 1))  # making indent. "-1" is normaliser.
                oldtag = self.tag_pop()
                template = Prompter.tag_end[oldtag]
                rtn.append(template.format(w(i), text))
            return "".join(rtn)
        if self.gain == 0:
            if self.now_tag:
                return Prompter.tag_end[self.now_tag].format(w(), text)
            elif self.befor_tag:
                return "\n"
            else:
                return Prompter.content_end[self.tag[-1]].format(w(), text)
        if self.gain > 0:
            return "\n"

    def open_line(self) -> str:
        w = self.white_space
        text = self.text
        if self.now_level == 0:
            zerotag = Prompter.marker["0"]
            return Prompter.content[zerotag].format(w(), text)
        if self.now_tag:
            return Prompter.tag[self.now_tag].format(w(), text)
        else:
            return Prompter.content[self.tag[-1]].format(w(), text)

    def code(self) -> str:
        if self.blankline():
            return ""
        code = self.close_line() + self.open_line()
        return "".join(code)

    def __str__(self) -> str:
        return super().__str__() + "\ncode:{}".format(self.code())


if __name__ == "__main__":
    Prompter()
    test = ("hello world:",
            "    heyper heyper:m",
            "        headline",
            "        payapaya",
            "    hoge",
            "end")
    for t in test:
        c = Coder(t)
        print(c)
    for t in test:
        c = Coder(t)
        print(c.code(), end="")
