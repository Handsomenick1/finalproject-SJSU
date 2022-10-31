import json
import sys 

class Venue:
    def __init__(self, info_list) -> None:
        self.id = info_list["venueId"]
        self.rooms = info_list["rooms"]
        
    def get_id(self):
        return self.id
    
    def get_rooms(self):
        return self.rooms

    def get_rooms_info(self):
        return {
            "venueId": self.get_id(),
            "rooms": self.get_rooms()
        }
        
    def get_venue_json(self):
        return json.dumps(self.get_rooms_info())
        