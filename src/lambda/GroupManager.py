import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    """_summary_
    
    1, takes groups from Queue 
    2, assign groups into rooms (if no room available, wait till next call)
    3, collects judging result
    4, pass control back to round manager if all groups are completed.
    
    """
    
    
    return {
        "statusCode": 200
    }
