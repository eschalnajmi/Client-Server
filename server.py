import os
import socket

def getdir():
    addedfiles = []
    destination = input("Enter the destination directory path: ")

    if not(os.path.exists(destination)):
        os.mkdir(destination)
        print(f"Created directory {destination}\n\n")
    else:
        addedfiles += os.listdir(destination) 
            
    return destination, addedfiles

def connect(destination,addedfiles):
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
            print(f"Created file {filename}")
            client.send("Success".encode())

            contents = client.recv(4096).decode()
            if contents != f"\0":
                file.write(contents)
            file.close()
            print(f"Written contents {filename}")
            client.send("Success".encode())

            print(f"Received file {filename}\n\n")
            addedfiles.append(filename)

        client.close()
        
if __name__ == "__main__":
    destination, addedfiles = getdir()
    connect(destination, addedfiles)