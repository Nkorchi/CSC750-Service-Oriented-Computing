from protocheck import bspl
marketplace = bspl.load_file('marketplace.bspl').export('Marketplace')

from Marketplace import Buyer, eBay, PayPal, Merchant, Shipper
from Marketplace import (
    Order,
    PaymentEbay,
    PaymentPaypal,
    OrderDetails,
    HoldNotice,
    SendItem,
    ShipPackedItem,
    Tracking,
    UploadTracking,
    ItemShipped,
    ItemReceived,
    DeliveryConfirmation,
    PassDeliveryConfirmation,
    ReviewSubmission,
    ReleaseFund,
    SendFund,
    ReviewTxn,
    Defective,
    DefectiveNotice,
    RequestDefectRefund,
    SendDefectRefund,
    DefectRefund,
    CancelOrder
)

    #ItemShipped,
    #DeliveryConfirmation

config = {
    Buyer: ('0.0.0.0', 8000),
    eBay: ('0.0.0.0', 8001),
    PayPal: ('0.0.0.0', 8002),
    Merchant: ('0.0.0.0', 8003),
    Shipper: ('0.0.0.0', 8004)
}