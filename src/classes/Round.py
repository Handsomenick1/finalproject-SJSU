import json
import sys 
from constants.DecimalEncoder import DecimalEncoder

class Round:
    def __init__(self, roundId, queued = [], assigned=[], completed=[], started=[], awards=[]) -> None:
        self.id = roundId
        self.queued = queued
        self.assigned = assigned
        self.completed = completed
        self.started = started
        self.awards = awards
        
    def get_id(self):
        return self.id
    
    def get_queued(self):
        return self.queued
    
    def get_assigned(self):
        return self.assigned
    
    def get_started(self):
        return self.started
    
    def get_completed(self):
        return self.completed
    
    def get_awards(self):
        return self.awards
    
    def queued_to_assigned(self, group):
        for g in self.queued:
            if g["groupId"] == group["groupId"]:
                self.queued.remove(g)
        self.assigned.append(group)
                
    
    def assigned_to_started(self, group):
        self.assigned.remove(group)
        self.started.append(group)

    def started_to_completed(self, group):
        self.started.remove(group)
        self.completed.append(group)

    def all_completed(self):
        return len(self.queued == 0) and len(self.assigned == 0) and len(self.started == 0)
    
    def get_round_info(self):
        return {
            "roundid" : self.get_id(),
            "queued" : self.get_queued(),
            "assigned" : self.get_assigned(),
            "completed": self.get_completed(),
            "started": self.get_started(),
            "awards": self.get_awards()
        }  
    
    def get_round_json(self):
        return json.dumps(
            self.get_round_info(), cls=DecimalEncoder
        )  