class JobDeserializer:

    def __init__(self, job):
        self.job = job

    def from_dict(self, job):
        self.job.content = job["content"]
        self.job.guid = job["guid"]

        return self.job