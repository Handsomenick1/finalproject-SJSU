import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    """_summary_
    
    1,   creats groups
    2,   assigns competitors and judges to group
    3,   place groups into the group queue
    4.1, tabulate the result, assign next round
    4.2, tabulate the winner
    
    """
    return {
        "statusCode": 200
    }
