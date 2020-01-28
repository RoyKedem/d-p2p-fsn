import Triple
import KBucket


class KBucketList:
    def __init__(self, my_id):
        self.bucket_list = []
        self.my_id = my_id
        for i in range(0, 8):   # replace 8 with const
            x = KBucket(i)
            self.bucket_list.append(x)

    def triple_store(self, triple):
        distance = self.my_id ^ triple.id

        for i in range(0, 8):   #replace 8 with const
            bottom_range = (2 ** i) + self.my_id
            end_range = (2 ** (i + 1)) + self.my_id
            if (bottom_range <= distance) and (distance < end_range):
                self.bucket_list[i].add_triple(triple)
                break
