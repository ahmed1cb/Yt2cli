class Yt2cli:
    def __init__(self) -> None:
        self.options = {
            "search": "Use it To Search for Youtube Videos , usage: search :query",
            "open": "Use It to Open A video From the List of Searched Videos",
        }
        self.show_options()

    def handle(self, args: list | str):
        if type(args) is str:
            args = args.split()
        command = args[0]

    def show_options(self):
        print("*" * 5 + " Available Options " + "*" * 5)
        for option in self.options:
            print(f"{option} : {self.options[option]} ")
