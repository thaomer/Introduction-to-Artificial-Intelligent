class Action:
    def __init__(self, agent):
        self.target_vertex = agent.state.current_vertex
        self.agent = agent
        self.graph = agent.state.percept

    def __call__(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__

    def the_move(self, pickup):
        self.graph.change_agent_location(self.agent, self.target_vertex)
        if pickup:
            self.agent.state.people_saved += self.target_vertex.people
            self.graph.total_number_of_people_evacuated += self.target_vertex.people
            self.target_vertex.people = 0
        if self.target_vertex.is_brittle:
            self.target_vertex.is_broken = True


class TraverseAction(Action):
    def __init__(self, agent, target_vertex, pickup):
        super().__init__(agent)
        self.target_vertex = target_vertex
        self.pickup = pickup

    def __call__(self):
        if self.graph.agent_locations[self.agent] == self.target_vertex:
            raise Exception("this is is traverse action why is it moving to itself?")
        linked_vertexes = [x for x in self.graph.graph_dict[self.agent.state.current_vertex] if x[0] == self.target_vertex]
        assert len(linked_vertexes) == 1
        self.agent.state.time += linked_vertexes[0][1]
        self.the_move(self.pickup)
        return False

class NoOpAction(Action):
    def __init__(self, agent, pickup):
        super().__init__(agent)
        self.pickup = pickup

    def __call__(self):
        self.agent.state.time += 1
        self.the_move(self.pickup)
        return False

class TerminateAction(Action):
    def __init__(self, agent):
        super().__init__(agent)

    def __call__(self):
        return True
    