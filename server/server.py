import socket
from threading import Thread
import pickle
from Interface import Interface
import sys

class ListenClients(Thread):
    def __init__(self, sock, self_ip, self_port):
        Thread.__init__(self)
        self.sock = sock
        self.ip = self_ip
        self.port = self_port
        print("Client connected!")

    def run(self):
        data_rcv = self.sock.recv(1024*1024)
        loaded_data = pickle.loads(data_rcv)
        method_name = loaded_data["function_name"]
        parameters = loaded_data["function_params"]
        int_obj = globals()['Interface']()
        func = getattr(int_obj, method_name)
        response_data = {}
        try:
            result = func(*parameters)
            if result[0] == 200:
                response_data["status"] = "success"
                response_data["response"] = result[1]
                converted_data = pickle.dumps(response_data)
                self.sock.sendall(converted_data)
                print("Function executed succesfully")
            elif result[0] == 205:
                response_data["status"] = "failure"
                response_data["response"] = result[1]
                converted_data = pickle.dumps(response_data)
                self.sock.sendall(converted_data)
                print("Error occured in executing the function: ", result[1])
        except:
            response_data["status"] = "failure"
            response_data["response"] = sys.exc_info()[1]
            converted_data = pickle.dumps(response_data)
            self.sock.sendall(converted_data)
            print("Error occured in executing the function: ", sys.exc_info()[1])
        self.sock.close()


self_ip = "10.42.0.228"
self_port = 12344
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((self_ip, self_port))


while True:
    tcpsock.listen(1000)
    (conn, (ip,port)) = tcpsock.accept()
    listenthread = ListenClients(conn, self_ip, self_port)
    listenthread.daemon = True
    listenthread.start()