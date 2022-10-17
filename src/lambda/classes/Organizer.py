import json
import sys 

class Organizer:
    def __init__(self, info_list) -> None:
        self.id = info_list["organizerId"]
        self.tournaments = info_list["tournamentId"]
    
    def get_id(self):
        return self.id
    
    def get_tournaments(self):
        return self.tournaments
    
    def get_organizer_json(self):
        return json.dumps({
            "userId" : self.get_id(),
            "tournaments": self.get_tournaments()
        })
        
    def get_organizer_info(self):
        return {
            "organizerId" : self.get_id(),
            "tournaments": self.get_tournaments()
        }