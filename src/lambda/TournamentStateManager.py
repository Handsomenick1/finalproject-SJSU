import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    """_summary_

    1, track tournament state
    2, manage the realted reources

    """
    return {
        "statusCode": 200
    }
