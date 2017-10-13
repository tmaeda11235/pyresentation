from csv import DictReader
from os.path import exists, abspath, dirname, join
from typing import Dict


TagDict = Dict[str, str]


class Template:
    markers = dict()  # type: TagDict
    tag_begin = dict()  # type: TagDict
    content = dict()  # type: TagDict
    content_end = dict()  # type: TagDict
    tag_end = dict()  # type: TagDict
    loaded = False

    def __new__(cls, *args) -> object:
        if not cls.loaded:
            cls.load()
        return super().__new__(cls)

    @classmethod
    def load(cls) -> None:
        format_path = join(dirname(abspath(__file__)), "format.csv")
        if not exists(format_path):
            raise FileNotFoundError
        with open(format_path, newline="") as f:
            reader = DictReader(f)
            for plain_data in reader:
                data = cls.parse(plain_data)
                cls.markers[data["Marker"]] = data["Name"]
                cls.tag_begin[data["Name"]] = "{0}" + data["Tag"]
                cls.content[data["Name"]] = "{0}" + data["Content"]
                cls.content_end[data["Name"]] = data["ContentEnd"] + "\n"
                cls.tag_end[data["Name"]] = data["TagEnd"] + "\n"
        cls.loaded = True

    @classmethod
    def parse(cls, data: dict) -> dict:
        return {key: data[key]
                .replace("{", "{{")
                .replace("}", "}}")
                .replace("@@", "\n{0}")
                .replace("@text", "{1}")
                for key in data}


if __name__ == "__main__":
    from pprint import PrettyPrinter
    Template()
    text = "{:X^10}".format("test")
    w = 4 * " "
    pp = PrettyPrinter()
    # pp.pprint(Template.__dict__)
    print("{:!^50}".format("format test"))
    for marker in Template.markers:
        key = Template.markers[marker]
        print("{:=^50}\n".format(key))
        print(Template.tag_begin[key].format(w, text), "\n", end="")
        print(Template.content[key].format(w, text), end="")
        print(Template.content_end[key].format(w, text), end="")
        print(Template.content[key].format(w, text), end="")
        print("\n" + w, Template.tag_end[key].format(w, text), end="")
        print("\n\n\n")
