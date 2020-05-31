from classes.Triple import Triple


class KBucket:
    def __init__(self, range_factor, **kwargs):
        """

        :param range_factor: the lower power in the range of the specific bucket
        also the location in the kbucketlist)
        """
        self.bucket = []
        self.range_factor = range_factor

        # allow build with bucket param
        for key in kwargs:
            if key == 'kbucket':
                kbucket_arg = kwargs.get(key)
                for str in kbucket_arg:
                    str = str.split('##')
                    self.add_triple(Triple(str[1], int(str[2])))

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
