import json

from classes.Node import Node
from gui.gui import *

if __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)

    port = data['port']
    kbucket = data['kbucket']

    n = Node(port)
    n.load_kbucket(kbucket)
    vp_start_gui(n)
