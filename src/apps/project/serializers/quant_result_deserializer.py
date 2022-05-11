class QuantResultDeserializer:

    def __init__(self, result):
        self.result = result

    def from_dict(self, result):
        self.result.guid = result["guid"]
        self.result.name = result["name"]
        self.result.count = result["count"]

        return self.result