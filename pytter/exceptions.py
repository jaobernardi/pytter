#TODO: Add a base class for pytter exceptions.

class ApiNotLinked(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)