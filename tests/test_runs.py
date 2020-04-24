import socket
import pickle


def test_node_thread(ip, port):
    sock = socket.socket()
    sock.connect((ip, port))
    msg = 'FIND_NODE' + '##' + str(345678765543)
    sock.send(msg.encode())
    x = sock.recv(1024)
    print(x)
    return x


if __name__ == '__main__':
    x = test_node_thread('127.0.0.1', 1000)
    print(pickle.loads(x))
