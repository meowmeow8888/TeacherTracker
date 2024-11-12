class Teacher:

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        result = f"{self.name}"
        return result

    def __eq__(self, other):
        return self.name == other.name