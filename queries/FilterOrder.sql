SELECT A.*,
B.ListID, B.DateOrdered, B.DateDue, B.Remarks
FROM DemoOrder as A 
INNER JOIN DemoDuration as B
ON A.OrderID = B.OrderID
INNER JOIN DemoOrderUnits as C
ON A.OrderID = C.OrderID
INNER JOIN Items as D
ON C.ItemID = D.ItemID
WHERE D.Serial LIKE %(serial)s
ORDER BY A.OrderID