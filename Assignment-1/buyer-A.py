from bungie import Adapter
import random
import asyncio
import logging
import uuid

from configuration import config, marketplace
import Marketplace
from Marketplace import Buyer, Order, Confirmation, PaymentEbay, ShipPackedItem, ItemShipped, ItemReceived, ReviewSubmission, DefectRefund, CancelOrder

#ItemShipped, DeliveryConfirmation

logger = logging.getLogger("Buyer-A")
#logging.getLogger('bungie').setLevel(logging.DEBUG)
adapter = Adapter(marketplace.roles['Buyer'], Marketplace.protocol, config)


@adapter.reaction(Confirmation)
async def handle_confirmation(msg):
    logger.info(f'Got confirmation message: {msg}'
    )
    print('abc', flush=True)


async def order_generator():
    await asyncio.sleep(2)
    for orderID in range(1):
        name = random.sample(['Tony', 'Steve', 'Clark'] , 1)[0],
        address = random.sample(['808 SW Queen St', '2725 Barbie St', '216 Santa Claus St'] , 1)[0],
        payment = str(uuid.uuid4()) 
        
        adapter.send(
            Order(
                orderID=orderID,
                name=name,
                address=address
            )
        )
        adapter.send(
            PaymentEbay(
                payment=payment,
                orderID=orderID,
                name=name,
                address=address
            )
        )
        if random.random() < 0.7:
            adapter.send(
                CancelOrder(
                    orderID=orderID,
                    payment=payment,
                    cancel=str('Cancel order')
                )
            )
    

#@adapter.reaction(ShipPackedItem)
#async def receivedItem(msg):
    #await asyncio.sleep(0.01)
    #logger.info(f'Received item from Shipper: {msg.payload}')

@adapter.reaction(ItemShipped)
async def itemShippedNotice(msg):
    logger.info(f'Received eBay notification that item was shipped: {msg.payload}')


@adapter.enabled(ItemReceived)
async def receivedItem(msg):
    logger.info(f'Received order from Shipper: {msg.payload}')
    adapter.send(
        ItemReceived(
            orderReceived = str(uuid.uuid4()),
            **msg.payload
        )
    )
    adapter.send(
        ReviewSubmission(
            review = str(uuid.uuid4()),
            **msg.payload
        )
    )


@adapter.reaction(DefectRefund)
async def refundReceived(msg):
    logger.info(f'Received refund for defective item from eBay: {msg.payload}')


#@adapter.reaction(DefectRefund)
#async def defectItemRefund(msg):
#    logger.info(f'Received refund for defective item from PayPal: {msg.payload}')

if __name__ == "__main__":
    logger.info("Starting Buyer...")
    adapter.start(order_generator())