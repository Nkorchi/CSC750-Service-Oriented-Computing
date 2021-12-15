from bungie import Adapter
import random
import asyncio
import logging
import uuid

from configuration import config
import Marketplace
from Marketplace import Shipper, SendItem, ShipPackedItem, Tracking, ItemReceived, DeliveryConfirmation, Defective


logger = logging.getLogger("Shipping-A")
logging.getLogger('Shipping-A').setLevel(logging.DEBUG)
adapter = Adapter(Shipper, Marketplace.protocol, config)

@adapter.reaction(SendItem)
async def orderItem(msg):
    logger.info(f'Received item from Merchant: {msg.payload}')

    if random.random() > 0.3:
        adapter.send(
            ShipPackedItem(
                shipping = msg.payload['item'],
                **msg.payload
            )
        )
        trackNum = str(uuid.uuid4())
        adapter.send(
            Tracking(
                trackNum = trackNum,
                **msg.payload
            )
        )
    else:
        adapter.send(
            Defective(
                defect = str(uuid.uuid4()),
                **msg.payload
            )
            #adapter.send()
        )


    

@adapter.reaction(ItemReceived)
async def deliveryConfirmed(msg):
    #logger.info(f'Buyer received the order: {msg.payload}')
    #trackNum = str(uuid.uuid4())
    adapter.send(
        DeliveryConfirmation(
            #trackNum = trackNum,
            delivered = str(uuid.uuid4()),
            **msg.payload
        )
    )



if __name__ == "__main__":
    logger.info("Starting Shipper...")
    adapter.start()