import os
import socket
import sys

def getdir():
    """
    Gets the destination directory path from the user.
    :return: destination directory path and list of files already in the directory
    """
    addedfiles = []

    if len(sys.argv) < 2:
        destination = "destination"
    else:
        destination = sys.argv[1]
   
    if not(os.path.exists(destination)):
        os.mkdir(destination)
        print(f"Created directory {destination}\n\n")
    else:
        addedfiles += os.listdir(destination) 
            
    return destination, addedfiles

def createfullpath(destination, filename):
    """
    Creates the full path of the file.
    :param destination: destination directory path
    :param filename: name of the file
    :return: full path of the file
    """
    return os.path.join(destination, filename)

def connect(destination,addedfiles):
    """
    Connects to the client and receives files from the client.
    :param destination: destination directory path
    :param addedfiles: list of files already in the directory
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0',8080))
    server.listen(5)

    while True:
        client, addr = server.accept()
        print(f"Connection from {addr}")

        while True:
            filename = client.recv(4096).decode()
            if filename == "": break

            if not os.path.exists(os.path.join(destination, os.path.dirname(filename))):
                os.makedirs(os.path.join(destination, os.path.dirname(filename)))

            file = open(os.path.join(destination, filename),"w")
            client.send("Success".encode())

            contents = client.recv(4096).decode()
            if contents != f"\0":
                file.write(contents)
            file.close()
            client.send("Success".encode())

            print(f"Received file {filename}\n\n")
            addedfiles.append(filename)

        client.close()
        
if __name__ == "__main__":
    destination, addedfiles = getdir()
    connect(destination, addedfiles)