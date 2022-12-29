from pydantic import (
    ValidationError
)
import json

def handle_api_exception(logger):
    """
    Handle api exceptions

    Args:
        logger (logging.logger): logger object from logging library.
    """
    def decorator(lambda_handler):
        def wrapper(*args, **kwargs):
            headers = {
                "Access-Control-Allow-Origin" : "*",
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
            try:
                logger.info("Trying to invoke function")
                return lambda_handler(*args, **kwargs)
            except ValidationError as e:
                logger.info("Validation error")
                logger.error(e.json())
                return {'statusCode': 400, 'body': e.json(), 'headers': headers}
            except Exception as e:
                logger.info("Exception occured")
                logger.error(e.__repr__())
                logger.error(e.__str__())
                return {'statusCode': 400, 'body': json.dumps({'detail': e.__repr__()}), 'headers': headers}

        return wrapper
        
    return decorator