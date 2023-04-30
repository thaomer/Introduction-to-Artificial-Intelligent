import sys
import networkx as nx
from queue import PriorityQueue
from State import State
from StateNode import StateNode
from action import NoOpAction, TraverseAction, TerminateAction


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = [node for node in graph.vertices if not node.is_broken or node is start_node]
    shortest_path = {}
    previous_nodes = {}
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0

    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        neighbors = graph.graph_dict[current_min_node]
        for neighbor in neighbors:
            if not neighbor[0].is_broken:
                tentative_value = shortest_path[current_min_node] + neighbor[1]
                if tentative_value < shortest_path[neighbor[0]]:
                    shortest_path[neighbor[0]] = tentative_value
                    previous_nodes[neighbor[0]] = current_min_node

        unvisited_nodes.remove(current_min_node)
    return previous_nodes, shortest_path


def new_dijkstra_algorithm(graph, start_node, broken_list):
    unvisited_nodes = [node for node in graph.vertices]
    shortest_path = {}
    previous_nodes = {}
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        neighbors = graph.graph_dict[current_min_node]
        for neighbor in neighbors:
            if not broken_list[neighbor[0].id_]:
                tentative_value = shortest_path[current_min_node] + neighbor[1]
                if tentative_value < shortest_path[neighbor[0]]:
                    shortest_path[neighbor[0]] = tentative_value
                    previous_nodes[neighbor[0]] = current_min_node

        unvisited_nodes.remove(current_min_node)
    return previous_nodes, shortest_path


def heuristic(graph, state_node):
    G = nx.Graph()
    starting_vertex, people_list, broken_list = state_node.get_info()
    important_nodes = [node for node in graph.vertices if people_list[node.id_]]
    _, weight = new_dijkstra_algorithm(graph, starting_vertex, broken_list)
    for node in important_nodes: #we do this only for starting node here because if it is broken they cant go to it
        if weight[node] == sys.maxsize:
            return sys.maxsize
        if weight[node] != 0:
            G.add_edge(starting_vertex, node, weight=weight[node])
    for current_vertex in important_nodes:
        _, weight = new_dijkstra_algorithm(graph, current_vertex, broken_list)
        for node in important_nodes:
            if weight[node] == sys.maxsize:
                return sys.maxsize
            if weight[node] != 0:
                G.add_edge(current_vertex, node, weight=weight[node])
    mst = nx.minimum_spanning_tree(G)
    return mst.size(weight="weight")


def aStar(start_node, graph, limit):
    start_people_list = [vertex.people for vertex in graph.vertices]
    start_broken_list = [vertex.is_broken for vertex in graph.vertices]
    start_StateNode = StateNode(start_node, start_people_list, start_broken_list)
    pq = PriorityQueue()
    closed_list = set([])
    pq.put((0, start_StateNode))
    g = {start_StateNode: 0}
    parents = {start_StateNode: start_StateNode}
    counter = 0
    while pq.queue and counter != 10000:
        v = pq.get()[1]
        current_vertex, people_list, broken_list = v.get_info()
        if counter == limit or people_list.count(0) == len(people_list):
            reconst_path = []

            while parents[v] != v:
                reconst_path.append(v)
                v = parents[v]
            reconst_path.reverse()
            return reconst_path, counter

        for (target_vertex, weight) in graph.graph_dict[current_vertex]:
            if broken_list[target_vertex.id_]:
                continue
            target_people_list = people_list.copy() # make the neighbor state node
            target_broken_list = broken_list.copy()
            if target_people_list[target_vertex.id_] != 0:
                target_people_list[target_vertex.id_] = 0

            if target_vertex.is_brittle:
                target_broken_list[target_vertex.id_] = True
            u = StateNode(target_vertex, target_people_list, target_broken_list)
            h = heuristic(graph, u)
            if h == sys.maxsize:  # this also checks if the goal state is achievable
                continue  # no possible way to achive goal from this statenode
            if u not in [item[1] for item in pq.queue] and u not in closed_list:
                parents[u] = v
                g[u] = g[v] + weight
                f = g[u] + h
                pq.put((f, u))

            else:
                if g[u] > g[v] + weight:
                    g[u] = g[v] + weight
                    parents[u] = v

                    if u in closed_list:
                        closed_list.remove(u)
                        parents[u] = v
                        g[u] = g[v] + weight
                        pq.put((g[u] + h, u))
        closed_list.add(v)
    counter += 1
    if counter == 10000:
        print("AStar Failed")
    return [], counter


