import socket
import pickle
from threading import Thread
import hashlib
import random
import pandas as pd
import numpy as np

import utility
from classes.Triple import Triple
from classes.KBucket import KBucket
from classes.KBucketList import KBucketList
from classes.TempTable import *

alpha = 3


class Node:
    def __init__(self, port):
        """

        :param port: the port the node is communicate on
        """
        # port
        self.port = port

        # generate local id
        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)
        self.my_id = utility.calc_id(self.ip, self.port)

        # routing table
        self.routing_table = KBucketList(self.my_id)

        # my shared files
        # file id: file path
        self.my_shared_files = {}

        # storage
        # file name: owner_id
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
        temp_table = TempTable(target_id, x)

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

    # todo: when receives a message from other it will add it to the KBucketList
    def main_thread(self):
        """
        the main thread handle all the connections creations and RPCs
        it opens server socket
        :return:
        """
        print('setting up a server on port ' + str(self.ip) + str(self.port) + '...')
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
                self.storage[file_name] = int(owner_id)
                print(self.storage)
                handled = True

            if command == 'FILE_LOOKUP':
                file_name = rpc[1]
                if file_name in self.storage.keys():
                    client_socket.send(str(self.storage[file_name]).encode())
                else:
                    client_socket.send('not_found')
                handled = True

            if command == 'DOWNLOAD':
                file_name = rpc[1]
                file_id = utility.calc_file_id(file_name)
                print('DOWNLOAD rpc received. file name is ', file_name, '-> file id is', file_id)
                file_path = self.my_shared_files[file_id]

                BUFFER_SIZE = 1024
                f = open(file_path, 'rb')
                while True:
                    l = f.read(BUFFER_SIZE)
                    while (l):
                        client_socket.send(l)
                        # print('Sent ',repr(l))
                        l = f.read(BUFFER_SIZE)
                    if not l:
                        f.close()
                        client_socket.close()
                        handled = True
                        break

    def store_file(self, file_name, file_path):
        """

        :param file_name: file name, exa file.txt
        :param file_path: file path on this machine, exa C:/desktop/file.txt
        :return: none
        """
        # discover what is the file id
        file_id = utility.calc_file_id(file_name)
        # add the file path to my shared files dict
        self.my_shared_files[int(file_id)] = file_path
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

    def _file_lookup(self, file_name):
        """

        :param file_name: string of the file name. exa - file.txt
        :return: triple of the file holder, or an ERROR message.
        """
        # discover what is the file id
        file_id = utility.calc_file_id(file_name)
        # discover k closest nodes to the file id
        file_link_holders = self._node_lookup(file_id)  # node who may know where is the file stored
        msg = 'FILE_LOOKUP##' + file_name

        # todo: maybe add ack msg

        file_link_holders_answers = []
        for file_holder in file_link_holders:   # file location holder*
            sock = file_holder.create_socket()
            # if sock type is string there is an error (error msg returned, not sock obj)
            if type(sock) == str:
                print(sock)
            else:
                sock.send(msg.encode())
                ans = utility.recv_with_timeout(sock, 1024, 1)
                print('ans -', ans)
                if type(ans) != str:
                    ans = ans.decode()
                    file_link_holders_answers.append(ans)

        # best_answer is the file holder id if it is have been received
        best_answer = 'not_found'
        for answer in file_link_holders_answers:
            if answer != 'not_found':
                best_answer = answer

        # ans can be file holder id or str 'not_found'
        if best_answer == 'not_found':
            return 'ERROR: file doesnt exist'
        else:
            file_owner_id = int(best_answer)
            print('file owner id is', file_owner_id)
            potential_file_holders = self._node_lookup(file_owner_id)

            for triple in potential_file_holders:
                if triple.id == file_owner_id:
                    return triple
            return 'ERROR: file holder not found'

    def download(self, file_name):
        """

        :param file_name: the file name that the client is want to download
        :return: str msg of download succeed or error msg
        """
        file_holder = self._file_lookup(file_name)
        print('file holder: ', file_holder)
        if type(file_holder) == str:
            # there is an error, error msg returns
            return file_holder
        else:
            msg = 'DOWNLOAD##' + file_name
            sock = file_holder.create_socket()
            sock.send(msg.encode())
            file_data = self._recv_file(sock)
            file = open(file_name, 'w')
            file.write(file_data)
            file.close()
            return 'download succeed'

    @staticmethod
    def _recv_file(sock):
        buffer_size = 1024
        file_str = ''
        while True:
            # print('receiving file data...')
            data = sock.recv(buffer_size)
            if not data:    # if the is no data to get - all the file received
                print('file close()')
                return file_str
            # write data to a file str
            file_str += data.decode()

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
