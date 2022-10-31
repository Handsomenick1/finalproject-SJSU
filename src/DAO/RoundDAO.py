from abc import ABC, abstractmethod

class RoundDAO(ABC):
    @abstractmethod
    def getAllRounds(self):
        pass
    @abstractmethod
    def getRound(self, roundId):
        pass
    @abstractmethod
    def updateRound(self, roundId, filed: dict):
        pass
    @abstractmethod
    def addRound(self, round):
        pass
    @abstractmethod
    def getRoundbyGroupId(self, groupId):
        pass