import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def startGroups_handler(event, context):
    """_summary_
    
    This function takes groups from the QUEUED and assigns them to rooms.
    1, Call tournamentManager.getAvailableRooms() to get available rooms.
    2, Carry out groups from QUEUED.
        2.1, the number of groups <= number of available rooms
    3, Call tournamentManager.occupyRooms() to occupy rooms with groups.

    """
    
    
    return {
        "statusCode": 200
    }

def collectResult_handler(event, context):
    """_summary_
    
    This function will be called when a round is completed and used to collect judging results from the completed round.
    1, Move the completed group into COMPLETED.
    2, Check if there are uncompleted groups.
        2.1, If Yes:  Call tournamentManager.occupyRooms() with uncompleted groupId and current roomId.
        2.2, If No: Call roundManager.completeRound(roundId) to pass the control to roundManager. 

    """
    
    
    return {
        "statusCode": 200
    }
