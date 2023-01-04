# Built-in
from enum import Enum

class TransbankNewPaymentEnum(Enum):
    source = 'cl_transbank_webhook'
    detail_type = 'transbank_new_payment'