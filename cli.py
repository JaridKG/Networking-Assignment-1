__author__ = 'BrendonH'

import sys
import socket


def put(serverAddr, serverPort, fileName):  #this works for now but will need to work with a seperate connection
    #need to check if file name is valid

    # The name of the file
    # fileName = "file.txt"

    # Open the file
    fileObj = open(fileName, "r")

    # Create a TCP socket
    connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    connSock.connect((serverAddr, serverPort))

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
                numSent += connSock.send(fileData[numSent:].encode('ascii'))

        # The file has been read. We are done
        else:
            break


    print("Sent ", numSent, " bytes.")

    # Close the socket and the file
    connSock.close()
    fileObj.close()

def main(argv):

    # Command line checks
    if len(argv) < 2:
        print("USAGE python " + argv[0] + " <FILE NAME>")

    while True:
        command = input("ftp> ")
        command = command.split()   #splits string into list of words

        # Server address
        serverAddr = argv[1]

        # Server port
        serverPort = int(argv[2])


        if(command[0].lower() == "get"):
            pass    #pass is a placeholder for the eventual function get() function that will be called
        elif(command[0].lower() == "put"):
            put(serverAddr,serverPort, command[1])
        elif(command[0].lower() == "ls"):
            pass
        elif(command[0].lower() == "quit"):
            #function for sending quit goes here
            sys.exit(0)
        else:
            print("Invalid command")







if __name__ == "__main__":
    main(sys.argv)