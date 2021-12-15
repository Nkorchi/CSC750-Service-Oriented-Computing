from bungie import Adapter
import random
import asyncio
import logging
import uuid

from configuration import config
import Marketplace
from Marketplace import PayPal, PaymentPaypal, HoldNotice, ReleaseFund, SendFund, RequestDefectRefund, SendDefectRefund

logger = logging.getLogger("PayPal-Org")
adapter = Adapter(PayPal, Marketplace.protocol, config)

@adapter.reaction(PaymentPaypal)
async def receiveFund(msg):
    logger.info(f'Received fund with status hold: {msg.payload}')
    adapter.send(
        HoldNotice(
            paymentHold = str(uuid.uuid4()),
            **msg.payload
        )
    )

@adapter.reaction(ReleaseFund)
async def releaseFund(msg):
    logger.info(f'Fund released to Merchant: {msg.payload}')
    adapter.send(
        SendFund(
            sentFund = str(uuid.uuid4()),
            **msg.payload
        )
    )


@adapter.reaction(RequestDefectRefund)
async def defectRefund(msg):
    logger.info(f'Received defect refund request from eBay: {msg.payload}')
    adapter.send(
        SendDefectRefund(
            defRefundSent = str(uuid.uuid4()),
            **msg.payload
        )
    )



if __name__ == "__main__":
    logger.info("Starting PayPal...")
    adapter.start()
