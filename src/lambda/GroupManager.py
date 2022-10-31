import logging

from zmq import QUEUE
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
import boto3
import json
from constants.Response import returnResponse
from classes.Group import Group
lambda_client = boto3.client('lambda')

def startGroups_handler(event, context):
    """_summary_
    
    This function takes groups from the QUEUED and assigns them to rooms.
    1, Call tournamentManager.getAvailableRooms() to get available rooms.
    2, Carry out groups from QUEUED.
        2.1, the number of groups <= the number of available rooms
    3, Call tournamentManager.startRoom() to occupy rooms with groups.
    4, Move the groups to ASSIGNED.

    """
    roundId = event["roundId"]
    
    # 1.
    test_event = dict()
    room_response = lambda_client.invoke(
        FunctionName='getAvailableRooms',
        Payload=json.dumps(test_event),
    )
    
    # 2. 
    roundInfo = dynamoDB_get_roundInfo(roundId) # need CURD for round data
    roundObj = Round(roundInfo)   # need a round class
    QUEUED_list = roundObj.get_QUEUED()
    group_list = []
    for queueInfo in QUEUED_list:
        group_list.append(Group(queueInfo))
    
    roomNumber = room_response["roomNumber"]
    groupsNumber = 1
    for group in group_list:
        if(groupsNumber > roomNumber):
            break
        
    # 3. 
        payload_room = {
            "roundId" : group.get_id(),
            "roomdId": room_response["roomList"]["roomId"],
            "adminId": "not defined"}
        response = lambda_client.invoke(
        FunctionName='startRoom',
        Payload=json.dumps(payload_room),
        )
        
    # 4.
        roundObj.QUEUED_to_ASSIGNED(group.get_group_info())
    
    # Delete current group in group_list
        group_list = filter(lambda x: x != group, group_list)
        groupsNumber += 1
        
    return returnResponse(200, {"body" : "hello world!"})

def startCompetition_handler(event, context):
    """_summary_

    Judges will call this function to start the competition.
    1, Place the group from ASSIGNED into STARTED

    """
    roundId = event["roundId"]
    
    return returnResponse(200, {"body" : "hello world!"})

    
def collectResult_handler(event, context):
    """_summary_
    
    This function will be called when a round is completed and used to collect judging results from the completed round.
    1, Move the completed group from STARTED to COMPLETED.
    2, Check if there are uncompleted groups.
    3.1, If Yes:  
        3.1.1Call tournamentManager.finishRoom(roomId, adminId) to free the room.
        3.1.2Call startRoom(eventId, roomId, adminId) to strat the room.
    3.2, If No: Call roundManager.completeRound(roundId) to pass the control to roundManager. 

    """
    roundId = event["roundId"]
    groupId = event["groupId"]
       
    return returnResponse(200, {"body" : "hello world!"})

