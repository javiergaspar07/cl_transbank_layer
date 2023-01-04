# Local
from ..enums.events import TransbankNewPaymentEnum
from .base_event import BaseEvent


class TransbankNewPaymentEvent(BaseEvent):
    Source: str = TransbankNewPaymentEnum.source.value
    DetailType: str = TransbankNewPaymentEnum.detail_type.value