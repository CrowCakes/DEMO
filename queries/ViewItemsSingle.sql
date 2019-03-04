SELECT B.ItemID, B.Name, B.Quantity, B.Serial, B.Source, B.Remarks, B.Status
FROM DemoOrder AS A
INNER JOIN DemoOrderUnits as C
ON A.OrderID = C.OrderID
INNER JOIN Items AS B
ON C.ItemID = B.ItemID
WHERE A.OrderID = %(orderid)s