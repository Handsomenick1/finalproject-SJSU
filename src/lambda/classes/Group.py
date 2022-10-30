import json
import sys 

class Group:
    def __init__(self, info_list) -> None:
        self.id = info_list["groupId"]
        self.roomId = info_list["roomId"]
        self.judegesId = info_list["judegesId"]
        self.competitorId = info_list["competitorId"]
        self.result = {}
        
    def get_id(self):
        return self.id
    
    def get_roomId(self):
        return self.roomId
    
    def get_judegesId(self):
        return self.judegesId
    
    def get_competitorId(self):
        return self.competitorId
    
    def get_result(self):
        return self.result
    
    def set_roomId(self, newRoomId):
        self.roomId = newRoomId
        
    def set_judegesId(self, newJudegesId):
        self.judegesId = newJudegesId
        
    def set_result(self, newResult):
        self.result = newResult
    
    def set_competitorId(self, newCompetitorId):
        self.competitorId = newCompetitorId
    
    def get_group_info(self):
        return {
            "groupId" : self.get_id(),
            "roomId": self.get_roomId(),
            "judegesId": self.get_judegesId(),
            "competitorId": self.get_competitorId(),
            "result" : self.get_result()
        }
    
    def get_group_json(self):
        return json.dumps(self.get_group_info())