import mysql.connector
import os
import socket
import sys
from datetime import date

def InputQueries():
	input_queries = []
	return input_queries
	
# Construct a query from a multiline sql file in queries subdirectory
def make_query(filename):
	query = ""
	query_dir = os.path.dirname(__file__)
	rel_path = os.path.join("queries", filename)
	abs_path = os.path.join(query_dir, rel_path)
	for line in open(abs_path):
		query += line
	return query
# end of function

# Listen for and construct user client input
def get_client_input(socket_connection):
	data = ""
	#print "Waiting for input from user client"
	while True:
		stream_data = socket_connection.recv(1)
		#reached the end of the form
		if stream_data == '\f':
			break
		else:
			data += stream_data
  #print "Received data:", data
	return data
# end of function

# Listen for and construct user client input
def drain_client_input(socket_connection):
	data = ""
	#print "Waiting for input from user client"
	while True:
		stream_data = socket_connection.recv(1)
		#reached the end of the form
		if stream_data == '\n':
			break
		else:
			data += stream_data
  #print "Received data:", data
	return data
# end of function

# fetch the list of valid queries that the server should handle
def make_available_query_list():
	available_options = []
	for line in open('querylist.txt'):
		fline = line.rstrip()
		available_options.append(fline)
	return available_options
	
def FlushCursor(sqlcursor):
	print("Flushing cursor")
	for line in sqlcursor:
		print(line)
	print("\r\n")
	
def ViewOrders(sqlcursor, connection):
	for (OrderID, Client, RFD, ARD, AccountManager, Status, ListID, DateOrdered, DateDue, Remarks) in sqlcursor:
		connection.sendall(("{}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::\n").format(OrderID, Client, RFD, ARD, AccountManager, Status, ListID, DateOrdered, DateDue, Remarks))
		#print(("{}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::\n").format(OrderID, Client, RFD, ARD, AccountManager, Status, ListID, DateOrdered, DateDue, Remarks))
		
def ViewItemsSingle(sqlcursor, connection):
	for (ItemID, Name, Quantity, Serial, Source, Remarks, Status) in sqlcursor:
		connection.sendall(("{}::, {}::, {}::, {}::, {}::, {}::, {}::\n").format(ItemID, Name, Quantity, Serial, Source, Remarks, Status))
		print(("{}::, {}::, {}::, {}::, {}::, {}::, {}::\n").format(ItemID, Name, Quantity, Serial, Source, Remarks, Status))
		
def ViewUnits(sqlcursor, connection):
	for (ListID, ItemID, Part) in sqlcursor:
		connection.sendall(("{}::, {}::, {}::\n").format(ListID, ItemID, Part))
		print(("{}::, {}::, {}::\n").format(ListID, ItemID, Part))