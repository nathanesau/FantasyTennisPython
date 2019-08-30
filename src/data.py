# data types


class PlayerNodeData:
    def __init__(self, name, seed, country):
        self.name = name
        self.seed = seed
        self.country = country


class BracketNodeData:
    def __init__(self, playerOneNodeData, playerTwoNodeData):
        self.playerOneNodeData = playerOneNodeData
        self.playerTwoNodeData = playerTwoNodeData


# drawRowList: [[1, "Nadal", "bye"], [1, "Federer", "Evans"]]
# playerRowList: [["Nadal", "1", "Spain"], ["Federer", "3", "Switzerland"]]
