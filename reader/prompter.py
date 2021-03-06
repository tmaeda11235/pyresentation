from csv import DictReader
from os.path import exists
from typing import Dict


TagDict = Dict[str, str]


class Prompter:
    marker = dict()  # type: TagDict
    tag = dict()  # type: TagDict
    content = dict()  # type: TagDict
    content_end = dict()  # type: TagDict
    tag_end = dict()  # type: TagDict
    loaded = False

    def __new__(cls) -> object:
        if not cls.loaded:
            cls.load()
        return super().__new__(cls)

    @classmethod
    def load(cls):
        if not exists("format.csv"):
            raise FileNotFoundError
        with open("format.csv", newline="") as f:
            reader = DictReader(f)
            for plain_data in reader:
                data = cls.parse(plain_data)
                cls.marker[data["Marker"]] = data["Name"]
                cls.tag[data["Name"]] = "{0}" + data["Tag"]
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
    Prompter()
    text = "{:X^10}".format("test")
    w = 4 * " "
    pp = PrettyPrinter()
    # pp.pprint(Prompter.__dict__)
    print("{:!^50}".format("format test"))
    for key in Prompter.tag:
        print("{:=^50}\n".format(key))
        print(Prompter.tag[key].format(w, text), "\n", end="")
        print(Prompter.content[key].format(w, text), end="")
        print(Prompter.content_end[key].format(w, text), end="")
        print(Prompter.content[key].format(w, text), end="")
        print("\n" + w, Prompter.tag_end[key].format(w, text), end="")
        print("\n\n\n")
