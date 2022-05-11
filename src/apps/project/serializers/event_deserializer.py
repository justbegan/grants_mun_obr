import datetime


class EventDeserializer:

    def __init__(self, event):
        self.event = event

    def from_dict(self, event):
        self.event.job_id = event["job_id"]
        self.event.name = event["name"]
        self.event.guid = event["guid"]
        self.event.start_date = datetime.datetime.strptime(event["start_date"], '%Y-%m-%d')
        self.event.finish_date = datetime.datetime.strptime(event["finish_date"], '%Y-%m-%d')
        self.event.result = event["result"]
        self.event.publish_on_found = True

        return self.event
