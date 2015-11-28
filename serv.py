__author__ = 'BrendonH'
import sys
import socket

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):
	# The buffer
	recvBuff = ""

	# The temporary buffer
	tmpBuff = ""

	# Keep receiving till all is received
	while len(recvBuff) < numBytes:

		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes).decode('ascii')  #had to add.decode for it to work

		# The other side has closed the socket
		if not tmpBuff:
			break



		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	return recvBuff


def put(fileName, dataSock):


	# The buffer to all data received from the
	# the client.
	fileData = ""
	# The temporary buffer to store the received
	# data.
	recvBuff = ""
	# The size of the incoming file
	fileSize = 0
	# The buffer containing the file size
	fileSizeBuff = ""
	# Receive the first 10 bytes indicating the
	# size of the file
	fileSizeBuff = recvAll(dataSock, 10)	#This is where it breaks for this file
	# Get the file size
	fileSize = int(fileSizeBuff)
	print("The file size is ", fileSize)
	# Get the file data
	fileData = recvAll(dataSock, fileSize)
	print("The file data is: ")
	print(fileData)

def getCommand(sock):
	commandBytes = int(recvAll(sock,3))	#receive 1st 3 bytes (2-byte number and a space) indicating command size
	return recvAll(sock, commandBytes)	#receive the remaining command


def main(argv):
	if len(argv) > 1:
#         from sendfileserv.py
		# Accept connections forever
		# The port on which to listen
		listenPort = int(argv[1])

		# Create a welcome socket.
		welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Bind the socket to the port
		welcomeSock.bind(('', listenPort))

		# Start listening on the socket
		welcomeSock.listen(1)
		while True:

			print ("Waiting for connections...")

			# Accept connections
			clientSock, addr = welcomeSock.accept()

			print ("Accepted connection from client: ", addr)
			print ("\n")
			clientCommand = getCommand(clientSock)
			clientCommand = clientCommand.split()

			if(clientCommand[0].lower() == "get"):
				pass    #pass is a placeholder for the eventual function get() function that will be called
			elif(clientCommand[0].lower() == "put"):
				# connect to datasocket
				dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				dataSock.connect(("localhost", int(clientCommand[2])))	#addr[0] is the address the last socket connected to, clientCommand[2] is the ephemeral port sent by client
				dataSock.listen(1)
				put(clientCommand[1], dataSock)
			elif(clientCommand[0].lower() == "ls"):
				pass
			elif(clientCommand[0].lower() == "quit"):
				#function for sending quit goes here
				sys.exit(0)
			# put(clientSock)

			# Close our side
			clientSock.close()


if __name__ == "__main__":
	main(sys.argv)