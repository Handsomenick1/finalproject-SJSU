import json
import sys 

class Round:
    def __init__(self, roundId, QUEUED=[], ASSIGNED=[], STARTED=[], COMPLETED=[]) -> None:
        self.id = roundId
        self.QUEUED = QUEUED
        self.ASSIGNED = ASSIGNED
        self.STARTED = STARTED
        self.COMPLETED = COMPLETED
    def get_id(self):
        return self.id
    
    def get_QUEUED(self):
        return self.QUEUED
    
    def get_ASSIGNED(self):
        return self.ASSIGNED
    
    def get_STARTED(self):
        return self.STARTED
    
    def get_COMPLETED(self):
        return self.COMPLETED
    
    def QUEUED_to_ASSIGNED(self, groups):
        for group in groups:
            if group in self.QUEUED:
                self.ASSIGNED.append(group)
                
    def ASSIGNED_to_STARTED(self, groups):
        for group in groups:
            if group in self.ASSIGNED:
                self.STARTED.append(group)
        
    def STARTED_to_COMPLETED(self, groups):
        for group in groups:
            if group in self.STARTED:
                self.COMPLETED.append(group) 
    
    def get_round_info(self):
        return {
            "roundId" : self.get_id(),
            "QUEUED" : self.get_QUEUED(),
            "ASSIGNED" : self.get_ASSIGNED(),
            "STARTED" : self.get_STARTED(),
            "COMPELETED": self.get_COMPLETED()
        }  
    
    def get_round_json(self):
        return json.dumps(
            self.get_round_info()
        )  