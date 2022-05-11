class ProjectMemberDeserializer:

    def __init__(self, project_member):
        self.project_member = project_member

    def from_dict(self, member):
        self.project_member.position = member["position"]
        self.project_member.last_name = member["last_name"]
        self.project_member.first_name = member["first_name"]
        self.project_member.middle_name = member["middle_name"]
        self.project_member.education = member["education"]
        self.project_member.info = member["info"]
        self.project_member.guid = member["guid"]

        return self.project_member