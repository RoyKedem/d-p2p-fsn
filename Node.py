import socket
import pickle
from threading import Thread
import hashlib
import random
import pandas as pd
import numpy as np

import utility
from Triple import Triple
from KBucket import KBucket
from KBucketList import KBucketList
from TempTable import *
# todo: create config file

alpha = 1


# todo: optional id param
class Node:
    def __init__(self, port):
        """

        :param port: the port the node is communicate on
        """
        # port
        self.port = port

        # generate local id
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

        print('starting main thread...')
        server_thread = Thread(target=self.main_thread)
        server_thread.start()
        print('Done!')

    # todo: parallelism
    def node_lookup(self, target_id):
        """
        search for a node with the kademlia algorithm
        :param target_id:
        :return: KBucket obj of the K closest nodes to the node_id param
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
        self.node_lookup_recurse(target_id, temp_table)

    def node_lookup_recurse(self, target_id, temp_table):

        # this var hold the list before the changes to compare it to the list after the changes
        old_id_list = temp_table.get_id_list()

        # step 4
        i = 0
        alpha_nodes = []
        # answers_threads - list of all the threads that holds the recv func
        answers_threads = []
        # answer - array that will get the return values of the threads
        answers = []

        # find the closest triple to the target that hasn't been queried yet
        while (not temp_table.node_lookup_table[i].queried) and len(alpha_nodes) < 3:
            alpha_nodes.append(temp_table.node_lookup_table[i])
            i += 1
        # send the FIND_NODE RPCs
        msg = "FIND_NODE##" + str(target_id)
        for node_connection in alpha_nodes:
            sock = node_connection.create_socket()  # socket type object
            sock.send(msg)
        # step 5
            node_connection.queried = True

        # step 6

            # each cell in the answers_threads list holds a thread of the recv function
            answers_threads.append(Thread(
                target=lambda a, arg1, arg2, arg3: a.append(utility.recv_with_timeout(arg1, arg2, arg3)),
                args=(answers, sock, 1024, 10)))
            answers_threads[-1].start()
            answers_threads[-1].join()

        # while loop waits until all the threads are done or timeout
        while len(answers_threads) != 0:
            for thread in answers_threads:
                if not thread.is_alive():  # if the thread is over
                    index = answers_threads.index(thread)
                    if answers[index] != "ERROR: timeout":  # and it returned with kbucket
                        # add kbuckets to the temp table
                        temp_table.add_sorted_bucket(answers[index])
                    answers_threads.pop(index)  # remove the thread from the waiting list

        # step 7
        # compare the id list
        if old_id_list == temp_table.get_id_list() and temp_table.is_all_queried():
            return temp_table
        else:
            self.node_lookup_recurse(target_id, temp_table)

    # todo: finish
    # todo: when receives a message from other it will add it to the KBucketList
    def main_thread(self):
        """
        the main thread handle all the connections creations and RPCs
        it opens server socket
        :return:
        """
        print('setting up a server on port ' + str(self.port) + '...')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', self.port))

        server_socket.listen(5)     # todo: replace with const
        print('server is ready')
        clients = []    # holds all the clients sockets
        while True:
            (client_socket, client_address) = server_socket.accept()
            clients.append(client_socket)
            a = Thread(target=self.handle_rpc, args=(client_socket,))
            a.start()

    # todo: finish
    def handle_rpc(self, client_socket):
        """
        handle all client RPCs
        :param client_socket: socket object to communicate with clients
        :return:
        """
        handled = False
        while not handled:
            rpc = client_socket.recv(1024)
            rpc = rpc.decode()

            # COMMAND_NAME##var1##var2....
            rpc = rpc.split('##')
            command = rpc[0]

            if command == "FIND_NODE":
                target_id = int(rpc[1])
                k = self.routing_table.kbucket_lookup(target_id)
                pickled_msg = pickle.dumps(k)
                client_socket.send(pickled_msg)
                handled = True

    def store_file(self, file_name, kbucket):    # todo: check why i wrote kbucket param
        pass

    def file_lookup(self, file_name):
        pass

    def ping(self, triple):
        pass

    def pong(self, triple):
        pass

    def _load_kbucket(self, file_path):
        """
        func loads to the node routing table a full or part of k-bucket csv file, for developer checks
        :param file_path: the file path of the csv file
        :return:
        """
        df = pd.read_csv(file_path)
        
        for bucket_index in df:
            if bucket_index != 'Unnamed: 0':
                kbucket = df[bucket_index].to_list()
                self.routing_table.load_kbucket(int(bucket_index), kbucket)
