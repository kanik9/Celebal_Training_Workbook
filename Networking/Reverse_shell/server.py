# importing important modules

import socket
import sys

# main script of server side

def create_socket():
    """
    This function is use to create socket to connect two computers.
    """
    try :
        global host
        global port
        global s

        host = ""
        port = 9999
        s = socket.socket()
        print("Done")
    except socket.error as msg:
        print("Socket Creation error : " + str(msg))


# Binding host and port together and perform listening operation for connections.
def bind_socket():
    try :
        global host
        global port
        global s

        print("Binding the port : " + str(port))
        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error : " + str(msg) + "\n" + "Retrying to bind the port : ")
        bind_socket()


# Establish the connection with a client and socket must be listening
def socket_accept():
    conn, address = s.accept()
    print("Connection has been establish" + " "+"IP" + " " + address[0] + " " + "Port" + " " +str(address[1]))
    print(conn)
    print(address)
    send_commands(conn)
    conn.close()


# Send commands to client
def send_commands(conn):
    """
    For execute more than 1 command when the socket is open we have to create infinite loop to open the socket for
    execute more than 1 command at a single socket
    """
    while True:
        cmd = input()

        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()

        else:
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024), "utf-8")
                print(client_response, end="\n")




def main():
    create_socket()
    bind_socket()
    socket_accept()




if __name__ == "__main__":
    main()
