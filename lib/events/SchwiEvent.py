import abc
from uuid import uuid4


class SchwiEvent:
    def __init__(self, schwi, dry=False):
        self.schwi = schwi
        self.id = str(uuid4())
        self.redis = self.schwi.get_cog("Redis")
        self.dry = dry

        if self.is_unique():
            self.redis.set(self.redis_key, self.id)

    @property
    def uid(self):
        """
        ID used for keeping track of uniqueness of events. If
        uniqueness is not important, this can just return self.id.
        """
        return self.id

    @property
    def redis_key(self):
        return f"event:{self.__class__.__name__}:{self.uid}"

    def is_unique(self):
        event_owner = self.redis.get(self.redis_key)
        return event_owner == self.id.encode() or event_owner is None

    def as_embed(self):
        return None

    def as_message(self):
        return None
