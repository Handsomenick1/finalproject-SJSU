import json
import sys 
from constants.DecimalEncoder import DecimalEncoder

class Event:
    def __init__(self, info_list) -> None:
        self.id = info_list["eventId"]
        self.awards = info_list["awards"]
        self.rounds = info_list["rounds"]
        self.currentRoundIdx = info_list["currentRoundIdx"]

    def get_id(self):
        return self.id
    
    def get_awards(self):
        return self.awards
    
    def get_rounds(self):
        return self.rounds
    
    def get_currentRoundIdx(self):
        return self.currentRoundIdx
    
    def get_event_info(self):
        return {
            "eventId" : self.get_id(),
            "awards" : self.get_awards(),
            "currentRoundIdx": self.get_currentRoundIdx(),
            "rounds" : self.get_rounds(),
        }
    def get_event_json(self):
        return json.dumps(self.get_event_info, cls=DecimalEncoder)