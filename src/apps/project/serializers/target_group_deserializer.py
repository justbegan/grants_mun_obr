class TargetGroupDeserializer:

    def __init__(self, target_group):
        self.target_group = target_group

    def from_dict(self, target_group):
        self.target_group.title = target_group["content"]
        self.target_group.type = target_group["type"]

        if 'organization_id' in target_group:
            self.target_group.organization_id = target_group["organization_id"]
            self.target_group.guid = target_group["guid"]

        return self.target_group