# utility.py
import hashlib
import socket


def calc_id(ip, port):
    a = ip + str(port)
    a = hashlib.md5(a.encode('latin-1'))
    id = int(a.hexdigest(), 16)
    return id


def distance(a, b):
    return int(a) ^ int(b)


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
