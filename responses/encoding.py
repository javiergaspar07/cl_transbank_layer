# Built-in
from datetime import datetime
from decimal import Decimal
from uuid import UUID

class Fakefloat(float):
    def __init__(self, value):
        self._value = value
    def __repr__(self):
        return str(self._value)

def json_encode(o):
    if isinstance(o, Decimal):
        return Fakefloat(o)
    if isinstance(o, UUID):
        return str(o)
    if isinstance(o, datetime):
        return str(o)
    raise TypeError(repr(o) + " is not JSON serializable")