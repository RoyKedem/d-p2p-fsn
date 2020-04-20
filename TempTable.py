from Triple import Triple
from KBucket import KBucket
# todo: change name!!!!!!!!!


class TempTableTripleObject(Triple):
    """
    the object that is stored in the temp table
    the object is like the triple object but with queried attribute
    """
    def __init__(self, triple, searched=False):
        Triple.__init__(self, triple.ip, triple.port)
        self.queried = searched
        self.id = triple.id


class TempTable:
    def __init__(self, alpha_nodes=""):
        self.node_lookup_table = []
        if alpha_nodes != "":
            for trpl in alpha_nodes:
                self.node_lookup_table.append(TempTableTripleObject(trpl))

    def add_sorted_bucket(self, k_bucket, my_id):
        """
        add a new bucket to the TempTable. it adds the triples in order by the distance from my_id
        :param k_bucket: the bucket you want to add
        :param my_id: the id of this node (to calc the distance from each triple)
        :return:
        """
        for triple in k_bucket:
            self.node_lookup_table.append(TempTableTripleObject(triple))

        self.node_lookup_table.sort(key=lambda elem: elem.id ^ my_id)

        # remove duplicates
        seen_ids = []
        for triple in self.node_lookup_table:
            seen_ids.append(triple.id)
            if seen_ids.count(triple.id) == 2:
                self.node_lookup_table.remove(triple)
                seen_ids.remove(triple.id)

        # length of the node lookup table is max 20
        if len(self.node_lookup_table) > 20:
            for i in range(20, len(self.node_lookup_table)):
                self.node_lookup_table.pop(i)

    def get_id_list(self):
        """
        :return: a list of the id's of the k first nodes
        """
        return_list = []    # the list tht returns from the func, holds the id's of the temp table triples

        for triple in self.node_lookup_table:
            return_list.append(triple.id)

        return return_list

    def get_regular_bucket(self):
        """

        :return: a kbucket that holds Triple instead Triple 2
        """

    def is_all_queried(self):
        for triple in self.node_lookup_table:
            if not triple.queried: return False
        return True
    
    def get_triple_by_id(self):
        pass

