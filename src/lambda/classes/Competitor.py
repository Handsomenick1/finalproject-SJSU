import json
import sys 

class Competitor:
    def __init__(self, info_list) -> None:
        self.id = info_list["competitorId"]
        self.entries = info_list["competitionEntryId"]
        
    def get_id(self):
        return self.id
    
    def get_entries(self):
        return self.entries
    
    def get_competitor_json(self):
        return json.dumps({
            "competitorId" : self.get_id(),
            "entries": self.get_entries()
        })
    
    def get_competitor_info(self):
        return {
            "competitorId" : self.get_id(),
            "entries": self.get_entries()
        }