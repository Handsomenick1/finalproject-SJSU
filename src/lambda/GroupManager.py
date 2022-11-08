import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
import boto3
import json
import random
from constants.Response import returnResponse
from classes.Group import Group
from classes.Round import Round
from classes.Event import Event
from DAOimple.GroupDAOimple import GroupDAOimpl
from DAOimple.RoundDAOimple import RoundDAOimpl
from DAOimple.EventDAOimple import EventDAOimpl

# Assign Judges, asking tournament to get judges
# 
def startGroups_handler(event, context):
    """_summary_
    
    This function takes groups from the queued and assigns them to rooms.
    1, Call tournamentManager.getAvailableRooms() to get available rooms.
    2, Call tournamentManager.tournamentManager() to get available judges.
        2.1 Get judgesPerRound in eventMetaData
    3, Carry out groups from queued.
        3.1, the number of groups <= the number of available rooms && <= the number of Judges
    4, Call tournamentManager.useJudge() to assign judges to groups
    5, Call tournamentManager.startRoom() to occupy rooms with groups.
    6, Move the groups to assigned.

    """
    lambda_client = boto3.client('lambda', region_name="us-east-1")

    # Initialize DAO
    roundDAO = RoundDAOimpl()
    groupDAO = GroupDAOimpl()
    eventDAO = EventDAOimpl()
    
    roundId = event["body"]["roundId"]
    eventId = event["body"]["eventId"]
    tournamentId = event["body"]["tournamentId"]
    
    # 1.
    available_room_event = {
        "body": {
            "tournamentId" : tournamentId
            }
        }#dict
    available_room_response = lambda_client.invoke(
        FunctionName='getAvailableRooms',
        InvocationType='Event',
        Payload=json.dumps(available_room_event),
    )
    
    # 2.
    available_judges_event = {
        "body": {
            "tournamentId" : tournamentId
            }
        }
    available_judges_response = lambda_client.invoke(
        FunctionName='getAvailableJudges',
        InvocationType='Event',
        Payload=json.dumps(available_judges_event),
    )
    
    # Extract the response 
    room_payload = json.loads(available_room_response["Payload"].read())
    judges_payload = json.loads(available_judges_response["Payload"].read())
    total_room = room_payload["body"]["totalRoom"]
    total_judges = judges_payload["body"]["totalJudge"]
    room_list = room_payload["body"]["rooms"]
    judges_list = judges_payload["body"]["judges"] # randomly shuffle teh jusdges list
    random.shuffle(judges_list)
    
    # 2.1 
    # Build event objct
    eventObj = Event(eventDAO.getEvent(eventId))
    # Get the number of jusges needed per round
    currentRoundIdx = eventObj.get_currentRoundIdx()
    print(eventObj.get_event_info())
    print(type(eventObj.get_currentRoundIdx()))
    judges_need = int(eventObj.get_rounds()[int(currentRoundIdx)]["judgesPerRound"])
    # arrang_judges_list used to store arranged judges
    arrang_judges_list = []
    # Sliding window 
    right_bound = judges_need
    left_bound = 0
    for i in range(0, total_judges):
        if right_bound > total_judges:
            break
        arrang_judges_list.append(judges_list[left_bound:right_bound])
        left_bound = right_bound
        right_bound += judges_need
        
    # 3. 
    group_list = []
    roundInfo = roundDAO.getRound(roundId) 
    roundObj = Round(roundInfo["roundId"], roundInfo["queued"], roundInfo["assigned"], roundInfo["started"], roundInfo["completed"])
    queued_list = roundObj.get_queued()
    for queued_group_info in queued_list:
        cur_group = Group(queued_group_info)
        group_list.append(cur_group)
        groupDAO.addGroup(cur_group.get_group_info())
    
    
    # judges_index used to track the arranged judges
    # groups_index used to track the group
    random.shuffle(group_list)
    judges_index = 0
    groups_index = 0
    for group in group_list:
        # 3.1
        if(groups_index >= total_room or judges_index >= len(arrang_judges_list)):
            break
        groupId = group.get_id()
    # 4.
        judgeId = arrang_judges_list[judges_index]
        payload_judges = {
            "body":{
                "tournamentId": tournamentId,
                "judgeId" : judgeId # list of judgeId
             }
            }
        try:
            response = lambda_client.invoke(
            FunctionName='useJudge',
            Payload=json.dumps(payload_judges),
            )
            group.set_judges(judgeId)
            groupDAO.updateGroup(groupId, {"judges": group.get_judges()})
        except Exception as err:
            logger.debug("Can not finish the 4. useJudge(), because {}".format(str(err)))
            raise
        
    # 5. 
        roomId = room_list[groups_index]
        payload_room = {
            "body":{
                "roundId" : roundId,
                "eventId" : eventId,
                "groupId" : groupId,
                "roomdId": room_list[groups_index],
                "tournamentId": tournamentId
             }
            }
        try:
            response = lambda_client.invoke(
            FunctionName='startRoom',
            Payload=json.dumps(payload_room),
            )
            group.set_roomId(roomId)
            groupDAO.updateGroup(groupId, {"roomId": group.get_roomId()})
        except Exception as err:
            logger.debug("Can not finish the 5. startRoom(), because {}".format(str(err)))
            raise
            
    # 6.
        roundObj.queued_to_assigned(group.get_group_info())
        roundDAO.updateRound(
            roundId, 
            {"queued" : roundObj.get_queued(), 
             "assigned": roundObj.get_assigned()})
        
    # Delete current group in group_list
        group_list = filter(lambda x: x != group, group_list)
        groups_index += 1
        judges_index += 1
    return returnResponse(200, {"body" : "hello world!"})

