import hashlib
import socket
import utility


class Triple:
    def __init__(self, ip, port, **kwargs):
        """
        Triple is all the information to communicate with other machines that use the program
        :param ip: the ip address of the machine
        :param port: the port that the program is communicate with
        """
        self.ip = ip
        self.port = port

        for key in kwargs:
            print(kwargs)
            if key == 'id':
                self.id = kwargs.get(key)
            else:
                self.id = utility.calc_id(self.ip, self.port)

    def create_socket(self):
        my_socket = socket.socket()

        my_socket.connect((self.ip, self.port))
        return my_socket
