import json
import sys 

class Group:
    def __init__(self, info_list, result={}) -> None:
        self.id = info_list["groupId"]
        self.roomId = info_list["roomId"]
        self.judgesIds = info_list["judgesIds"]
        self.competitorIds = info_list["competitorIds"]
        self.result = result
        
    def get_id(self):
        return self.id
    
    def get_roomId(self):
        return self.roomId
    
    def get_judgesIds(self):
        return self.judgesIds
    
    def get_competitorIds(self):
        return self.competitorIds
    
    def get_result(self):
        return self.result
    
    def set_roomId(self, newRoomId):
        self.roomId = newRoomId
        
    def set_judgesIds(self, newJudegesId):
        self.judgesIds = newJudegesId
        
    def set_result(self, newResult):
        self.result = newResult
    
    def set_competitorIds(self, newCompetitorId):
        self.competitorIds = newCompetitorId
    
    def get_group_info(self):
        return {
            "groupId" : self.get_id(),
            "roomId": self.get_roomId(),
            "judgesIds": self.get_judgesIds(),
            "competitorIds": self.get_competitorIds(),
            "result" : self.get_result()
        }
    
    def get_group_json(self):
        return json.dumps(self.get_group_info())