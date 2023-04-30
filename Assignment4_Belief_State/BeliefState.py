class BeliefState:
    def __init__(self, vertex, observation):
        self.vertex = vertex
        self.observation = observation

    def __eq__(self, other):
        return self.vertex == other.vertex and self.observation == other.observation

    def __repr__(self):
        return "curr_vertex=%s, observation=%s" % (self.vertex, self.observation)

    def __hash__(self):
        return hash((tuple(sorted(self.observation.items())), self.vertex))
