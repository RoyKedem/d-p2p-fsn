from classes.Node import Node


def download(file_name):
    n = Node(3999)
    n.load_kbucket('nodeD.csv')
    n.download(file_name)


if __name__ == '__main__':
    download('file.txt')
