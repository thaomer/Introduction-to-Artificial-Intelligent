from State import State
from StateNode import StateNode
from action import NoOpAction, TraverseAction, TerminateAction


def generate_state(state, agent, other_agent):
    people_list = [vertex.people for vertex in state.percept.G.nodes()]
    broken_list = [vertex.is_broken for vertex in state.percept.G.nodes()]
    scores_tuple = [agent.state.people_saved, other_agent.state.people_saved]
    location_tuple = [state.percept.agent_locations[0], state.percept.agent_locations[1]]
    return StateNode(people_list, broken_list, scores_tuple, location_tuple, True)


def successorsmaker(agent, statenode, percept, is_other_agent):
    successorslist = []
    neighbors = [node for node in percept.get_neighbors(statenode.location_tuple[agent.id_]) if not statenode.broken_list[node.id_]]
    neighbors.append(statenode.location_tuple[agent.id_])
    for neighbor in neighbors:
        people_list = statenode.people_list.copy()
        broken_list = statenode.broken_list.copy()
        location_tuple = statenode.location_tuple.copy()
        scores_tuple = statenode.scores_tuple.copy()
        if neighbor.is_brittle:
            broken_list[neighbor.id_] = True
        if not is_other_agent:
            scores_tuple[0] += people_list[neighbor.id_]
        else:
            scores_tuple[1] += people_list[neighbor.id_]
        people_list[neighbor.id_] = 0
        location_tuple[agent.id_] = neighbor
        successorslist.append([StateNode(people_list, broken_list, scores_tuple,location_tuple,is_other_agent), TraverseAction(agent, neighbor)])
    return successorslist

def minimax(state_node,
            agent,
            other_agent,
            percept,
            score_class,
            depth,
            alpha,
            beta,
            maximizing_player,
            state_node_list):
    if state_node in state_node_list or all([people == 0 for people in state_node.people_list]) or depth == 0:
        return score_class(state_node.scores_tuple[0], state_node.scores_tuple[1]), None
    state_node_list = state_node_list.copy()
    state_node_list.append(state_node)
    if maximizing_player:
        max_eval = score_class(-10000, 0)
        max_action = None
        successors = successorsmaker(agent, state_node, percept, False)
        for s, a in successors:
            # space = " "
            # print(space * (15 - depth), "maximizing: depth=%s currently in node %s checking action %s" % (depth, state_node.location_tuple[1], a))
            s_eval, _ = minimax(s, agent, other_agent, percept, score_class, depth - 1, alpha, beta, False, state_node_list)
            # print(space * (15 - depth), "maximizing: depth=%s currently in node %s got score %s" % (depth, state_node.location_tuple[1],s_eval))
            if s_eval > max_eval:
                # print(space * (15 - depth),  "maximizing: depth=%s currently in node %s found better action %s" % (depth, state_node.location_tuple[1], a))
                max_eval = s_eval
                max_action = a
            if s_eval > alpha:
                alpha = s_eval
            if not (beta > alpha):
                # print(space * (15 - depth), "maximizing: breaking")
                break
        return max_eval, max_action
    else:
        min_eval = score_class(10000, 0)
        successors = successorsmaker(other_agent, state_node, percept, True)
        for s, a in successors:
            # space = " "
            # print(space * (15 - depth), "not maximizing: depth=%s currently in node %s checking action %s" % (depth, state_node.location_tuple[0], a))
            s_eval, _ = minimax(s, agent, other_agent, percept, score_class, depth - 1, alpha, beta, True, state_node_list)
            # print(space * (15 - depth), "not maximizing: depth=%s currently in node %s got score %s" % (depth, state_node.location_tuple[0], s_eval))
            min_eval = min(min_eval, s_eval)
            # print(space * (15 - depth), "not maximizing: depth=%s currently in node %s min value is %s" % (depth, state_node.location_tuple[0], min_eval))
            if beta > s_eval:
                beta = s_eval
            if not (beta > alpha):
                # print(space * (15 - depth), "not maximizing: breaking")
                break
        return min_eval, None


