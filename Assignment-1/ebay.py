from bungie import Adapter
import random
import asyncio
import logging
import uuid

from configuration import config
import Marketplace
from Marketplace import eBay, Order, Confirmation, PaymentEbay, PaymentPaypal, OrderDetails, UploadTracking, ItemShipped, PassDeliveryConfirmation, ReviewSubmission, ReleaseFund, ReviewTxn, DefectiveNotice, RequestDefectRefund, SendDefectRefund, DefectRefund, CancelOrder

#PaymentPaypal, OrderDetails

logger = logging.getLogger("eBay-Org")
adapter = Adapter(eBay, Marketplace.protocol, config)

@adapter.reaction(Order)
async def orderConfirmation(msg):
    logger.info(f'Received order from Buyer: {msg.payload}')
    adapter.send(
        Confirmation(
            blah='blah',
            **msg.payload
        )
    )
    

@adapter.reaction(PaymentEbay)
async def paymentConfirmation(msg):
    logger.info(f'Received Payment from Buyer: {msg.payload}')
    adapter.send (
        PaymentPaypal(
            hold = str(uuid.uuid4()),
            **msg.payload
        )
    )


#@adapter.reaction(Order)
#async def sendOrderDetails(msg):
#    adapter.send(
#        OrderDetails(
#            orderInfo = str(uuid.uuid4()),
#            **msg.payload
#        )
#    )
@adapter.enabled(OrderDetails)
async def sendOrderDetails(msg):
    msg["orderInfo"] = "orderInfo"
    return msg

@adapter.reaction(UploadTracking)
async def receivedTrackNum(msg):
    logger.info(f'Received Tracking Number from Merchant: {msg.payload}')
    adapter.send(
        ItemShipped(
            shipmentNotification = str(uuid.uuid4()),
            **msg.payload
        )
    )


@adapter.reaction(ReviewSubmission)
async def buyerReview(msg):
    logger.info(f'Review from Buyer received: {msg.payload}')


@adapter.reaction(PassDeliveryConfirmation)
async def merchantConfirmedDelivery(msg):
    logger.info(f'Order delivery to Buyer is confirmed by Merchant: {msg.payload}')
    adapter.send(
        ReleaseFund(
            fund = str(uuid.uuid4()),
            **msg.payload
        )
    )


@adapter.reaction(ReviewTxn)
async def reviewtxnReceived(msg):
    logger.info(f'Received transaction review from Merchant: {msg.payload}')



@adapter.reaction(DefectiveNotice)
async def defectiveItem(msg):
    logger.info(f'Received defective notification from Merchant: {msg.payload}')
    adapter.send(
        RequestDefectRefund(
            defRefundRequest = str(uuid.uuid4()),
            **msg.payload
        )
    )


@adapter.reaction(SendDefectRefund)
async def defectItemRefund(msg):
    logger.info(f'Received refund for defective item from PayPal: {msg.payload}')
    adapter.send(
        DefectRefund(
            defectiveRefund = str(uuid.uuid4()),
            **msg.payload
        )
    )

@adapter.reaction(CancelOrder)
async def cancelBuyerOrder(msg):
    logger.info(f'Order is cancelled by Buyer: {msg.payload}')


if __name__ == "__main__":
    logger.info("Starting eBay...")
    adapter.start()