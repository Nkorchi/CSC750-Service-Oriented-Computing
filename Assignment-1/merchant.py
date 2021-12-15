from bungie import Adapter
import random
import asyncio
import logging
import uuid

from configuration import config
import Marketplace
from Marketplace import Merchant, OrderDetails, HoldNotice, SendItem, Tracking, UploadTracking, DeliveryConfirmation, PassDeliveryConfirmation, SendFund, ReviewTxn, Defective, DefectiveNotice

logger = logging.getLogger("Merchant-A")
adapter =  Adapter(Merchant, Marketplace.protocol, config)

@adapter.reaction(OrderDetails)
async def orderDetails(msg):
    logger.info(f'Received Order Details from eBay: {msg.payload}')


@adapter.reaction(HoldNotice)
async def receivedHoldNotice(msg):
    logger.info(f'Received hold notice from Paypal: {msg.payload}')
  

@adapter.enabled(SendItem)
async def sendItemShipper(msg):
    logger.info(f'Send item to Shipper: {msg.payload}')
    adapter.send(
        SendItem(
            item = str(uuid.uuid4()),
            **msg.payload
        )
    )


@adapter.reaction(Tracking)
async def trackingShipping(msg): 
    logger.info(f'Received Tracking Number from Shipper: {msg.payload}')
    adapter.send(
        UploadTracking(
            trackingInfo = str(uuid.uuid4()),
            **msg.payload
        )
    )

@adapter.reaction(DeliveryConfirmation)
async def deliveredToBuyer(msg):
    logger.info(f'Order delivery to Buyer is confirmed by Shipper {msg.payload}')
    adapter.send(
        PassDeliveryConfirmation(
            passedConfirmation = str(uuid.uuid4()),
            **msg.payload
        )
    )
    
@adapter.reaction(SendFund)
async def fundReceived(msg):
    logger.info(f'Fund received from PayPal: {msg.payload}')
    adapter.send(
        ReviewTxn(
            revtxn = str(uuid.uuid4()),
            **msg.payload
        )
    )


@adapter.reaction(Defective)
async def defectReaction(msg):
    logger.info(f'Received defective item back from Shipper: {msg.payload}')
    adapter.send(
        DefectiveNotice(
            defectNotice = str(uuid.uuid4()),
            **msg.payload
        )
    )
    



if __name__ == "__main__":
    logger.info("Starting Merchant...")
    adapter.start()