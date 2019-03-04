SELECT B.ListID, B.ItemID, B.Part
FROM DemoOrder AS A
INNER JOIN DemoOrderUnits as C
ON A.OrderID = C.OrderID
INNER JOIN UnitParts AS B
ON C.ItemID = B.ItemID
WHERE A.OrderID = %(orderid)s