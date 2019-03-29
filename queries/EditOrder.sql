UPDATE DemoOrder
SET Client = %(client)s,
RFD = %(rfd)s,
ARD = %(ard)s,
AccountManager = %(accountmanager)s,
PO = %(po)s,
RR = %(rr)s,
RTS = %(rts)s,
Status = %(status)s
WHERE OrderID = %(orderid)s