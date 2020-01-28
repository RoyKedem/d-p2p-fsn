import hashlib


class Triple:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.id = hashlib.md5(self.ip + str(self.port))

    def create_socket(self):
        pass
