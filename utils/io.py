from rich.console import Console
from rich.panel import Panel


class IO:
    """
    Input Output
    """

    @staticmethod
    def input(message: str) -> str:
        if message == "empty":
            return Console(color_system="windows").input(f"╰─> ")
        else:
            return Console(color_system="windows").input(f"{message}\n╰─> ")

    @staticmethod
    def output(message: str):
        Console(color_system="windows").print(message)

    @staticmethod
    def print_menu() -> int:
        while True:
            Console(color_system="windows").print(
                Panel.fit("1 - Check a website support.\n2 - Parse a website", title="Cimber Parser v0.0.4"))
            result = IO.input("empty")

            try:
                return int(result)
            except Exception as e:
                print(e)