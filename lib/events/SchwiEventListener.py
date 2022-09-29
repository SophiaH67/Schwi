from uuid import uuid4


class SchwiEventListener:
    def __init__(self, event_name, callback):
        self.id = uuid4()

        self.event_name = event_name
        self.callback = callback
