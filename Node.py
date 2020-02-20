import socket
from threading import Thread
import hashlib
from Triple import Triple
from KBucket import KBucket
from KBucketList import KBucketList
from TempTable import *
import random
# todo: create config file

alpha = 1


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

    # todo: parallelism
    def node_lookup(self, target_id):
        """
        search for a node with the kademlia algorithm
        :param target_id:
        :return: KBucket obj of the K closest nodes triples to the node_id param
        """
        # step 1
        # x is a kbucket object that holds the triples of the k closets node
        # todo: check if it is a pointer or not
        # todo: change name - x
        x = self.routing_table.kbucket_lookup(target_id)

        # step 2
        # choose random alpha nodes
        alpha_nodes = []
        for i in range(0, alpha):
            # todo: choices must be different
            alpha_nodes.append(random.choice(x))

        # step 3
        k = TempTable(alpha_nodes)

        # step 4
        i = 0
        alpha_nodes = []
        # find the closest triple to the target that hasn't been queried yet
        while (not k.node_lookup_table[i].queried) and len(alpha_nodes) < 3:
            alpha_nodes.append(k.node_lookup_table[i])
        # send the FIND_NODE RPCs
        msg = "FIND_NODE##" + target_id
        for node_connection in alpha_nodes:
            sock = node_connection.create_socket()\
            sock.send(msg)

        # step 5
            node_connection.queried = True

        # step 6
        


    def main_thread(self):
        """
        the main thread handle all the connections creations and RPCs
        it opens server socket
        :return:
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', self.port))

        server_socket.listen(5)     # todo: replace with const

        clients = []    # holds all the clients sockets
        while True:
            (client_socket, client_address) = server_socket.accept()
            clients.append(client_socket)
            a = Thread(target=handle_rpc, args=(client_socket,))    # todo: add the object to params to fix error
            a.start()

    def handle_rpc(self, client_socket):
        """
        handle all client RPCs
        :param client_socket: socket object to communicate with clients
        :return:
        """
        while True:
            rpc = client_socket.recv(1024)
            rpc.decode()
            rpc = rpc.split('##')
            command = rpc[0]

            if command == "FIND_NODE":
                pass

    def store_file(self, file_name, kbucket):    # todo: check why i wrote kbucket param
        pass

    def file_lookup(self, file_name):
        pass

    def ping(self, triple):
        pass

    def pong(self, triple):
        pass


def node_lookup_thread_func(triple):
    pass
