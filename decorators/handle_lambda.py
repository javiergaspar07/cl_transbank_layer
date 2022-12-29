from pydantic import (
    ValidationError
)
import json

def handle_lambda_exception(logger):
    """
    Handle lambda functions exceptions

    Args:
        logger (logging.logger): logger object from logging library.
    """
    def decorator(lambda_handler):
        def wrapper(*args, **kwargs):
            try:
                logger.info("Trying to invoke function")
                return lambda_handler(*args, **kwargs)
            except ValidationError as e:
                logger.info("Validation error")
                logger.error(e.json())
                return {'statusCode': 400, 'body': e.json()}
            except Exception as e:
                logger.info("Exception occured")
                logger.error(e.__repr__())
                logger.error(e.__str__())
                return {'statusCode': 400, 'body': json.dumps({'detail': e.__repr__()})}

        return wrapper
        
    return decorator