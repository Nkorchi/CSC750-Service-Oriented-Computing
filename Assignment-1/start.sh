#!/bin/bash
set -euo pipefail

/usr/bin/python3.7 buyer-A.py &
BUYERA=$!
/usr/bin/python3.7 buyer-B.py &
BUYERB=$!

/usr/bin/python3.7 ebay.py &
EBAY=$!

/usr/bin/python3.7 paypal.py &
PAYPAL=$!

/usr/bin/python3.7 merchant.py &
MERCHANT=$!

/usr/bin/python3.7 shipper.py &
SHIPPER=$!

read -n1 -rsp $'Press any key to stop...\n'
kill -9 $BUYERA $EBAY $PAYPAL $MERCHANT $SHIPPER $BUYERB