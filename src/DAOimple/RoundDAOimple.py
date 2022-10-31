import sys
sys.path.append("..")
import os
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
from DAO.RoundDAO import RoundDAO
from aws_helper.DynamoDB import update_item_db, scan_items_db, put_item_db, get_item_db

region = os.environ["region"]
round_table = os.environ["round_table"]
group_table = os.environ["group_table"]

class RoundDAOimpl(RoundDAO):
   
    def __init__(self) -> None:
        self.roundTable = boto3.resource("dynamodb", region).Table(round_table)
        self.groupTable = boto3.resource("dynamodb", region).Table(group_table)        
        self.rounds = {}
        
    #override
    def getAllRounds(self):
        
        try:
            self.rounds = scan_items_db(self.roundTable)
        except Exception as err:
            logger.error(
                "Couldn't get all rounds from table %s. Here's why: %s: %s",
                self.roundTable,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return self.rounds
    
    #override
    def getRound(self, roundId):
        
        try:
            round = get_item_db(self.roundTable, "roundId", roundId)
        except Exception as err:
            logger.error(
                "Couldn't get the round from table %s. Here's why: %s: %s",
                self.roundTable,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return round
    
    #override
    def updateRound(self, roundId, fileds: dict):
        
        try:
            for key in fileds:
                update_item_db(self.roundTable, "roundId", roundId, key, fileds.get(key))
            
        except Exception as err:
            logger.error(
                "Couldn't update the round to table %s. Here's why: %s: %s",
                self.roundTable,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
    
    #override
    def addRound(self, round):
        
        try:
            put_item_db(self.roundTable, round)

        except Exception as err:
            logger.error(
                "Couldn't add the round to table %s. Here's why: %s: %s",
                self.roundTable,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
    
    #override
    def getRoundbyGroupId(self, groupId) -> list:
        
        try:
            self.groups = scan_items_db(self.groupTable)
            self.rounds = scan_items_db(self.roundTable)
            round = []
            for group in self.groups:
                if group["groupId"] == groupId and group in self.rounds:
                    round.append(group)
            if round:
                return round
            
        except Exception as err:
            logger.error(
                "Couldn't get the group from table %s. Here's why: %s: %s",
                self.groupTable,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise