from abc import abstractproperty
from SchwiEvent import SchwiEvent


class UniqueSchwiEvent(SchwiEvent):
    @abstractproperty
    def uid(self):
        pass
