INSERT INTO DemoDuration(OrderID, DateOrdered, DateDue, Remarks)
VALUES (LAST_INSERT_ID(), DATE(NOW()), DATE(NOW()), "n/a")