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


def recv_with_timeout(sock, size, timeout):
    """
    socket.recv function that have a timeout
    :param sock: the socket object
    :param size: size (for the recv function)
    :param timeout: number of second for the timeout
    :return:
    """
    # set timeout of 10 seconds of no activity
    sock.settimeout(timeout)

    try:
        return sock.recv(size)
    except socket.timeout:
        return 'ERROR: timeout'
    finally:
        sock.close()

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
        temp_table = TempTable(alpha_nodes)

        # step 4
        i = 0
        alpha_nodes = []
        # find the closest triple to the target that hasn't been queried yet
        while (not temp_table.node_lookup_table[i].queried) and len(alpha_nodes) < 3:
            alpha_nodes.append(temp_table.node_lookup_table[i])
        # send the FIND_NODE RPCs
        msg = "FIND_NODE##" + target_id
        for node_connection in alpha_nodes:
            sock = node_connection.create_socket()  # socket type object
            sock.send(msg)

        # step 5
            node_connection.queried = True

        # step 6
            # answer - array that will get the return values of the threads
            answers = []
            # index - the index of the node connection in the alpha nodes list
            index = alpha_nodes.index(node_connection)
            # each cell in the alpha_nodes list holds a thread of the recv function
            alpha_nodes[index] = Thread(target=lambda a, arg1, arg2, arg3: a.append(recv_with_timeout(arg1, arg2, arg3)), args=(answers, sock, 1024, 10))
            alpha_nodes[index].start()
            alpha_nodes[index].join()

        # while loop waits until all the threads are done or timeout
        while not len(alpha_nodes) == 0:
            for thread in alpha_nodes:
                if not thread.is_alive():   # if the thread is over
                    index = alpha_nodes.index(thread)
                    if not answers[index] == "ERROR: timeout":  # and it returned with kbucket
                        # add kbuckets to the temp table
                        temp_table.add_sorted_bucket(answers[index])
                    alpha_nodes.pop(index)  #


    # todo: finish
    # todo: when receives a message from other it will add it to the KBucketList
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

    # todo: finish
    def handle_rpc(self, client_socket):
        """
        handle all client RPCs
        :param client_socket: socket object to communicate with clients
        :return:
        """
        while True:
            rpc = client_socket.recv(1024)
            rpc.decode()

            # COMMAND_NAME##var1##var2....
            rpc = rpc.split('##')
            command = rpc[0]

            if command == "FIND_NODE":
                id = command[1]
                return self.routing_table.kbucket_lookup(id)

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
