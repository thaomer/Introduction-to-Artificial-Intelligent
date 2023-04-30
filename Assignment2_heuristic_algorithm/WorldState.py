class WorldState:
    def __init__(self, percept, agent):
        self.broken_list = [vertex.is_broken for vertex in percept.G.nodes()]
        self.people_list = [vertex.people for vertex in percept.G.nodes()]
        self.location_tuple = [percept.agent_locations[0], percept.agent_locations[1]]
        self.agent_to_move = agent.id_


    def __eq__(self, other):
        return self.broken_list == other.broken_list and self.people_list == other.people_list and self.location_tuple == other.location_tuple and self.agent_to_move == other.agent_to_move

    def __repr__(self):
        return "people=%s, broken=%s location=%s agent.id=%d:\n" % (self.people_list, self.broken_list, self.location_tuple, self.agent_to_move)
