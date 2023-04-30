from Vertex import Vertex
import networkx as nx


def parse_config(config_):
    G = nx.Graph()
    for line in config_.split('\n'):
        if len(line) > 0:
            first_letter = line[1]
            if first_letter == 'N':
                num_vertex = int(line[3:])
            elif first_letter == 'V':
                info_on_vertex = line[1:].split()
                if len(info_on_vertex) == 1:
                    vertex_name = int(info_on_vertex[0][1:]) - 1
                    amount_of_people = 0
                    vertex_is_brittle = False
                    G.add_node(Vertex(vertex_name, amount_of_people, vertex_is_brittle))
                elif len(info_on_vertex) == 2:
                    vertex_name = int(info_on_vertex[0][1:]) - 1
                    if 'P' in info_on_vertex[1]:
                        amount_of_people = int(info_on_vertex[1][1:])
                        vertex_is_brittle = False
                    else:
                        amount_of_people = 0
                        vertex_is_brittle = True
                    G.add_node(Vertex(vertex_name, amount_of_people, vertex_is_brittle))
                else:
                    vertex_name = int(info_on_vertex[0][1:]) - 1
                    amount_of_people = int(info_on_vertex[1][1:])
                    vertex_is_brittle = True
                    G.add_node(Vertex(vertex_name, amount_of_people, vertex_is_brittle))
            else:
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
    return G


class Graph:
    def __init__(self, config_):
        self.G = parse_config(config_)
        self.vertices = sorted(list(self.G.nodes()))
        self.agent_locations = dict()
        self.total_number_of_people_evacuated = 0
        self.agents = []

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
        if pickup:
            agent.state.people_saved += vertex.people
            self.total_number_of_people_evacuated += vertex.people
            vertex.people = 0
        if vertex.is_brittle:
            vertex.is_broken = True

    def change_agent_location(self, agent, vertex):
        print("agent %d has moved from %d to %d\n" % (agent.id_, self.agent_locations[agent.id_].id_, vertex.id_))
        self.agent_locations[agent.id_] = vertex

    def __repr__(self):
        return f"people: {[vertex.people for vertex in self.G.nodes()]}\n" \
               f"brokens: {[vertex.is_broken for vertex in self.G.nodes()]}\n"
