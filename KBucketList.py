from Triple import Triple
from KBucket import KBucket


# todo: replace all numbers
class KBucketList:
    def __init__(self, my_id):
        self.bucket_list = []
        self.my_id = my_id
        for i in range(0, 128):   # replace 8 with const
            x = KBucket(i)
            self.bucket_list.append(x)

    def triple_store(self, triple):
        # todo: distance func in util file
        distance = self.my_id ^ triple.id

        for i in range(0, 128):   # replace 8 with const
            bottom_range = (2 ** i) + self.my_id
            end_range = (2 ** (i + 1)) + self.my_id
            if (bottom_range <= distance) and (distance < end_range):
                self.bucket_list[i].add_triple(triple)
                break

    def kbucket_lookup(self, target_id):
        """
        return the kbucket that is in the range of the target id
        :param target_id:
        :return: kbucket object
        """
        distance = self.my_id ^ target_id

        for i in range(0, 8):  # replace 8 with const
            bottom_range = (2 ** i)
            top_range = (2 ** (i + 1))

            if (bottom_range <= distance) and (distance < top_range):
                returned_bucket = self.bucket_list[i].bucket.copy()
                # replace 20 with const
                # todo: return always k length bucket
                return returned_bucket
