import hashlib
import socket


class Triple:
    def __init__(self, ip, port):
        """
        Triple is all the information to communicate with other machines that use the program
        :param ip: the ip address of the machine
        :param port: the port that the program is communicate with
        """
        self.ip = ip
        self.port = port

        a = self.ip + str(self.port)
        a = hashlib.md5(a.encode('latin-1'))
        self.id = int(a.hexdigest(), 16)

    def create_socket(self):
        my_socket = socket.socket()

        my_socket.connect((self.ip, self.port))
        return my_socket
