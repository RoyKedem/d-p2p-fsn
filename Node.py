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

alpha = 3


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
        self.my_id = utility.calc_id(ip, self.port)

        # routing table
        self.routing_table = KBucketList(self.my_id)

        # my shared files
        self.my_shared_files = {}

        # storage
        self.storage = {}

        print('starting main thread...')
        server_thread = Thread(target=self.main_thread)
        server_thread.start()
        print('Done!')

    def _node_lookup(self, target_id):
        """
        search for a node with the kademlia algorithm
        :param target_id:
        :return: list of triple obj of the K closest nodes to the node_id param
        """
        # step 1
        # x is a kbucket object that holds the triples of the k closets node
        # todo: check if it is a pointer or not
        # todo: change name - x
        x = self.routing_table.kbucket_lookup(target_id)

        # step 2
        # choose random alpha nodes
        """alpha_nodes = []
        for i in range(0, alpha):
            # todo: choices must be different
            alpha_nodes.append(random.choice(x))
        """
        # step 3
        temp_table = TempTable(self.my_id, x)

        # step 4
        return self._node_lookup_recurse(target_id, temp_table)

    def _node_lookup_recurse(self, target_id, temp_table):
        """

        :param target_id:
        :param temp_table:
        :return:
        """
        # this var hold the list before the changes to compare it to the list after the changes
        old_id_list = temp_table.get_id_list()

        # step 4
        alpha_nodes = []
        # answers_threads - list of all the threads that holds the recv func
        answers_threads = []
        # answer - array that will get the return values of the threads
        answers = []

        # find the closest triple to the target that hasn't been queried yet
        i = 0
        while len(alpha_nodes) < alpha and i < 20:
            if not temp_table.node_lookup_table[i].queried:
                alpha_nodes.append(temp_table.node_lookup_table[i])
            i += 1
        # send the FIND_NODE RPCs
        msg = "FIND_NODE##" + str(target_id)
        for node_connection in alpha_nodes:
            sock = node_connection.create_socket()  # socket type object
            # if sock type is string there is an error (error msg returned, not sock obj)
            if type(sock) == str:
                print(sock)
                node_connection.queried = True
            else:
                print('connection ')
                sock.send(msg.encode())
        # step 5
                node_connection.queried = True

        # step 6

            # each cell in the answers_threads list holds a thread of the recv function
            answers_threads.append(Thread(
                target=lambda a, arg1, arg2, arg3: a.append(utility.recv_with_timeout(arg1, arg2, arg3)),
                args=(answers, sock, 10000, 1)))
            answers_threads[-1].start()

        # while loop waits until all the threads are done or timeout
        while len(answers_threads) != 0:
            for thread in answers_threads:
                if not thread.is_alive():  # if the thread is over
                    index = answers_threads.index(thread)
                    if answers[index][:5] != "ERROR":  # and it returned with kbucket
                        # add kbuckets to the temp table
                        temp_table.add_sorted_bucket(pickle.loads(answers[index]))
                    answers_threads.pop(index)  # remove the thread from the waiting list
        # step 7
        # compare the id list
        if old_id_list == temp_table.get_id_list() and temp_table.is_all_queried():
            return temp_table.get_regular_bucket()
        else:
            return self._node_lookup_recurse(target_id, temp_table)

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
            a = Thread(target=self._handle_rpc, args=(client_socket,))
            a.start()

    # todo: finish
    def _handle_rpc(self, client_socket):
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

            if command == 'FIND_NODE':
                target_id = int(rpc[1])
                k = self.routing_table.kbucket_lookup(target_id)
                pickled_msg = pickle.dumps(k)
                client_socket.send(pickled_msg)
                handled = True

            if command == 'STORE_FILE':
                file_name = rpc[1]
                owner_id = rpc[2]
                self.storage[file_name] = owner_id
                handled = True

    def store_file(self, file_name, file_path):
        # discover what is the file id
        file_id = hashlib.md5(file_name)
        # add the file path to my shared files dict
        self.my_shared_files[file_id] = file_path
        # discover k closest nodes to the file id
        file_link_holders = self._node_lookup(file_id)

        msg = 'STORE_FILE##' + file_name + '##' + str(self.my_id)

        # todo: maybe add ack msg
        for file_holder in file_link_holders:
            sock = file_holder.create_socket()
            # if sock type is string there is an error (error msg returned, not sock obj)
            if type(sock) == str:
                print(sock)
            else:
                print('connection ')
                sock.send(msg.encode())

    def file_lookup(self, file_name):
        pass

    def ping(self, triple):
        pass

    def pong(self, triple):
        pass

    def load_kbucket(self, file_path):
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
