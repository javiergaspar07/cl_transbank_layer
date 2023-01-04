# Built-in
from datetime import datetime
import json
import os
from secrets import token_hex
from uuid import UUID

# Local
from cl_transbank_layer import ProductType

# TPP's
from pydantic import (
    BaseModel,
    root_validator,
    AnyUrl,
    Field
)
from shortuuid import (
    uuid
)
from transbank.webpay.webpay_plus.transaction import (
    Transaction,
    WebpayOptions
)
from transbank.error.transaction_authorize_error import TransactionAuthorizeError
from transbank.error.transaction_commit_error import TransactionCommitError


class TransbankController(object):
    """
    Transbank object. Capable of initialize a financial auth request,
    which authorize a user to make a payment. 

    """

    def __init__(self, integration_type):
        """
        Fields:
            TBK_API_KEY_SECRET (str): Transbank API Key.
            TBK_API_KEY_ID (str): Transbank API Key ID.
            INTEGRATION_TYPE (str): Transbank integration type.
            transaction (Transaction): Transbank Transaction object initialized
            with given credentials.
        """
        self.TBK_API_KEY_SECRET = os.getenv('TBK_API_KEY_SECRET')
        self.TBK_API_KEY_ID = os.getenv('TRANSBANK_API_KEY_ID')
        self.INTEGRATION_TYPE = integration_type
        self.transaction = Transaction(WebpayOptions(self.TBK_API_KEY_ID,
                                                     self.TBK_API_KEY_SECRET,
                                                     self.INTEGRATION_TYPE))

    def init_financial_auth_request(self, data: dict) -> dict:
        """
        Make a financial authorization request for a credit
        or debit card payment. First step to make a payment.

        Args:
            data (dict): Object with financial auth request data.

        Raises:
            TransactionAuthorizeError: Error raised when init financial
            authorization request fails.

        Returns:
            dict: Dict with the url to make the payment.
        """
        response = self.transaction.create(**data)
        
        if not 'url' in response.keys():
            raise TransactionAuthorizeError()

        return response

    def confirm_transaction(self, token: str) -> dict:
        try:
            commit_result = self.transaction.commit(token)
        except TransactionCommitError:
            commit_result = None
        return commit_result

    def transaction_status(self, token: str) -> dict:
        """
        Make a request to Transbank API to get a transaction status.

        Args:
            token (str): Transbank token (generated by TBK API)

        Returns:
            dict: Status data of a transaction.
        """
        return self.transaction.status(token)


class TransbankCheckoutRequest(BaseModel):
    """
    Object which manage validation of data needed to make
    a financial auth request (Transbank).
    """
    buy_order: str = uuid()
    product_type: ProductType
    proposal_uuid: UUID
    amount: int
    session_id: str = token_hex(nbytes=25)
    return_url: AnyUrl

    @root_validator(pre=True)
    def get_amount(cls, values):
        amount = values.get('amount')

        if not amount:
            raise ValueError("'amount' parameter needed")
        
        if not isinstance(amount, float) and not isinstance(amount, int):
            raise ValueError("'amount' parameter must be float or int")
        
        if isinstance(amount, float):
            amount = int(round(amount, 0))

        values['amount'] = amount
        return values

    def dict(self):
        return json.loads(self.json())


class TransbankCheckoutResponse(BaseModel):
    """
    Validate cl_transbank_one_time_checkout response.

    - buy_order (str): Code generated by TransbankFinancialAuthRequest
    to identify an order in Transbank API
    - payment_url (AnyUrl): URL returned by Transbank API to make
    a one-time checkout.
    """
    buy_order: str
    payment_url: AnyUrl

    def dict(self):
        return json.loads(self.json())