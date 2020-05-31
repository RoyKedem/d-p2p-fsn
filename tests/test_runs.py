import socket
import pickle
import utility
from classes.Node import Node

def test_node_thread(ip, port):
    sock = socket.socket()
    sock.connect((ip, port))
    target_id = utility.calc_id('127.0.0.1', 100)
    print(target_id)
    msg = 'FIND_NODE' + '##' + str(target_id)
    sock.send(msg.encode())
    x = sock.recv(100000)
    print(x)
    return x


def test_node(port):
    n = Node(port)
    index = int(port / 1000) - 1
    abc = 'ABCDEFGHIJ'
    print(abc[index])
    n.load_kbucket('node' + abc[index] + '.csv')


if __name__ == '__main__':
    test_node(2000)
    test_node(3000)
