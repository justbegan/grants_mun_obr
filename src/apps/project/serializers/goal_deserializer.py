class GoalDeserializer:

    def __init__(self, goal):
        self.goal = goal

    def from_dict(self, goal):
        self.goal.content = goal["content"]
        self.goal.guid = goal["guid"]

        return self.goal