import json


class ContestSerializer:

    def __init__(self, contest):
        self.contest = contest

    def to_json(self):
        directions = []
        for d in self.contest.directions.all():
            subjects = []
            for s in d.subjects():
                subjects.append({
                    "id": s.id,
                    "title": s.title
                })
            directions.append({
                "id": d.id,
                "title": d.title,
                "subjects": subjects
            })

        return json.dumps({
            'id': self.contest.id,
            'title': self.contest.title,
            'content': self.contest.content,
            'directions': directions,
        })
