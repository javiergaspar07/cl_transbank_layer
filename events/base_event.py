# Built-in
from datetime import datetime
import os
from typing import List

# TPP's
from pydantic import BaseModel


class BaseEvent(BaseModel):
    Detail: str
    EventBusName: str = os.getenv('BUS')
    Resources: List[str]
    Time: str = str(datetime.now().time())