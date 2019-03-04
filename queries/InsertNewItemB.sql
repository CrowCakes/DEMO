INSERT INTO DemoOrderUnits(OrderID, ItemID) 
VALUES (%(orderid)s, LAST_INSERT_ID())