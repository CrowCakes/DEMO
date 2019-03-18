DROP DATABASE IF EXISTS Demo;

CREATE DATABASE Demo;
USE Demo;

CREATE TABLE DemoOrder (
	OrderID int AUTO_INCREMENT PRIMARY KEY,
	Client varchar(50),
	RFD varchar(50),
	ARD varchar(50),
	AccountManager varchar(30),
	PO varchar(20),
	RR varchar(20),
	Status varchar(15)
);

CREATE TABLE DemoDuration (
	ListID int AUTO_INCREMENT PRIMARY KEY,
	OrderID int,
	DateOrdered date,
	DateDue date,
	Remarks varchar(300) DEFAULT 'n/a',
	
	FOREIGN KEY (OrderID) REFERENCES DemoOrder (OrderID)
	ON UPDATE CASCADE 
	ON DELETE CASCADE
);

CREATE TABLE Items (
	ItemID int AUTO_INCREMENT PRIMARY KEY,
	Name varchar(150),
	Quantity int,
	Serial varchar(30),
	Source varchar(100),
	Remarks varchar(300),
	Status varchar(15)
);

CREATE TABLE UnitParts (
	ListID int AUTO_INCREMENT PRIMARY KEY,
	ItemID int,
	Part varchar(100),
	Serial varchar(30),
	
	FOREIGN KEY (ItemID) REFERENCES Items (ItemID)
	ON UPDATE CASCADE 
	ON DELETE CASCADE
);

CREATE TABLE DemoOrderUnits (
	ListID int AUTO_INCREMENT PRIMARY KEY,
	OrderID int,
	ItemID int,
	
	FOREIGN KEY (ItemID) REFERENCES Items (ItemID)
	ON UPDATE CASCADE 
	ON DELETE CASCADE,
	FOREIGN KEY (OrderID) REFERENCES DemoOrder (OrderID)
	ON UPDATE CASCADE 
	ON DELETE CASCADE
);
ALTER TABLE DemoOrderUnits ADD UNIQUE OnlyOneOfEach(OrderID, ItemID);