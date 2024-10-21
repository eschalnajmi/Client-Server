import os
import glob
import socket
import hashlib
import sys
import pathlib

def getdir():
    """
    Gets the source directory path from the user, if invalid path is entered, prompts the user to enter again.
    :return: source directory path
    """
    if len(sys.argv) < 2:
        return os.getcwd()
    
    return os.path.join(os.getcwd(),sys.argv[1])

def recursiveget(source, f):
    """
    Recursively gets directories.
    :param source: source directory path
    :param f: file or directory name
    :return: full path of the file or directory
    """
    allfiles = []
    fullpath = os.path.join(source, f)
    print(f"FULL PATH: {fullpath}")
    for file in os.listdir(fullpath):
        if os.path.isdir(file):
            allfiles+=recursiveget(fullpath, file)
        else:
            allfiles.append(os.path.join(fullpath,file))

    return allfiles

def sendfiles(newfiles, source):
    """
    Sends all new files to the server.
    :param newfiles: list of new files
    :param source: source directory path
    :return: list of successfully added files and their contents
    """
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
        print(f"Sent file {f}\n\n")

    client.close()
    return successfullyadded,newcontents

def getfiles(source):
    """
    Gets all files from the source directory and sends any new ones to the server.
    :param source: source directory path
    """
    addedfiles=[]
    addedcontents=[] # stores hash of added contents

    for f in list(glob.glob(os.path.join(source, "*"))):
        addedcontents.append(hashlib.md5(open(os.path.join(source, f),"r").read().encode()).hexdigest())

    count = 0
    while True:
        for f in list(glob.glob(os.path.join(source, "*"))):
            if os.path.isfile(f):
                allfilenames = os.listdir(source)
        
        newfiles = [f for f in allfilenames if f not in addedfiles]

        if count !=0 and count % 5 == 0:
            for i, f in enumerate(addedfiles):
                if hashlib.md5(open(os.path.join(source, f),"r").read().encode()).hexdigest() != addedcontents[i]:
                    print(f"File {f} has been modified.")
                    newfiles.append(f)
                    addedcontents.pop(i)
                    addedfiles.pop(i)


        if len(newfiles)==0:
            count+=1
            continue

        try:
            newlyaddedfiles,newcontents=sendfiles(newfiles, source)
            addedfiles+=newlyaddedfiles
            print(f"added the files {newlyaddedfiles}")
            addedcontents+=newcontents
            count+=1
            
        except Exception as e:
            print(f"Error: {e}")
            return


if __name__ == "__main__":
    source = getdir()

    print(f"SOURCE: {source}")

    for f in os.listdir(source):
        print("F: ",f)
        if(os.path.isfile(f)):
            print("file " + f)

        if os.path.isdir(f):
            print("directory " + recursiveget(source, f))
    
    #getfiles(source)