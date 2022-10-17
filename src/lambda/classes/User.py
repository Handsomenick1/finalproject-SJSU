import json
import sys 

class User:
    def __init__(self, info_list) -> None:
        self.id = info_list["userId"]
        self.name = info_list["name"]
        self.email = info_list["email"]
        self.competitor = info_list["competitor"]
        self.organizer = info_list["organizer"]
        
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_email(self):
        return self.email
    
    def get_competitor(self):
        return self.competitor
    
    def get_organizer(self):
        return self.organizer
    
    def get_user_json(self):
        return json.dumps({
            "userId" : self.get_id(),
            "name": self.get_name(),
            "email": self.get_email(),
            "competitor": self.get_competitor(),
            "organizer": self.get_competitor()
        })
    
    def get_user_info(self):
        return {
            "userId" : self.get_id(),
            "name": self.get_name(),
            "email": self.get_email(),
            "competitor": self.get_competitor(),
            "organizer": self.get_competitor()
        }