class StateNode:

    def __init__(self, node, people_list, broken_list):
        self.node = node
        self.people_list = people_list.copy()
        self.broken_list = broken_list.copy()

    def get_info(self):
        return self.node, self.people_list, self.broken_list

    def __hash__(self):
        return hash((self.node, tuple(self.people_list), tuple(self.broken_list)))

    def __lt__(self, other):
        return self.node.id_ < other.node.id_

    def __eq__(self, other):
        node = self.node.id_ == other.node.id_
        people_list = self.people_list == other.people_list
        broken_list = self.broken_list == other.broken_list
        return node and people_list and broken_list

    def __repr__(self):
        return "node=%s people=%s broken=%s\n" % (self.node, self.people_list, self.broken_list,)
