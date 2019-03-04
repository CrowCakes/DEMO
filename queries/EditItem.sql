UPDATE Items
SET Name = %(name)s,
Quantity = %(quantity)s,
Serial = %(serial)s,
Source = %(source)s,
Remarks = %(remarks)s,
Status = %(status)s
WHERE ItemID = %(itemid)s