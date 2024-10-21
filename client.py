import os
import socket
import hashlib
import sys

def getdir():
    '''
    Gets the source directory path from the user, if no path entered it returns the current working directory.
    :return: source directory path
    '''
    if len(sys.argv) < 2:
        source = os.getcwd()
        return source
    
    return sys.argv[1]

def sendfiles(newfiles, source):
    '''
    Sends all new files to the server.
    :param newfiles: list of new files
    :param source: source directory path
    :return: list of successfully added files
    '''
    successfullyadded = []
    newcontents = [] # stores hash of new contents
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('0.0.0.0',8080))

    for f in newfiles:
        client.send(f"{f}".encode())

        server_msg = client.recv(4096).decode()
        if server_msg != "Success":
            print(f"Error with file {f}")
            return []
        
        contents = open(os.path.join(source, f),"r").read()

        if contents == "":
            contents = f"\0"

        client.send(f"{contents}".encode())
        server_msg = client.recv(4096).decode()
        if server_msg != "Success":
            print(f"Error with file {f}")
            return []
        
        successfullyadded.append(f)
        newcontents.append(hashlib.md5(contents.encode()).hexdigest())

    client.close()
    return successfullyadded, newcontents

def getfiles(source):
    '''
    Gets all files from the source directory and sends any new ones to the server.
    :param source: source directory path
    '''
    addedfiles=[]
    addedcontents=[] # stores hash of added contents

    for f in os.listdir(source):
        if not(os.path.isdir(os.path.join(source, f))):
            addedcontents.append(hashlib.md5(open(os.path.join(source, f),"r").read().encode()).hexdigest())

    count = 0
    while True:
        allfilenames = [f for f in os.listdir(source) if not(os.path.isdir(os.path.join(source, f)))]

        newfiles = [f for f in allfilenames if f not in addedfiles]
        if len(newfiles)!=0: print(f"New files: {newfiles}")

        for i, f in enumerate(addedfiles):
            if hashlib.md5(open(os.path.join(source, f),"r").read().encode()).hexdigest() != addedcontents[i]:
                newfiles.append(f)
                addedcontents.pop(i)
                addedfiles.pop(i)

        if len(newfiles)==0:
            continue

        try:
            newlyaddedfiles,newcontents=sendfiles(newfiles, source)
            addedfiles+=newlyaddedfiles
            addedcontents+=newcontents
            count+=1
            
        except Exception as e:
            print(f"Error: {e}")
            return


if __name__ == "__main__":
    source = getdir()
    getfiles(source)