class TestModel():

    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return "Test Object with id :: {} and name :: {}".format(self.id, self.name)
