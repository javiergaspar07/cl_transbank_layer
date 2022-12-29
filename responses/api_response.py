# Built-in
import json
from typing import (
    Optional,
    Dict,
    Any,
    Union
)

# Local
from .status import StatusCode
from .encoding import json_encode

# TPP's
from pydantic import (
    BaseModel
)

class APIResponse(BaseModel):
    statusCode: StatusCode
    body: Optional[Union[str, Dict[str, Any]]] = {}
    headers: Dict[str, str] = {
        "Access-Control-Allow-Origin" : "*",
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }

    def dict(self):
        body = self.body if isinstance(self.body, str) else json.dumps(self.body, default=json_encode)
        return {
            'statusCode': self.statusCode.value,
            'body': body,
            'headers': self.headers
        }