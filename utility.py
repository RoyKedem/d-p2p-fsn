# utility.py
import hashlib
import socket

default_id = 10000000000000000000000000000000000000


def calc_id(ip, port):
    exceptions = {100: 10000000000000000000000000000000000000}
    for i in range(1000, 10000, 1000):
        exceptions[i] = 10000000000000000000000000000000000000 + i * 10000
    if port in exceptions.keys():
        return exceptions[port]
    a = ip + str(port)
    a = hashlib.md5(a.encode('latin-1'))
    id = int(a.hexdigest(), 16)
    return id


def calc_file_id(file_name):
    if file_name == 'file.txt':
        return 10000000000000000000000000000030000000
    else:
        a = hashlib.md5(file_name.encode('latin-1'))
        file_id = int(a.hexdigest(), 16)
        return file_id


def distance(a, b):
    return int(a) ^ int(b)


def find_appropriate_bucket(my_id, target_id):
    dist = distance(my_id, target_id)
    if dist == 0:
        return 1

    for i in range(0, 128):  # replace 128 with const
        bottom_range = (2 ** i)
        end_range = (2 ** (i + 1))

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
    if type(sock) == str:
        return 'ERROR: timeout'
    sock.settimeout(timeout)

    try:
        return sock.recv(size)
    except socket.timeout:
        return 'ERROR: timeout'
    finally:
        sock.close()
