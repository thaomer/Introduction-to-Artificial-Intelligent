class StateNode:

    def __init__(self, people_list, broken_list, scores_tuple, location_tuple, maximizing_player):
        self.people_list = people_list.copy()
        self.broken_list = broken_list.copy()
        self.scores_tuple = scores_tuple
        self.location_tuple = location_tuple
        self.maximizing_player = maximizing_player

    def get_score_minimax(self):
        return self.scores_tuple[0]-self.scores_tuple[1]

    def get_score_semi(self):
        return list((self.scores_tuple[0], self.scores_tuple[1]))

    def get_score_fully(self):
        return self.scores_tuple[0] + self.scores_tuple[1]

    def set_parent(self, other):
        self.parent = other

    def get_info(self):
        return self.people_list, self.broken_list, self.location_tuple, self.scores_tuple

    def __hash__(self):
        return hash((tuple(self.people_list), tuple(self.broken_list), tuple(self.location_tuple), self.maximizing_player))

    # def __lt__(self, other):
    #     return self.node.id_ < other.node.id_

    def __eq__(self, other):
        return self.people_list == other.people_list and self.broken_list == other.broken_list and self.location_tuple == other.location_tuple and self.maximizing_player == other.maximizing_player

    def __repr__(self):
        return "people=%s, broken=%s location=%s, scores=%s, maximizing=%s\n" % (self.people_list, self.broken_list,
                                                                  self.location_tuple, self.scores_tuple, self.maximizing_player)
