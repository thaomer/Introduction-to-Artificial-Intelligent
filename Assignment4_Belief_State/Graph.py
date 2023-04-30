from Vertex import Vertex
import networkx as nx


def parse_config(config_):
    G = nx.Graph()
    start_vertex = None
    target_vertex = None
    for line in config_.split('\n'):
        if len(line) > 0:
            first_letter = line[1]
            if first_letter == 'V':
                num_vertex = int(line[3:])
                for i in range(num_vertex):
                    G.add_node(Vertex(i))
            elif first_letter == 'E':
                info_on_vertex = line.split()[1:]
                assert len(info_on_vertex) == 3
                source = int(info_on_vertex[0]) - 1
                source_to_put = None
                target = int(info_on_vertex[1]) - 1
                target_to_put = None
                weight = int(info_on_vertex[2][1:])
                for node in list(G.nodes):
                    if (type(node)) != type(1):
                        if node.id_ == target:
                            target_to_put = node
                        elif node.id_ == source:
                            source_to_put = node
                assert source_to_put
                assert target_to_put
                G.add_edge(source_to_put, target_to_put, weight=weight)
            elif first_letter == 'B':
                info_on_vertex = line.split()[1:]
                assert len(info_on_vertex) == 2
                vertex_id = int(info_on_vertex[0]) - 1
                prob = float(info_on_vertex[1])
                assert (prob >= 0.0) and (prob <= 1.0)
                found_vertex = False
                for node in list(G.nodes):
                    if (type(node)) != type(1):
                        if node.id_ == vertex_id:
                            node.set_probability(prob)
                            found_vertex = True
                            break
                assert found_vertex
            elif first_letter == 'S':
                line_info = line.split()
                assert line_info[0][1:] == "Start"
                vertex_id = int(line_info[1]) - 1
                for node in list(G.nodes):
                    if (type(node)) != type(1):
                        if node.id_ == vertex_id:
                            start_vertex = node
                            break
            elif first_letter == 'T':
                line_info = line.split()
                assert line_info[0][1:] == "Target"
                vertex_id = int(line_info[1]) - 1
                for node in list(G.nodes):
                    if (type(node)) != type(1):
                        if node.id_ == vertex_id:
                            target_vertex = node
                            break
    assert start_vertex
    assert target_vertex

    start_vertex.prob = 0
    start_vertex.blocked = False
    target_vertex.prob = 0
    target_vertex.blocked = False

    # add edge between start and target with very high weight
    neighbors_list = G.neighbors(start_vertex)
    if target_vertex not in neighbors_list:
        G.add_edge(start_vertex, target_vertex, weight=10000)

    return G, start_vertex, target_vertex


class Graph:
    def __init__(self, config_):
        self.G, self.start, self.target = parse_config(config_)
        self.vertices = sorted(list(self.G.nodes()))
        self.agent_locations = dict()
        self.policies = dict()

    def set_policies(self, policies):
        self.policies = policies

    def get_neighbors(self, vertex):
        return list(self.G.neighbors(vertex))

    def get_neighbors_by_id(self, vertex_id, id_=False):
        vertex = self.vertices[vertex_id]
        if id_:
            return [neighbor.id_ for neighbor in self.G.neighbors(vertex)]
        return [neighbor for neighbor in self.G.neighbors(vertex)]

    def get_node(self, node):
        for vertex in self.G.nodes():
            if vertex.id_ == node:
                return vertex

    def insert_agent(self, agent, vertex_id):
        vertex = self.vertices[vertex_id]
        self.agent_locations[agent.id_] = vertex

    def change_agent_location(self, agent, vertex):
        print("agent %d has moved from %d to %d\n" % (agent.id_, self.agent_locations[agent.id_].id_, vertex.id_))
        self.agent_locations[agent.id_] = vertex

    def print_veritcies(self):
        for node in self.vertices:
            print("V%s(probability=%s, blocked=%s)" % (node.id_, node.prob, node.blocked))

    def print_graph(self):
        print("========= nodes =============")
        self.print_veritcies()
        print("========= edges =============")
        for u, v in self.G.edges():
            print("V%s <=======> V%s weight=%s" % (u.id_, v.id_, self.G[u][v]['weight']))