def startCompetition_handler(event, context):
    """_summary_

    Judges will call this function to start the competition.
    1, Place the group from assigned into started

    """
    roundId = event["body"]["roundId"]
    groupId = event["body"]["groupId"]
    
    # Initialize DAO
    roundDAO = RoundDAOimpl()
    groupDAO = GroupDAOimpl()
    
    # Build group & round obj
    group_info = groupDAO.getGroup(groupId)
    roundInfo = roundDAO.getRound(roundId) # need CURD for round data
    roundObj = Round(roundInfo["roundId"], roundInfo["queued"], roundInfo["assigned"], roundInfo["started"], roundInfo["completed"])   # need a round class
    
    # 1.
    roundObj.assigned_to_started(group_info)
    
    return returnResponse(200, {"body" : "hello world!"})

    
def collectResult_handler(event, context):
    """_summary_
    
    This function will be called when a round is completed and used to collect judging results from the completed round.
    1, Move the completed group from started to completed.
    2, Save the judging result
    3, Call tournamentManager.freeJudge() to free judges
    4, Release the occupied room by calling tournamentManager.finishRoom(roomId, adminId)
    5, Check if there are uncompleted groups.
        5.1, If Yes:  
            5.1.1Call startRoom(eventId, roomId, adminId) to strat the room.
        5.2, If No: Call roundManager.completeRound(roundId) to pass the control to roundManager. 

    """
    lambda_client = boto3.client('lambda', region_name="us-east-1")

    roundId = event["body"]["roundId"]
    groupId = event["body"]["groupId"]
    judgeId = event["body"]["judges"]
    eventId = event["body"]["eventId"]
    roomId = event["body"]["roomId"]   
    tournamentId = event["body"]["tournamentId"]
    ranking = event["body"]["ranking"]
    
     # Initialize DAO
    roundDAO = RoundDAOimpl()
    groupDAO = GroupDAOimpl()
    
    roundInfo = roundDAO.getRound(roundId)
    roundObj = Round(roundInfo["roundId"], roundInfo["queued"], roundInfo["assigned"], roundInfo["started"], roundInfo["completed"])   # need a round class
    group_Info = groupDAO.getGroup(groupId)
    # 1.
    roundObj.started_to_completed(group_Info)
    roundDAO.updateRound(
            roundId, 
            {"started" : roundObj.get_started(), 
             "completed": roundObj.get_completed()})
    # 2.
    groupDAO.updateGroup(groupId, {"ranking": ranking})

    # 3.
    payload_judge = {
        "body":{
            "judgeId": judgeId, # list of judges
            "tournamentId": tournamentId
            }
        }
    response = lambda_client.invoke(
        FunctionName='freeJudge',
        Payload=json.dumps(payload_judge),
    )
    
    # 4.
    payload_room = {
        "body": {
            "roomdId": roomId,
            "tournamentId": tournamentId
            }
    }
    response = lambda_client.invoke(
        FunctionName='finishRoom',
        Payload=json.dumps(payload_room),
    )
    # 5.
    queued_list = roundObj.get_queued()
    
    # 5.1
    if queued_list:
        # 5.1.1
        next_group_id = queued_list[0]["groupId"]
        payload_room = {
            "body": {
                "roundId" : roundId,
                "eventId" : eventId,
                "groupId" : next_group_id,
                "roomdId": roomId,
                "tournamentId": tournamentId
                }
        }
        response = lambda_client.invoke(
        FunctionName='startRoom',
        Payload=json.dumps(payload_room),
        )
        # Update group database
        groupDAO.updateGroup(next_group_id, {"roomId": roomId})
        # Update round database
        roundObj.assigned_to_started([next_group_id])
        roundDAO.updateRound(
            roundId, 
            {"queued" : roundObj.get_queued(), 
             "assigned": roundObj.get_assigned()}
            )
        return returnResponse(200, {"message" : "still have groups in queued"})

    # 5.2
    if roundObj.all_completed():
        payload_room = {
            "body": {
                "eventId": eventId,
                "roundId": roundId,
                "tournamentId" : tournamentId
            }
        }
        response = lambda_client.invoke(
        FunctionName='completeRound',
        Payload=json.dumps(payload_room),
        )
        return returnResponse(200, {"message" : "all groups are completed"})
