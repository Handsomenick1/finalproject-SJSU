import logging

from DAO.GroupDAO import GroupDAO
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
import boto3
import json
from constants.Response import returnResponse
from classes.Group import Group
from classes.Round import Round
from DAOimple.GroupDAOimple import GroupDAOimpl
from DAOimple.RoundDAOimple import RoundDAOimpl

def startGroups_handler(event, context):
    """_summary_
    
    This function takes groups from the QUEUED and assigns them to rooms.
    1, Call tournamentManager.getAvailableRooms() to get available rooms.
    2, Carry out groups from QUEUED.
        2.1, the number of groups <= the number of available rooms
    3, Call tournamentManager.startRoom() to occupy rooms with groups.
    4, Move the groups to ASSIGNED.

    """
    lambda_client = boto3.client('lambda', region_name="us-east-1")

    # Initialize DAO
    roundDAO = RoundDAOimpl()
    groupDAO = GroupDAOimpl()
    
    roundId = event["roundId"]
    
    # 1.
    test_event = {
        "body": {
            "roomList" :[
                        {"roomId" : "room001"},
                        {"roomId" : "room002"},
                        ],
            "roomNumber" : 2
            }
        }#dict
    room_response = lambda_client.invoke(
        FunctionName='getAvailableRooms',
        InvocationType='Event',
        Payload=json.dumps(test_event),
    )
    
    # 2. 
    roundInfo = roundDAO.getRound(roundId) # need CURD for round data
    roundObj = Round(roundInfo["roundId"], roundInfo["QUEUED"])   # need a round class
    QUEUED_list = roundObj.get_QUEUED()
    group_list = []
    for queueInfo in QUEUED_list:
        cur_group = Group(queueInfo)
        group_list.append(cur_group)
        groupDAO.addGroup(queueInfo)
    
    room_payload = json.loads(room_response["Payload"].read())
    print(room_payload)
    roomNumber = room_payload["body"]["roomNumber"]
    groupsNumber = 0
    for group in group_list:
        # 2.1
        if(groupsNumber >= roomNumber):
            break
        
    # 3. 
        payload_room = {
            "body":{
                "roundId" : group.get_id(),
                "roomdId": room_payload["body"]["roomList"][groupsNumber],
                "adminId": "not defined"
             }
            }
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
    groupId = event["groupId"]
    
    # Initialize DAO
    roundDAO = RoundDAOimpl()
    groupDAO = GroupDAOimpl()
    
    # Build group & round obj
    group_info = groupDAO.getGroup(groupId)
    roundInfo = roundDAO.getRound(roundId) # need CURD for round data
    roundObj = Round(roundInfo["roundId"], roundInfo["ASSIGNED"])   # need a round class
    
    # 1.
    roundObj.ASSIGNED_to_STARTED([group_info])
    
    return returnResponse(200, {"body" : "hello world!"})

    
def collectResult_handler(event, context):
    """_summary_
    
    This function will be called when a round is completed and used to collect judging results from the completed round.
    1, Move the completed group from STARTED to COMPLETED.
    2, Save the judging result
    3, Release the occupied room by calling tournamentManager.finishRoom(roomId, adminId)
    4, Check if there are uncompleted groups.
        4.1, If Yes:  
            4.1.1Call startRoom(eventId, roomId, adminId) to strat the room.
        4.2, If No: Call roundManager.completeRound(roundId) to pass the control to roundManager. 

    """
    lambda_client = boto3.client('lambda', region_name="us-east-1")

    roundId = event["roundId"]
    groupId = event["groupId"]
    roomId = event["roomId"]   
    adminId = "not defined"
    result = event["judgeingresult"]
    
     # Initialize DAO
    roundDAO = RoundDAOimpl()
    groupDAO = GroupDAOimpl()
    
    roundInfo = roundDAO.getRound(roundId) # need CURD for round data
    roundObj = Round(roundInfo["roundId"], roundInfo["QUEUED"], roundInfo["ASSIGNED"], roundInfo["STARTED"])   # need a round class
    group_Info = groupDAO.getGroup(groupId)
    
    # 1.
    roundObj.STARTED_to_COMPLETED([group_Info])
    
    # 2.
    groupDAO.updateGroup(groupId, {"judgeingresult": result})
    
    # 3.
    payload_room = {
            "roomdId": roomId,
            "adminId": adminId}
    response = lambda_client.invoke(
        FunctionName='finishRoom',
        Payload=json.dumps(payload_room),
    )
    # 4.
    QUEUED_list = roundObj.get_QUEUED()
    
    # 4.1
    if QUEUED_list:
        # 4.1.1
        payload_room = {
            "groupId" : groupId,
            "roomdId": roomId,
            "adminId": adminId}
        response = lambda_client.invoke(
        FunctionName='startRoom',
        Payload=json.dumps(payload_room),
        )
        return returnResponse(200, {"message" : "uncompleted"})

    # 4.2
    else:
        payload_room = {
            "roundId": roundId
        }
        response = lambda_client.invoke(
        FunctionName='completeRound',
        Payload=json.dumps(payload_room),
        )
        return returnResponse(200, {"message" : "completed"})
