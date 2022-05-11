class PartnerDeserializer:

    def __init__(self, partner):
        self.partner = partner

    def from_dict(self, partner):
        self.partner.name = partner["name"]
        self.partner.guid = partner["guid"]
        supports = ''
        for supportData in partner["supports"]:
            supports = supports + supportData['text'] + ','
        
        self.partner.supports = supports.rstrip(',')
        return self.partner