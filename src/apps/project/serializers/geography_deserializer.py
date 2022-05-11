class GeographyDeserializer:

    def __init__(self, geo):
        self.geo = geo

    def from_dict(self, geo):
        self.geo.guid = geo["guid"]
        self.geo.name = geo["name"]
        self.geo.organization_id = geo["organization_id"]

        return self.geo