from lib.events.SchwiEvent import SchwiEvent
from lib.events.SchwiEventListener import SchwiEventListener
from schwi.SchwiCog import SchwiCog
from promise import Promise


class EventManager(SchwiCog):
    listeners: dict[str, list[SchwiEventListener]] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on(self, event: SchwiEvent, callback, unique=False):
        listener = SchwiEventListener(event.event_name, callback, unique=unique)
        if event in self.listeners:
            self.listeners[event.event_name].append(listener)
        else:
            self.listeners[event.event_name] = [listener]
        return listener

    def off(self, listener: SchwiEventListener):
        self.listeners[listener.event_name].remove(listener)

    def emit(self, event: SchwiEvent):
        for listener in self.listeners[event.event_name]:
            if listener.unique and not event.is_unique():
                continue
            listener.callback(event)

    def wait_for(self, event: SchwiEvent):
        def resolver(resolve, reject):
            def callback(event):
                resolve(event)
                self.off(listener)

            listener = self.on(event, callback, unique=True)

        return Promise(resolver)
