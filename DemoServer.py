import mysql.connector
import datetime
import socket
import sys
import threading
from DemoServerFunctions import *
from mysql.connector import errorcode
from mysql.connector import pooling

class DemoServer:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))
		self.lock = threading.Lock()
		
	def listen(self):
		self.sock.listen(5)
		
		# set up DB credentials
		dbconfig = {
                "database": "Demo",
                "user": "Demo",
                "password": "flashbearslap",
                "host": "127.0.0.1"
		}
		
		# connect to the database
		try:
			#cnx = mysql.connector.connect(**dbconfig)
			cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "admin_pool", pool_size = 5, **dbconfig)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)
		else:
			print("Server ready\n")
			sys.stdout.flush()
			while True:
				client, address = self.sock.accept()
				
				#if not cnx.is_connected():
				#	try:
				#		cnx = mysql.connector.connect(**dbconfig)
				#	except mysql.connector.Error as err:
				#		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				#			print("Something is wrong with your user name or password")
				#			sys.stdout.flush()
				#		elif err.errno == errorcode.ER_BAD_DB_ERROR:
				#			print("Database does not exist")
				#			sys.stdout.flush()
				#		else:
				#			print(err)
				#			sys.stdout.flush()
							
				#self.listenToClient(client, address, cnx)
				#pooled_cnx = mysql.connector.connect(pool_name = "admin_pool")
				running = True
				while running:
					try:
						pooled_cnx = cnxpool.get_connection()
						threading.Thread(target = self.listenToClient,args = (client,address,pooled_cnx)).start()
						running = False
					except mysql.connector.PoolError as err:
						print(err)
						print("\n")
						
						#client.sendall("The server is handling too many connections right now. Please inform the developer that you encountered this message, then try again later.")
						pooled_cnx.close()
			cnx.close()
		sys.stdout.flush()
	# end of function
		

	def listenToClient(self, connection, address, cnx):
		# store the user's parsed message here
		user_message = ParseMessage(connection)
		drain_client_input(connection)
		
		#returned boolean or empty list
		if not user_message:
			connection.sendall("Something went wrong with the web client. Please contact the developer for help.")
		#returned list of queries and their parameters
		else:
			#print "Successfully parsed the message"
			#sys.stdout.flush()
				
			cursor = cnx.cursor()
				
			print(datetime.datetime.now())
			print("Received command " + user_message[0] + " with " + str(len(user_message[1])) + " parameters\n")
			HandleQuery(user_message[0], cursor, connection, cnx, user_message[1])
				
			cursor.close()
			
			#print(user_message[i], user_message[i+1])
			#sys.stdout.flush()
		#end of processing
		
		#print("Returning pool connection")
		sys.stdout.flush()
		cnx.close()
		connection.close()
	# end of function
	
