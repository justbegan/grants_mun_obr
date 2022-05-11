class GenericCostDeserializer:

    def __init__(self, cost):
        self.cost = cost

    def from_dict(self, cost):
        self.cost.guid = cost["guid"]
        self.cost.name = cost["name"]
        self.cost.items_count = cost["items_count"]
        self.cost.cost = cost["cost"]
        self.cost.co_financing = cost["co_financing"]
        self.cost.comment = cost["comment"]
        self.cost.type = cost["type"]

        return self.cost