import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def startGroups_handler(event, context):
    """_summary_
    
    1, Assign groups in QUEUED into rooms (if no room is available, wait until the next call)
    2, Collects judging results
    3, Passes control back to the roundManager if all groups are completed.

    """
    
    
    return {
        "statusCode": 200
    }

def collectResult_handler(event, context):
    """_summary_
    
    1, Assign groups in QUEUED into rooms (if no room is available, wait until the next call)
    2, Collects judging results
    3, Passes control back to the roundManager if all groups are completed.

    """
    
    
    return {
        "statusCode": 200
    }
