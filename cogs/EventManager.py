from lib.events.SchwiEvent import SchwiEvent
from lib.events.SchwiEventListener import SchwiEventListener
from schwi.SchwiCog import SchwiCog
from promise import Promise
import asyncio


class EventManager(SchwiCog):
    listeners: dict[str, list[SchwiEventListener]] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on(self, event: SchwiEvent, callback):
        self.logger.debug(f"Adding event listener for event {event.event_name}")
        listener = SchwiEventListener(event.event_name, callback)
        if event in self.listeners:
            self.listeners[event.event_name].append(listener)
        else:
            self.listeners[event.event_name] = [listener]
        return listener

    def off(self, listener: SchwiEventListener):
        self.logger.debug(f"Removing event listener {listener.event_name}")
        self.listeners[listener.event_name].remove(listener)

    def emit(self, event: SchwiEvent):
        if not event.event_name in self.listeners:
            return
        for listener in self.listeners[event.event_name]:
            if not event.is_unique():
                continue
            ret = listener.callback(event)
            if asyncio.iscoroutine(ret):
                loop = asyncio.get_event_loop()
                loop.create_task(ret)

    def wait_for(self, event: SchwiEvent):
        def resolver(resolve, reject):
            def callback(event):
                resolve(event)
                self.off(listener)

            listener = self.on(event, callback)

        return Promise(resolver)
