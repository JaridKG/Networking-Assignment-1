__author__ = 'BrendonH'

import sys
import socket

#from ephemeral.py, not entirely sure how to use it yet
def getEphemeralPort():
    # Create a socket
    welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to port 0
    welcomeSocket.bind(('',0))

    # Retreive the ephemeral port number
    print("I chose ephemeral port: ", welcomeSocket.getsockname()[1])

    return welcomeSocket



def put(dataSock, fileName):
    #need to check if file name is valid

    # The name of the file
    # fileName = "file.txt"

    # Open the file
    fileObj = open(fileName, "r")



    # The number of bytes sent
    numSent = 0

    # The file data
    fileData = None

    # Keep sending until all is sent
    while True:

        # Read 65536 bytes of data
        fileData = fileObj.read(65536)

        # Make sure we did not hit EOF
        if fileData:


            # Get the size of the data read
            # and convert it to string
            dataSizeStr = str(len(fileData))

            # Prepend 0's to the size string
            # until the size is 10 bytes
            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr


            # Prepend the size of the data to the
            # file data.
            fileData = dataSizeStr + fileData

            # The number of bytes sent
            numSent = 0

            # Send the data!
            while len(fileData) > numSent:
                numSent += dataSock.send(fileData.encode('ascii'))    #this is where it breaks right now

        # The file has been read. We are done
        else:
            break


    print("Sent ", numSent, " bytes.")

    # Close the socket and the file
    dataSock.close()
    fileObj.close()

def lsCommand(tempSock):
    bytes_sent = 0
    #While loop that modifies bytes sent

    #Send request to server for list of
    #Files in the folder

    #Print list

    #Close


def sendCommand(commandString, connSock):
    # send command
    commandString = str(len(commandString)) + " " + commandString   #prepend size of command string
    bytes_sent = 0
    while bytes_sent < len(commandString):
        bytes_sent += connSock.send(commandString.encode('ascii'))



def main(argv):

    # Command line checks
    if len(argv) < 2:
        print("USAGE python " + argv[0] + " <FILE NAME>")

    while True:


        # Server address
        serverAddr = argv[1]

        # Server port
        serverPort = int(argv[2])

        # Create a TCP socket
        connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        connSock.connect((serverAddr, serverPort))

        commandString = input("ftp> ")
        command = commandString.split()   #splits string into list of words



        if(command[0].lower() == "get"):
            pass    #pass is a placeholder for the eventual function get() function that will be called
        elif(command[0].lower() == "put"):
            welcomeSock = getEphemeralPort()

            commandString = commandString + " " + str(welcomeSock.getsockname()[1])

            welcomeSock.listen(1)
            sendCommand(commandString, connSock)
            dataSock, addr = welcomeSock.accept()
            put(dataSock, command[1])
        elif(command[0].lower() == "ls"):
            tempSocket = getEphemeralPort()
            lsCommand(tempSocket)


        elif(command[0].lower() == "quit"):
            #Send message to server saying to shut down
            #Wait for response saying it is shutting down
            #Shut down
            sys.exit(0)
        else:
            print("Invalid command")



if __name__ == "__main__":
    main(sys.argv)
