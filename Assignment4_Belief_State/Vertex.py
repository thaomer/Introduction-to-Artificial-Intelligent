
import random


class Vertex:
    def __init__(self, id_):
        self.id_ = id_
        self.prob = 0
        self.blocked = False

    def __lt__(self, other):
        return self.id_ < other.id_

    def __eq__(self, other):
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)

    def set_probability(self, prob):
        self.prob = prob
        rand_num = random.uniform(0, 1)
        if rand_num < self.prob:
            self.blocked = True

    def get_probability(self):
        return self.prob

    def is_blocked(self):
        return self.blocked

    def __repr__(self):
        return "V%s" % self.id_
