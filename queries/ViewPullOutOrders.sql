SELECT A.OrderID, A.Client, A.RFD, A.ARD, A.AccountManager, A.PO, A.RR, A.RTS, A.Status,
B.ListID, B.DateOrdered, B.DateDue, B.Remarks
FROM DemoOrder as A 
INNER JOIN DemoDuration as B
ON A.OrderID = B.OrderID
WHERE Status = "Pullout"
ORDER BY A.OrderID, B.DateDue ASC