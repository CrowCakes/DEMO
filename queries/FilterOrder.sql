SELECT A.OrderID, A.Client, A.RFD, A.ARD, A.AccountManager, A.PO, A.RR, A.RTS, A.Status,
B.ListID, B.DateOrdered, B.DateDue, B.Remarks
FROM DemoOrder as A 
INNER JOIN DemoDuration as B
ON A.OrderID = B.OrderID
INNER JOIN DemoOrderUnits as C
ON A.OrderID = C.OrderID
INNER JOIN Items as D
ON C.ItemID = D.ItemID
INNER JOIN UnitParts as E
ON D.ItemID = E.ItemID
WHERE D.Serial REGEXP %(serial)s OR E.Serial REGEXP %(serial)s
ORDER BY A.OrderID, B.DateDue ASC