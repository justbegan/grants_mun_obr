import datetime


class InstitutionDeserializer:

    def __init__(self, institution):
        self.institution = institution

    def from_dict(self, institution):
        self.institution.guid = institution["guid"]
        self.institution.organization = institution["organization"]
        self.institution.position = institution["position"]
        if institution["start_date"]:
            self.institution.start_date = datetime.datetime.strptime(institution["start_date"], '%Y-%m-%d')
        self.institution.in_present = institution["in_present"] if "in_present" in institution else False
        if institution["finish_date"]:
            self.institution.finish_date = datetime.datetime.strptime(institution["finish_date"], '%Y-%m-%d')
        if self.institution.in_present:
            self.institution.finish_date = None
        self.institution.member_id = institution["member_id"]
        self.institution.manager_id = institution["manager_id"]
        self.institution.type = institution["type"]

        return self.institution
