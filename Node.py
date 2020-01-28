import socket
import hashlib
import Triple
import KBucket
import KBucketList


class Node:
    def __init__(self, port):
        """

        :param port: the port the node is communicate on
        """
        # port
        self.port = port

        # generate id
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        a = ip + str(self.port)
        a = hashlib.md5(a.encode('latin-1'))
        self.my_id = int(a.hexdigest(), 16)

        # routing table
        self.routing_table = KBucketList(self.my_id)

        # my shared files
        self.my_shared_files = []

        # storage
        self.storage = []

    def node_lookup(self, node_id):
        """
        search for a node with the kademlia algorithm
        :param node_id:
        :return: KBucket obj of the K closest nodes triples to the node_id param
        """
        pass

    def store_file(self, file_name, kbucket):    # todo: check why i wrote kbucket param
        pass

    def file_lookup(self, file_name):
        pass

    def ping(self, triple):
        pass

    def pong(self, triple):
        pass
