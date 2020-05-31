import utility
from classes.Triple import Triple
from classes.KBucket import KBucket


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
        :return: List of Triples
        """
        kbucket_number = utility.find_appropriate_bucket(self.my_id, target_id)
        print('preforming kbucket lookup target id: ', target_id, '-> kbucket ', kbucket_number)

        returned_bucket = self.bucket_list[kbucket_number].bucket.copy()
        numbers = []
        for i in range(0, 128):
            numbers.append(i)

        before_kbucket_number = numbers[:kbucket_number]
        after_kbucket_number = numbers[:kbucket_number:-1]

        search_order = []
        for i in range(0, 128):
            if i % 2 == 0:
                if before_kbucket_number:
                    search_order.append(before_kbucket_number.pop(-1))
            else:
                if after_kbucket_number:
                    search_order.append(after_kbucket_number.pop(-1))
        for i in search_order:
            returned_bucket.extend(self.bucket_list[i].bucket.copy())
            if len(returned_bucket) > 20:
                returned_bucket = returned_bucket[:20]
                break

        print(self.bucket_list[kbucket_number].range_factor, self.bucket_list[kbucket_number].bucket)
        # replace 20 with const
        return returned_bucket
