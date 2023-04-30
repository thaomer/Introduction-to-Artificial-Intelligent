class Action:
    def __init__(self, agent):
        self.target_vertex = agent.state.current_vertex
        self.agent = agent
        self.graph = agent.state.percept

    def __call__(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__ + " " + str(self.target_vertex)

    def move(self, pickup):
        self.graph.change_agent_location(self.agent, self.target_vertex)
        if pickup:
            self.agent.state.people_saved += self.target_vertex.people
            self.graph.total_number_of_people_evacuated += self.target_vertex.people
            self.target_vertex.people = 0
        if self.target_vertex.is_brittle:
            self.target_vertex.is_broken = True
        self.agent.state.time += 1


class TraverseAction(Action):
    def __init__(self, agent, target_vertex, pickup=True):
        super().__init__(agent)
        self.target_vertex = target_vertex
        self.pickup = pickup

    def __call__(self):
        if self.graph.agent_locations[self.agent.id_] == self.target_vertex:
            print("tried to move to myself probobly tried to give the other agent a good move\n")
        self.move(self.pickup)
        self.agent.state.current_vertex = self.target_vertex
        return False


class NoOpAction(Action):
    def __init__(self, agent, pickup=True):
        super().__init__(agent)
        self.pickup = pickup

    def __call__(self):
        self.move(self.pickup)
        return False


class TerminateAction(Action):
    def __init__(self, agent):
        super().__init__(agent)

    def __call__(self):
        return True