class Agent:
    def __init__(self, id_):
        self.seq = []
        self.state = State()
        self.id_ = id_

    def update_state(self, state, percept):
        self.state.percept = percept
        self.state.current_vertex = percept.agent_locations[self]
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
            return TerminateAction(self)
        action = seq[0]
        if type(action) == TraverseAction and action.target_vertex.is_broken:
            return NoOpAction(self, False)
        return action

    def __call__(self, percept):
        self.state = self.update_state(self.state, percept)
        if len(self.seq) == 0:
            self.seq = self.search()
        action = self.recommendation(self.seq, self.state)
        self.seq = self.remainder(self.seq, self.state)
        return action


class HumanAgent(Agent):
    def __init__(self, id_):
        super().__init__(id_)

    def search(self):
        while True:
            user_input = input("Agent%d: please choose destination vertex(-1 for terminate):\n" % self.id_)
            target_vertex_id = int(user_input)
            if target_vertex_id >= self.state.percept.num_of_vertices:
                print("illegal vertex!\n")
                continue
            if target_vertex_id == -1:
                return [TerminateAction(self)]
            linked_vertexes_id = map(lambda x: x[0].id_, self.state.percept.graph_dict[
                self.state.percept.vertices[self.state.current_vertex.id_]])
            if target_vertex_id not in linked_vertexes_id:
                print("cannot go to {} from {}\n".format(target_vertex_id, self.state.current_vertex.id_))
                continue
            return [TraverseAction(self, self.state.percept.vertices[target_vertex_id], True)]


class StupidGreedyAgent(Agent):
    def __init__(self, id_):
        super().__init__(id_)

    def search(self):
        min_score = sys.maxsize
        target_vertex = None
        path_dict, dist_dict = dijkstra_algorithm(self.state.percept, self.state.current_vertex)
        for vertex, score in dist_dict.items():
            if vertex.people and score:
                if score < min_score:  # or ((score == min_score) and (vertex.id_ < target_vertex.id_)):
                    min_score = score
                    target_vertex = vertex
        if target_vertex is None:
            return [TerminateAction(self)]
        seq = []
        next_vertex = target_vertex
        while next_vertex != self.state.current_vertex:
            seq.insert(0, TraverseAction(self, next_vertex, True))
            next_vertex = path_dict[next_vertex]
        return seq


class SaboteurAgent(Agent):
    def __init__(self, id_):
        super().__init__(id_)

    def search(self):
        min_score = sys.maxsize
        target_vertex = None
        path_dict, dist_dict = dijkstra_algorithm(self.state.percept, self.state.current_vertex)
        for vertex, score in dist_dict.items():
            if vertex.is_brittle and score:
                if score < min_score:  # or ((score == min_score) and (vertex.id_ < target_vertex.id_)):
                    min_score = score
                    target_vertex = vertex
        if target_vertex is None:
            return [TerminateAction(self)]
        seq = []
        next_vertex = target_vertex
        while next_vertex != self.state.current_vertex:
            seq.insert(0, TraverseAction(self, next_vertex, False))
            next_vertex = path_dict[next_vertex]
        return seq


class AStarAgent(Agent):
    def __init__(self, id_, t=0):
        super().__init__(id_)
        self.t = t

    def search(self):
        temp, n = aStar(self.state.current_vertex, self.state.percept, -1)
        seq = list(map(lambda x: TraverseAction(self, x.node, True), temp))
        self.state.time += n * self.t
        return seq


class RealTimeAStarAgent(Agent):
    def __init__(self, id_, t=0, l=10):
        super().__init__(id_)
        self.t = t
        self.l = l

    def search(self):
        temp, n = aStar(self.state.current_vertex, self.state.percept, self.l)
        seq = list(map(lambda x: TraverseAction(self, x.node, True), temp))
        self.state.time += n * self.t
        return seq


class GreedyAStarAgent(Agent):
    def __init__(self, id_, t=0, l=1):
        super().__init__(id_)
        self.t = t
        self.l = l

    def search(self):
        temp, n = aStar(self.state.current_vertex, self.state.percept, self.l)
        seq = list(map(lambda x: TraverseAction(self, x.node, True), temp))
        self.state.time += n * self.t
        return seq
