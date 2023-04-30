import networkx as nx
from decimal import Decimal

from Vertex import Vertex


def parse_config(config_):
    G = nx.Graph()
    mild = 0
    stormy = 0
    extreme = 0
    for line in config_.split('\n'):
        if len(line) > 0:
            first_letter = line[1]
            if first_letter == 'N':
                info_on_vertex = line.split()[1:]
                for n in range(int(info_on_vertex[0])):
                    G.add_node(Vertex(n))
            elif first_letter == 'V':
                info_on_vertex = line.split()[1:]
                vertexid = int(info_on_vertex[0]) - 1
                bloc = info_on_vertex[2]
                for node in list(G.nodes):
                    if node.id_ == vertexid:
                        node.bloc = bloc
            elif first_letter == 'E':
                info_on_vertex = line.split()[1:]
                assert len(info_on_vertex) == 3
                source = int(info_on_vertex[0]) - 1
                source_to_put = None
                target = int(info_on_vertex[1]) - 1
                target_to_put = None
                for node in list(G.nodes):
                    if (type(node)) != type(1):
                        if node.id_ == source:
                            source_to_put = node
                weight = int(info_on_vertex[2][1:])
                for node in list(G.nodes):
                    if (type(node)) != type(1):
                        if node.id_ == target:
                            target_to_put = node
                G.add_edge(source_to_put, target_to_put, weight=weight)
            elif first_letter == 'W':
                info_on_vertex = line[3:].split()
                mild = info_on_vertex[0]
                stormy = info_on_vertex[1]
                extreme = info_on_vertex[2]
    return G, mild, stormy, extreme


class Graph:
    def __init__(self, config_):
        self.G, self.mild, self.stormy, self.extreme = parse_config(config_)
        self.vertices = sorted(list(self.G.nodes()))
        self.agent_locations = dict()
        self.total_number_of_people_evacuated = 0
        self.p1 = 0.2
        self.p2 = 0.3

    # def get_weight(self, vertex1, vertex2):
    #     return self.G

    def get_neighbors(self, vertex):
        return [neighbor for neighbor in self.G.neighbors(vertex)]

    def get_neighbors_by_id(self, vertex_id, id_=False):
        vertex = self.vertices[vertex_id]
        if id_:
            return [neighbor.id_ for neighbor in self.G.neighbors(vertex)]
        return [neighbor for neighbor in self.G.neighbors(vertex)]

    def get_node(self, node):
        for vertex in self.G.nodes():
            if vertex.id_ == node:
                return vertex

    def insert_agent(self, agent, vertexid, pickup):
        vertex = self.vertices[vertexid]
        self.agent_locations[agent.id_] = vertex

    def change_agent_location(self, agent, vertex):
        print("agent %d has moved from %d to %d\n" % (agent.id_, self.agent_locations[agent.id_].id_, vertex.id_))
        self.agent_locations[agent.id_] = vertex

    def __repr__(self):
        return "nodes:%s  \n mild=%s\n stormy=%s\n extreme =%s\n p1=%s\n p2=%s\n" % (self.vertices, self.mild,
                                                                                     self.stormy, self.extreme,
                                                                                     self.p1, self.p2)
