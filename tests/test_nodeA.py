from classes.Node import Node
import utility


def test_node_lookup():
    target_id = utility.default_id
    n = Node(1000)
    n.load_kbucket('nodeA.csv')
    x = n._node_lookup(target_id)
    print('node lookup answer:', x)
    for triple in x:
        print(utility.distance(triple.id, target_id))


def test_store_file():
    target_id = utility.default_id
    n = Node(1000)
    n.load_kbucket('nodeA.csv')
    x = n.store_file('file.txt', r'C:\Users\roykc\Documents\Projects\d-p2p-fsn\tests\file.txt')
    print('in my shared files: ', n.my_shared_files)


if __name__ == '__main__':
    test_store_file()
