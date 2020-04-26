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


def find_appropriate_bucket(my_id, target_id):
    dist = distance(my_id, target_id)

    for i in range(0, 128):  # replace 128 with const
        bottom_range = (2 ** i) + my_id
        end_range = (2 ** (i + 1)) + my_id
        if (bottom_range <= dist) and (dist < end_range):
            return i


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
