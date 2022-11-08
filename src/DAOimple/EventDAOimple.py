import sys 
sys.path.append("..")
import os
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
from DAO.EventDAO import EventDAO
from aws_helper.DynamoDB import update_item_db, scan_items_db, put_item_db, get_item_db

region = os.environ["region"]
event_table = os.environ["event_table"]

class EventDAOimpl(EventDAO):
    def __init__(self) -> None:
        self.eventTable = boto3.resource("dynamodb", region).Table(event_table)
        self.events = []
    
    # Override
    def getAllEvent(self):
        
        try:
            self.events = scan_items_db(self.eventTable)
        except Exception as err:
            logger.error(
                "Couldn't get all events from table %s. Here's why: %s",
                self.eventTable,
                str(err))
            raise
        else:
            return self.events
    
    
    # Override
    def getEvent(self, eventId):
        
        try:
            event = get_item_db(self.eventTable, "eventId", eventId)
        except Exception as err:
            logger.error(
                "Couldn't get the event from table %s. Here's why: %s",
                self.eventTable,
                str(err))
            raise
        else:
            return event

    # Override
    def updateEvent(self, eventId, filed: dict):
        
        try:
            for key in filed:
                update_item_db(self.eventTable, "eventId", eventId, key, filed.get(key))
            
        except Exception as err:
            logger.error(
                "Couldn't update the event to table %s. Here's why: %s",
                self.eventTable,
                str(err))
            raise
        
    # Override
    def deleteEvent(self, eventId):
        return super().deleteEvent(eventId)
    
    # Override
    def addEvent(self, event):
        
        try:
            put_item_db(self.eventTable, event)

        except Exception as err:
            logger.error(
                "Couldn't add the group to table %s. Here's why: %s",
                self.eventTable,
                str(err))
            raise