def HandleQuery(option, sqlcursor, client_connection, sql_connection, insert_data=[]):
	#print("query: " + option)
	#sys.stdout.flush()

	#execute query
	if not insert_data:
		sqlcursor.execute(make_query(option+'.sql'))
	else:
		try:
			if (option == "FilterOrder"):
				user_option_data = {'serial': insert_data[0]}
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				
			elif (option == "ViewItemsSingle" or 
				option == "ViewUnits" or
				option == "FindOrder"):
				user_option_data = {'orderid': insert_data[0]}
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				
			elif (option == "InsertNewOrder"):
				user_option_data = {'client': insert_data[0], 
									'rfd': insert_data[1], 
									'ard': insert_data[2], 
									'accountmanager': insert_data[3], 
									'po': insert_data[4], 
									'rr': insert_data[5], 
									'rts': insert_data[6],
									'status': insert_data[7]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				
				sqlcursor.execute(make_query("InsertNewOrderDateB.sql"), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
				
			elif (option == "EditOrder"):
				user_option_data = {'orderid': insert_data[0],
									'client': insert_data[1], 
									'rfd': insert_data[2], 
									'ard': insert_data[3], 
									'accountmanager': insert_data[4], 
									'po': insert_data[5], 
									'rr': insert_data[6],
									'rts': insert_data[7],
									'status': insert_data[8]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
				
			elif (option == "InsertNewOrderDate"):
				user_option_data = {'orderid': insert_data[0],
									'dateordered': insert_data[1],
									'datedue': insert_data[2],
									'remarks': insert_data[3]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
				
			elif (option == "EditOrderDate"):
				user_option_data = {'listid': insert_data[0],
									'orderid': insert_data[1],
									'dateordered': insert_data[2],
									'datedue': insert_data[3],
									'remarks': insert_data[4]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
				
			elif (option == "InsertNewItem"):
				user_option_data = {'name': insert_data[0],
									'quantity': insert_data[1], 
									'serial': insert_data[2], 
									'source': insert_data[3], 
									'remarks': insert_data[4], 
									'status': insert_data[5],
									'orderid': insert_data[6]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				
				sqlcursor.execute(make_query("InsertNewItemB.sql"), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
				
			elif (option == "EditItem"):
				user_option_data = {'itemid': insert_data[0],
									'name': insert_data[1],
									'quantity': insert_data[2], 
									'serial': insert_data[3], 
									'source': insert_data[4], 
									'remarks': insert_data[5], 
									'status': insert_data[6]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
			
			elif (option == "InsertNewUnitPart"):
				user_option_data = {'itemid': insert_data[0],
									'part': insert_data[1],
									'serial': insert_data[2]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
			
			elif (option == "EditUnitPart"):
				user_option_data = {'listid': insert_data[0],
									'itemid': insert_data[1],
									'part': insert_data[2],
									'serial': insert_data[3]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
			
			elif (option == "DeleteOrder"):
				user_option_data = {'orderid': insert_data[0]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
				
			elif (option == "DeleteOrderDate"):
				user_option_data = {'listid': insert_data[0]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
				
			elif (option == "DeleteItem"):
				user_option_data = {'itemid': insert_data[0]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
				
			elif (option == "DeleteUnitPart"):
				user_option_data = {'listid': insert_data[0]}
				
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				sql_connection.commit()
				client_connection.sendall("Successfully completed the operation!")
				
			#elif (option):
			#	user_option_data = {}
			#	
			#	sqlcursor.execute(make_query(option+'.sql'), user_option_data)
			#	sql_connection.commit()
			#	client_connection.sendall("Successfully completed the operation!")
				
		except mysql.connector.Error as err:
			print(datetime.datetime.now())
			print(err)
			print "\r\n"
			FlushCursor(sqlcursor)
			sys.stdout.flush()
			
			sql_connection.rollback()
	
		except Exception as err2:
			print(datetime.datetime.now())
			print(err2)
			print "\r\n"
			FlushCursor(sqlcursor)
			sys.stdout.flush()
			
			sql_connection.rollback()
			
	#send results of view queries
	if (option == "ViewOrders" or
		option == "ViewOverdueOrders" or
		option == "ViewPullOutOrders" or
		option == "ViewReturnedOrders" or
		option == "ViewInHouseOrders" or
		option == "ViewDueOrders" or
		option == "FilterOrder" or
		option == "FindOrder"):
		ViewOrders(sqlcursor, client_connection)
	elif (option == "ViewItemsSingle"):
		ViewItemsSingle(sqlcursor, client_connection)
	elif (option == "ViewUnits"):
		ViewUnits(sqlcursor, client_connection)
	else:
		FlushCursor(sqlcursor)
		sys.stdout.flush()
	#sys.stdout.flush()
# end of function

# Web client sends messages of this format to this server:
# STARTMESSAGE\f
# STARTCOMMAND\f
# <insert query name here>\f
# ENDCOMMAND\f
# STARTCOMMAND\f
# <insert query name here>\f
# WITHINPUT\f
# <insert lines of parameters here>\f
# <insert lines of parameters here>\f
# ...
# ENDINPUT\f
# ENDCOMMAND\f
# ...
# ENDMESSAGE\f\n

def ParseMessage(client_connection):
	available_options = make_available_query_list()

	user_message = []
	insert_data = []
	keywords = ["STARTMESSAGE", "STARTCOMMAND", 
				"ENDCOMMAND", "WITHINPUT", "ENDINPUT", "ENDMESSAGE"]
	error = False

	# start parsing the message
	# must read STARTMESSAGE\f next
	user_option = get_client_input(client_connection)

	if user_option != "STARTMESSAGE":
		print(datetime.datetime.now())
		print "Message format is not valid. It should start with STARTMESSAGE\\f"
		print "\r\n"
		sys.stdout.flush()
		
		return error
		
	# read the message body
	else:
		# must read STARTCOMMAND\f next
		user_option = get_client_input(client_connection)
		
		# message cannot be empty
		if user_option == "ENDMESSAGE":
			print(datetime.datetime.now())
			print "Message format is not valid. Message body cannot be empty"
			print "\r\n"
			sys.stdout.flush()
			
			return error
			
		# after STARTMESSAGE\f, the next line must be STARTCOMMAND\f
		elif user_option != "STARTCOMMAND":
			print(datetime.datetime.now())
			print "Message format is not valid. It should start with STARTMESSAGE\\f"
			print "\r\n"
			sys.stdout.flush()
			
			return error
		
		# keep reading until the end of the message
		while user_option != "ENDMESSAGE":
			# read the query name
			user_option = get_client_input(client_connection)
			
			# check if the query name is invalid
			if user_option not in available_options:
				print(datetime.datetime.now())
				print user_option + " is not a valid query. Please copy the query name exactly"
				print "\r\n"
				sys.stdout.flush()
				
				return error
				
			# check if it came with parameters
			else:
				# reset the parameter placeholder
				insert_data = []
				
				# ADD THE QUERY NAME TO THE PARSED MESSAGE ##########
				user_message.append(user_option)
				
				# read WITHINPUT\f or ENDCOMMAND\f
				user_option = get_client_input(client_connection)
				
				# read parameters if there are
				if user_option == "WITHINPUT":
					# read the first parameter
					user_option = get_client_input(client_connection)
					
					# parameter list cannot be empty
					if user_option == "ENDINPUT":
						print(datetime.datetime.now())
						print "Parameters cannot be empty for " + insert_data[-1]
						print "\r\n"
						sys.stdout.flush()
						
						return error

					# must properly end list of parameters
					elif user_option in keywords:
						print(datetime.datetime.now())
						print "Can't use keywords as parameters"
						print "\r\n"
						sys.stdout.flush()
						
						return error
					
					# parse the list of parameters
					while user_option != "ENDINPUT":
						insert_data.append(user_option)
						user_option = get_client_input(client_connection)
					
					# must read ENDCOMMAND\f next
					user_option = get_client_input(client_connection)

					if user_option != "ENDCOMMAND":
						print(datetime.datetime.now())
						print "Message format is not valid. STARTCOMMAND\\f should end with ENDCOMMAND\\f"
						print "\r\n"
						sys.stdout.flush()
						
						return error
				# end of parameter parsing
						
				# don't read anything else if there aren't any parameters
				elif user_option == "ENDCOMMAND":
					pass
					
				# improper format
				elif user_option != "ENDCOMMAND":
					print(datetime.datetime.now())
					print "Message format is not valid. STARTCOMMAND\\f should end with ENDCOMMAND\\f"
					print "\r\n"
					sys.stdout.flush()
					
					return error
					
				# ADD THE COMMAND'S PARAMETER LIST TO PARSED MESSAGE ########
				user_message.append(insert_data)
			# end of command parsing
				
			# read the next STARTCOMMAND\f or ENDMESSAGE\f
			user_option = get_client_input(client_connection)

			if user_option != "STARTCOMMAND" and user_option != "ENDMESSAGE":
				print(datetime.datetime.now())
				print "Message format is not valid. Expected STARTCOMMAND\\f or ENDCOMMAND\\f"
				print "\r\n"
				sys.stdout.flush()
				
				return error
		# end of loop
		
		# finally, return the whole parsed message
		return user_message
	# end of function