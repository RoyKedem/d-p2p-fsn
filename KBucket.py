import Triple


class KBucket:
    """

    """
    def __init__(self, range_factor):
        """

        :param range_factor: the lower power in the range of the specific bucket
        """
        self.bucket = []
        self.range_factor = range_factor

    # todo: what the hell is this
    def __getitem__(self, item):
        return self.bucket[item]

    def add_triple(self, triple_to_add):
        self.bucket.append(triple_to_add)
        # todo: when size=k remove triples doesnt response to ping

    def delete_triple(self, triple_to_delete):
        index = 0
        for trpl in self.bucket:
            if trpl.id == triple_to_delete.id:
                self.bucket.pop(index)
            index += 1
