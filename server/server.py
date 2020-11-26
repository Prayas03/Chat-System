from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import os
from client import Person

#GLOBAL VARIABLE
HOST = 'localhost'
PORT = 8081
BUFFSIZE = 512
SERVER = socket(AF_INET, SOCK_STREAM)
X = (HOST,PORT)
SERVER.bind(X)

persons = []

def broadcast(msg, name):
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name + ": ", "utf8") + msg)
        except Exception as e:
            print("[ERROR]", e)        


def client_communcation(person):

    client = person.client
    addr = person.addr

    name = client.recv(BUFFSIZE)

    while True:
        name = client.recv(BUFFSIZE).decode("utf8")
        msg = f"{name} has joined the chat!"
        broadcast(name)


        if msg == bytes("{quit}", "utf8"):
            client.close()
            persons.remove(person)
            broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
            print(f"[DISCONNECTED] {name} disconnected")
            break
        else:
            client.send(msg, name)

            
def wait_for_connection():

    while True:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, name, client)
            person.append(person)

            print(f"CONNECTED {addr} connected to the server at {time.time()}")
            Thread(target=client_communcation, args=(person,)).start()
            
        except Exception as e:
            print("FAILURE, cant connect to the server", e)
            break




if __name__ == "__main__":
    SERVER.listen(5)
    print('Waiting for connection...')
    ACCEPT_THREAD = Thread(target=wait_for_connection, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    

