UPDATE DemoOrder
SET Client = %(client)s,
RFD = %(rfd)s,
ARD = %(ard)s,
AccountManager = %(accountmanager)s,
Status = %(status)s
WHERE OrderID = %(orderid)s