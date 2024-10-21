import os
import socket

def getdir():
    '''
    Gets the destination directory path from the user.
    :return: destination directory path and list of files already in the directory
    '''
    addedfiles = []
    destination = input("Enter the destination directory path: ")

    if not(os.path.exists(destination)):
        os.mkdir(destination)
        print(f"Created directory {destination}\n\n")
    else:
        addedfiles += os.listdir(destination) 
            
    return destination, addedfiles

def connect(destination,addedfiles):
    '''
    Connects to the client and receives files from the client.
    :param destination: destination directory path
    :param addedfiles: list of files already in the directory
    '''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0',8080))
    server.listen(5)

    while True:
        client, addr = server.accept()
        print(f"Connection from {addr}")

        while True:
            filename = client.recv(4096).decode()
            if filename == "": break
            file = open(os.path.join(destination, filename),"w")
            client.send("Success".encode())

            contents = client.recv(4096).decode()
            if contents != f"\0":
                file.write(contents)
            file.close()
            client.send("Success".encode())

            addedfiles.append(filename)

        client.close()
        
if __name__ == "__main__":
    destination, addedfiles = getdir()
    connect(destination, addedfiles)