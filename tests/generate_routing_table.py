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
    # todo: fix more then one arg problem
    for arg in args:
        ip = arg.split('##')[0]
        port = int(arg.split('##')[1])
        arg_id = utility.calc_id(ip, port)

        arg_triple_string = str(arg_id) + '##' + ip + '##' + str(port)
        kbucket = _create_triple_list()
        kbucket[args.index(arg)] = arg_triple_string

        kbucket_number = utility.find_appropriate_bucket(self_id, arg_id)
        print(kbucket_number)
        routing_table[str(kbucket_number)] = kbucket

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


if __name__ == '__main__':
    ip = '192.168.56.1'
    _create_routing_table(utility.calc_id(ip, 1000), 'nodeA.csv', '192.168.56.1##2000')
    _create_routing_table(utility.calc_id(ip, 2000), 'nodeB.csv', '192.168.56.1##3000')
    _create_routing_table(utility.calc_id(ip, 3000), 'nodeC.csv', '192.168.7.156##100', '192.168.56.1##1000')
    _create_routing_table(utility.calc_id(ip, 3999), 'nodeD.csv', '192.168.56.1##3000')
