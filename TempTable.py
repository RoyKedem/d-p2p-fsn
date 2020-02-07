from Triple import Triple
from KBucket import KBucket
# todo: change name!!!!!!!!!


class Triple2(Triple):
    def __init__(self, triple, searched=False):
        Triple.__init__(self, triple.ip, triple.port)
        self.searched = searched
        self.id = triple.id


class TempTable:
    def __init__(self):
        self.node_lookup_table = []

    def add_sorted_bucket(self, k_bucket, my_id):
        """
        add a new bucket to the TempTable. it adds the triples in order by the distance from my_id
        :param k_bucket: the bucket you want to add
        :param my_id: the id of this node (to calc the distance from each triple)
        :return:
        """
        for triple in k_bucket:
            self.node_lookup_table.append(Triple2(triple))

        self.node_lookup_table.sort(key=lambda elem: elem.id ^ my_id)


if __name__ == '__main__':
    my_id = 1
    x = KBucket(2)
    for i in range(40, 50):
        x.add_triple(Triple('127.0.01', i))

   # for triple in x.bucket:
        # print("before - " + str(triple.id ^ my_id))

    print("break")

    t = TempTable()
    t.add_sorted_bucket(x, my_id)
    print(t.node_lookup_table)

    for triple in t.node_lookup_table:
        print("after - " + str(int((triple.id ^ my_id) / 10000000000000000000000000000000)))

