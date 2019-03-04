SELECT A.OrderID, A.Client, A.RFD, A.ARD, A.AccountManager, A.Status,
B.ListID, B.DateOrdered, B.DateDue, B.Remarks
FROM DemoOrder as A 
INNER JOIN DemoDuration as B
ON A.OrderID = B.OrderID
WHERE Status = "Active" AND
TO_DAYS(B.DateDue) - TO_DAYS(NOW()) < 0
ORDER BY B.DateDue DESC, A.OrderID, B.ListID