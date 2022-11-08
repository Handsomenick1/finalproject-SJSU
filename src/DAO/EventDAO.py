from abc import ABC, abstractmethod

class EventDAO(ABC):
    @abstractmethod
    def getAllEvent(self):
        pass
    @abstractmethod
    def getEvent(self, eventId):
        pass
    @abstractmethod
    def updateEvent(self, eventId, filed: dict):
        pass
    @abstractmethod
    def deleteEvent(self, eventId):
        pass
    @abstractmethod
    def addEvent(self, event):
        pass
    