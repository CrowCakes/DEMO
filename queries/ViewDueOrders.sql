SELECT A.OrderID, A.Client, A.RFD, A.ARD, A.AccountManager, A.PO, A.RR, A.RTS, A.Status,
C.ListID, C.DateOrdered, C.DateDue, C.Remarks
FROM DemoOrder as A 
INNER JOIN 
(SELECT B.*
FROM DemoDuration AS B INNER JOIN
(SELECT OrderID, MAX(DateDue) as Due
FROM DemoDuration
GROUP BY OrderID) A
ON B.OrderID = A.OrderID AND B.DateDue = A.Due) C
ON A.OrderID = C.OrderID
WHERE (Status = "Active" OR Status = "Internal") AND
(TO_DAYS(C.DateDue) - TO_DAYS(NOW()) <= 7)
ORDER BY C.DateDue DESC, A.OrderID