def maxmax(state_node,
            agent,
            other_agent,
            percept,
            score_class,
            depth,
            maximizing_player,
            state_node_list):
    if state_node in state_node_list or all([people == 0 for people in state_node.people_list]) or depth == 0:
        return score_class(state_node.scores_tuple[0], state_node.scores_tuple[1]), None

    state_node_list = state_node_list.copy()
    state_node_list.append(state_node)
    max_eval = score_class(-10000, 0)
    max_action = None
    successors = successorsmaker(agent if maximizing_player else other_agent, state_node, percept, not maximizing_player)
    for s, a in successors:
        # space = " "
        # print(space * (15 - depth), "maximizing: depth=%s currently in node %s checking action %s" % (depth, state_node.location_tuple[1], a))
        s_eval, _ = maxmax(s, agent, other_agent, percept, score_class, depth - 1, not maximizing_player, state_node_list)
        # print(space * (15 - depth), "maximizing: depth=%s currently in node %s got score %s" % (depth, state_node.location_tuple[1],s_eval))
        if s_eval > max_eval:
            # print(space * (15 - depth),  "maximizing: depth=%s currently in node %s found better action %s" % (depth, state_node.location_tuple[1], a))
            max_eval = s_eval
            max_action = a
    return max_eval, max_action

class Agent:
    def __init__(self, id_):
        self.seq = []
        self.state = State()
        self.id_ = id_

    def update_state(self, state, percept):
        self.state.percept = percept
        self.state.current_vertex = percept.agent_locations[self.id_]
        return state

    def search(self):
        raise NotImplementedError

    def remainder(self, seq, state):
        if len(seq) == 0:
            return []
        if seq[0].target_vertex.is_broken and type(seq[0]) == TraverseAction:
            return []
        else:
            return seq[1:]

    def recommendation(self, seq, state):
        if len(seq) == 0:
            return NoOpAction(self)
        action = seq[0]
        if type(action) == TraverseAction and action.target_vertex.is_broken:
            return NoOpAction(self)
        return action

    def __call__(self, percept):
        self.state = self.update_state(self.state, percept)
        if len(self.seq) == 0:
            self.seq = self.search()
        action = self.recommendation(self.seq, self.state)
        self.seq = self.remainder(self.seq, self.state)
        return action


class Score:
    def __init__(self, my_score, other_score):
        self.my_score = my_score
        self.other_score = other_score

    def __gt__(self, other):
        raise NotImplementedError

    def __repr__(self):
        return "<%s, %s>" % (self.my_score, self.other_score)


class ZeroSumScore(Score):
    def get_score(self):
        return self.my_score - self.other_score

    def __gt__(self, other):
        return self.get_score() > other.get_score()


class SemiCoopScore(Score):
    def __gt__(self, other):
        if self.my_score > other.my_score:
            return True
        elif self.my_score == other.my_score:
            return self.other_score > other.other_score
        else:
            return False

class FullCoopScore(Score):
    def get_score(self):
        return self.my_score + self.other_score

    def __gt__(self, other):
        return self.get_score() > other.get_score()

class AdversarialAgent(Agent):
    def __init__(self, id_, d):
        super().__init__(id_)
        self.d = d

    def search(self):
        agent = self
        if self.id_ == 0:
            other_agent = self.state.percept.agents[1]
        else:
            other_agent = self.state.percept.agents[0]
        state_node = generate_state(self.state, agent, other_agent)
        alpha = ZeroSumScore(-10000, 0)
        beta = ZeroSumScore(10000, 0)
        _, action = minimax(state_node, agent, other_agent, self.state.percept, ZeroSumScore, self.d, alpha, beta, True, [])
        return [action]

class SemiCooperativeAgent(Agent):
    def __init__(self, id_, d=1):
        super().__init__(id_)
        self.d = d

    def search(self):
        agent = self
        if self.id_ == 0:
            other_agent = self.state.percept.agents[1]
        else:
            other_agent = self.state.percept.agents[0]

        state_node = generate_state(self.state, agent, other_agent)
        alpha = SemiCoopScore(-10000, 0)
        beta = SemiCoopScore(10000, 0)
        _, action = minimax(state_node, agent, other_agent, self.state.percept, SemiCoopScore, self.d, alpha, beta, True, [])
        return [action]


class FullyCooperativeAgent(Agent):
    def __init__(self, id_, d):
        super().__init__(id_)
        self.d = d

    def search(self):
        agent = self
        if self.id_ == 0:
            other_agent = self.state.percept.agents[1]
        else:
            other_agent = self.state.percept.agents[0]

        state_node = generate_state(self.state, agent, other_agent)
        _, action = maxmax(state_node, agent, other_agent, self.state.percept, FullCoopScore, self.d, True, [])
        return [action]
