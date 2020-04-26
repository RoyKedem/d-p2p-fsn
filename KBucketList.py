import utility
from Triple import Triple
from KBucket import KBucket


# todo: replace all numbers
class KBucketList:
    def __init__(self, my_id):
        self.bucket_list = []
        self.my_id = my_id
        for i in range(0, 128):   # replace 128 with const
            x = KBucket(i)
            self.bucket_list.append(x)

    def triple_store(self, triple):
        kbucket_number = utility.find_appropriate_bucket(self.my_id, triple.id)
        self.bucket_list[kbucket_number].add_triple(triple)

    def load_kbucket(self, range_factor, kbucket):
        self.bucket_list[range_factor] = KBucket(range_factor, kbucket=kbucket)

    def kbucket_lookup(self, target_id):
        """
        return the kbucket that is in the range of the target id
        :param target_id:
        :return: List
        """
        kbucket_number = utility.find_appropriate_bucket(self.my_id, target_id)

        returned_bucket = self.bucket_list[kbucket_number].bucket.copy()
        print(self.bucket_list[kbucket_number].range_factor, self.bucket_list[kbucket_number].bucket)
        # replace 20 with const
        # todo: return always k length bucket
        return returned_bucket
