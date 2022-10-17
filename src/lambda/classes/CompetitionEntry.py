import json
import sys 

class CompetitionEntry:
    
    def __init__(self, info_list) -> None:
        self.id = info_list["competitionEntryId"]
        self.tournament = info_list["tournamentId"]
        self.eventFeePaid = info_list["eventFeePaid"]
        self.confirmedCompetitors = info_list["confirmedCompetitorId"]
        self.invitedCompetitors = info_list["invitedCompetitorId"]
        
    def get_id(self):
        return self.id
    
    def get_tournament(self):
        return self.tournament
    
    def get_eventFeePaid(self):
        return self.eventFeePaid
    
    def get_confirmedCompetitors(self):
        return self.confirmedCompetitors
    
    def get_invitedCompetitors(self):
        return self.invitedCompetitors
    
    def get_competitionEntry_json(self):
        return json.dumps({
            "competitionEntryId" : self.get_id(),
            "tournament": self.get_tournament(),
            "eventFeePaid": self.get_eventFeePaid(),
            "confirmedCompetitors": self.get_confirmedCompetitors(),
            "invitedCompetitors": self.get_invitedCompetitors()
        })
    
    def get_get_competitionEntry_info(self):
        return {
            "competitionEntryId" : self.get_id(),
            "tournament": self.get_tournament(),
            "eventFeePaid": self.get_eventFeePaid(),
            "confirmedCompetitors": self.get_confirmedCompetitors(),
            "invitedCompetitors": self.get_invitedCompetitors()
        }