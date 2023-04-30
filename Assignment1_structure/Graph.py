from Vertex import Vertex


def parse_config(config_):
    num_vertex = 0
    all_vertices = []
    all_edges = []
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
                    all_vertices.append(Vertex(vertex_name, amount_of_people, vertex_is_brittle))
                elif len(info_on_vertex) == 2:
                    vertex_name = int(info_on_vertex[0][1:]) - 1
                    if 'P' in info_on_vertex[1]:
                        amount_of_people = int(info_on_vertex[1][1:])
                        vertex_is_brittle = False
                    else:
                        amount_of_people = 0
                        vertex_is_brittle = True
                    all_vertices.append(Vertex(vertex_name, amount_of_people, vertex_is_brittle))
                else:
                    vertex_name = int(info_on_vertex[0][1:]) - 1
                    amount_of_people = int(info_on_vertex[1][1:])
                    vertex_is_brittle = True
                    all_vertices.append(Vertex(vertex_name, amount_of_people, vertex_is_brittle))
            else:
                info_on_vertex = line.split()[1:]
                assert len(info_on_vertex) == 3
                all_edges.append((int(info_on_vertex[0]) - 1,
                                  int(info_on_vertex[1]) - 1,
                                  int(info_on_vertex[2][1:])))
    return num_vertex, all_vertices, all_edges


class Graph:
    def __init__(self, config_):
        self.num_of_vertices, self.vertices, self.edges = parse_config(config_)
        self.graph_dict = self.build_dict_graph()
        self.agent_locations = {}
        self.total_number_of_people_evacuated = 0
        self.people_to_save = sum([node.people for node in self.vertices])

    def build_dict_graph(self):
        dict_graph = dict()
        for vertex in self.vertices:
            dict_graph[vertex] = []
        for edge in self.edges:
            source_vertex_id = edge[0]
            source_vertex = self.vertices[source_vertex_id]
            assert source_vertex.id_ == source_vertex_id
            target_vertex_id = edge[1]
            target_vertex = self.vertices[target_vertex_id]
            assert target_vertex.id_ == target_vertex_id
            dict_graph[source_vertex].append((target_vertex, edge[2]))
            dict_graph[target_vertex].append((source_vertex, edge[2]))
        return dict_graph

    def change_agent_location(self, agent, vertex):
        print("agent %d has moved from %d to %d\n" % (agent.id_, self.agent_locations[agent].id_, vertex.id_))
        self.agent_locations[agent] = vertex

    def insert_agent(self, agent, vertexid, pickup):
        vertex = self.vertices[vertexid]
        self.agent_locations[agent] = vertex
        if pickup:
            agent.state.people_saved += vertex.people
            self.total_number_of_people_evacuated += vertex.people
            vertex.people = 0
        if vertex.is_brittle:
            vertex.is_broken = True

    def __repr__(self):
        res = ""
        for vertex in self.graph_dict:
            for neighbourhood in self.graph_dict[vertex]:
                res += str(vertex.id_) + f"---{str(neighbourhood[1])}-->"
                res += str(neighbourhood[0]) + "  "
            res += '\n'
        return res
