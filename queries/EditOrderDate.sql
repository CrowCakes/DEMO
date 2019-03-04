UPDATE DemoDuration
SET OrderID = %(orderid)s, 
DateOrdered = %(dateordered)s, 
DateDue = %(datedue)s, 
Remarks = %(remarks)s
WHERE ListID = %(listid)s