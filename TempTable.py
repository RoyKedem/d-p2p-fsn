from Triple import Triple
from KBucket import KBucket


class TempTable:
    def __init__(self):
        self.node_lookup_table = []

    def add_sorted_bucket(self, k_bucket, my_id):
        for triple in k_bucket.bucket:
            for x in range(0, len(self.node_lookup_table)):
                higher_then_before = triple.id ^ my_id > self.node_lookup_table[x] ^ my_id
                lower_then_next = triple.id ^ my_id < self.node_lookup_table[x+1] ^ my_id
                if higher_then_before and lower_then_next:
                    self.node_lookup_table.insert(x, triple)
