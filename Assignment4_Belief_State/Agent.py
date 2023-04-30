from State import State
from action import NoOpAction, TraverseAction, TerminateAction
from BeliefState import BeliefState

class Agent:
    def __init__(self, id_):
        self.seq = []
        self.state = State()
        self.id_ = id_

    def update_state(self, state, percept):
        self.state.percept = percept
        self.state.current_vertex = percept.agent_locations[self.id_]
        # update observation according to current state
        blockable_neighbors = [vertex for vertex in percept.get_neighbors(self.state.current_vertex) if vertex.get_probability()]
        for vertex in blockable_neighbors:
            self.state.observation[vertex] = vertex.is_blocked()
        return state

    def search(self):
        b_state = BeliefState(self.state.current_vertex, self.state.observation)
        print("search: current_belief_state[%s]" % b_state)
        target_vertex = self.state.percept.policies[b_state]
        if target_vertex is None:
            return [TerminateAction(self)]
        return [TraverseAction(self, target_vertex, False)]

    def remainder(self, seq, state):
        if len(seq) == 0:
            return []
        return seq[1:]

    def recommendation(self, seq, state):
        if len(seq) == 0:
            return NoOpAction(self)
        action = seq[0]
        return action

    def __call__(self, percept):
        self.state = self.update_state(self.state, percept)
        if len(self.seq) == 0:
            self.seq = self.search()
        action = self.recommendation(self.seq, self.state)
        self.seq = self.remainder(self.seq, self.state)
        return action
