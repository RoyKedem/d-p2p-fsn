import utility
import pandas as pd
import numpy as np
import random
import hashlib


def _generate_random_ip():
    ip = str(random.randint(0, 255))
    for i in range(3):
        rand = random.randint(0, 255)
        ip += '.' + str(rand)
    return ip


def _create_triple_list():
    a = []
    for i in range(0, 20):
        final_str = ''
        ip = _generate_random_ip()
        port = random.randint(1000, 43000)
        id = utility.calc_id(ip, port)
        final_str = str(id) + '##' + ip + '##' + str(port)
        a.append(final_str)
    return a


def _create_routing_table(self_id, file_name, *args):
    """

    :param self_id: the id of the node that will use this routing table
    :param args: The args param is a list of ip's and port's that will be in the routing table in addition to the random
    triples. ip##port example - '127.0.0.1##100'
    :return: pandas DataFrame object
    """

    try:
        file = open(file_name, 'r')
    except FileNotFoundError:
        file = open(file_name, 'w')
    finally:
        file.close()

    routing_table = pd.DataFrame()
    for arg in args:
        ip = arg.split('##')[0]
        port = arg.split('##')[1]
        arg_id = utility.calc_id(ip, port)

        arg_triple_string = str(arg_id) + '##' + ip + '##' + str(port)
        kbucket = _create_triple_list()
        kbucket[0] = arg_triple_string

        distance = utility.distance(self_id, arg_id)
        for i in range(0, 128):  # replace 128 with const
            bottom_range = (2 ** i) + self_id
            end_range = (2 ** (i + 1)) + self_id
            if (bottom_range <= distance) and (distance < end_range):
                routing_table[str(i)] = kbucket
                break
    routing_table.to_csv(file_name)


def mmm():
    file_df = pd.read_csv('csv-test.csv')

    arr = _create_triple_list()
    df = pd.DataFrame()
    df['index1'] = arr
    arr = _create_triple_list()
    df['index2'] = arr
    df.to_csv('csv-test.csv')

    file = pd.read_csv('csv-test.csv')
    print(file.iloc[0:, 0])


def multiplication_table():
    df = pd.DataFrame()
    for i in range(1, 10):
        cols = []
        for j in range(1, 10):
            cols.append(j * i)
        df[str(i)] = cols
    return df


if __name__ == '__main__':
    _create_routing_table(3213212, 'try.csv', '127.0.0.1##100')
