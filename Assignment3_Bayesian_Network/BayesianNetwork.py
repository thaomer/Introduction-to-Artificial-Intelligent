import networkx as nx
from RandomVariable import RandomVariableEvacuate, RandomVariableBlockage, RandomVariableWeather
import copy


def generate_nodes(graph):
    bs = nx.DiGraph()
    weather = RandomVariableWeather(graph.mild, graph.stormy, graph.extreme)
    bs.add_node(weather)
    for node in graph.G.nodes():
        bs.add_node(RandomVariableEvacuate(node))
        bs.add_node(RandomVariableBlockage(node))
    return bs, weather


def generate_edges(graph, weather, bs, evacuates, blockages):
    for blockage_node in blockages:
        neighbors = graph.get_neighbors_by_id(blockage_node.id_, id_=True)
        neighbors.append(blockage_node.id_)
        random_variables_neighbors = [random_variable for random_variable in evacuates if
                                      random_variable.id_ in neighbors]
        for son in random_variables_neighbors:
            bs.add_edge(blockage_node, son)
    for blockage in blockages:
        bs.add_edge(weather, blockage)


def divide_bs(bs):
    blocked = [node for node in bs.nodes() if type(node) == RandomVariableBlockage]
    evacuate = [node for node in bs.nodes() if type(node) == RandomVariableEvacuate]
    return blocked, evacuate


def normalize(vector):
    res = []
    s = sum(vector)
    for element in vector:
        res.append(element / s)
    return res


def enumeration_ask(x, evidences, bn):
    distribution_over_x = [0 for i in range(len(x.options))]
    for index, option in enumerate(x.options):
        a = evidences.copy()
        d = dict()
        distribution_over_x[index] = enumerate_all(bn.all_random_vars, a + [(x, option)], bn, d)
    return normalize(distribution_over_x)


def has_value_in_e(var, evidences_list):
    for evidence in evidences_list:
        if var == evidence[0]:
            if var.__class__.__name__ == evidence[0].__class__.__name__:
                return evidence
    return False


# [(weather, "extreme"), (blockage1, True), (blockage3, True)]
def add_var_to_list(lst, var):
    a = lst.copy()


def enumerate_all(bn_vars, evidences, bn, d):
    if len(bn_vars) == 0:
        return 1
    Y_ = bn_vars[0]
    appears = has_value_in_e(Y_, evidences)
    parents = bn.get_parents(Y_)
    if appears:
        d[Y_] = appears[1]
        if len(parents) == 0:
            print(Y_.get_probability(appears[1]))
            return Y_.get_probability(appears[1]) * enumerate_all(bn_vars[1:], evidences, bn, d.copy())
        else:
            list_of_probs = []
            for parent in parents:
                list_of_probs.append(tuple([parent] + [d[parent]]))
            Y_.get_probability(list_of_probs, d[Y_])
            print(Y_.get_probability(list_of_probs, d[Y_]))
            return Y_.get_probability(list_of_probs, d[Y_]) * enumerate_all(bn_vars[1:], evidences, bn, d.copy())
    else:
        counter = 0
        for option in Y_.options:
            a = evidences.copy()
            counter += 0
            list_of_probs = []
            for parent in parents:
                list_of_probs.append(tuple([parent] + [d[parent]]))
            d[Y_] = option
            print(Y_.get_probability(list_of_probs, option))
            counter += Y_.get_probability(list_of_probs, option) * enumerate_all(bn_vars[1:], a + [(Y_, option)], bn,
                                                                                 d.copy())
        return counter


def get_relevant_random_var(vertex_number, random_var_list):
    for random_var in random_var_list:
        if random_var.id_ == int(vertex_number):
            return random_var


class BayesianNetWork:
    def __init__(self, world):
        self.original_world = world
        self.G, self.weather = generate_nodes(world)
        self.blocked, self.evacuate = divide_bs(self.G)
        generate_edges(world, self.weather, self.G, self.evacuate, self.blocked)
        self.p1 = world.p1
        self.p2 = world.p2
        self.generate_probabilities()
        self.evidence_list = []
        self.all_random_vars = [self.weather] + self.blocked + self.evacuate

    def reset_evidence(self):
        self.evidence_list = []

    def add_evidence(self, evidence):  # evidence: (Evacuate_n, True\False), (Blockage_n, True\False), (W, m/s/e)
        node_type = evidence[0]
        vertex_number = node_type.id_
        value = evidence[1]
        if node_type.__class__.__name__ == "RandomVariableWeather":
            self.evidence_list.append((self.weather, value))
        elif node_type.__class__.__name__ == "RandomVariableBlockage":
            random_var = get_relevant_random_var(vertex_number, self.blocked)
            self.evidence_list.append((random_var, value))
        elif node_type.__class__.__name__ == "RandomVariableEvacuate":
            random_var = get_relevant_random_var(vertex_number, self.evacuate)
            self.evidence_list.append((random_var, value))

    def __repr__(self):
        return "nodes:%s  \n" % self.blocked

    def get_parents(self, node):
        return list(self.G.predecessors(node))

    def generate_probabilities(self):
        self.weather.set_probability()
        for blocked in self.blocked:
            blocked.set_probability(self.weather)
        for evacuate in self.evacuate:
            evacuate.set_probability(self.get_parents(evacuate), self.original_world)

    def reasoning(self, a):
        return enumeration_ask(a, self.evidence_list, self)

    def b_and_e_nodes(self, vertex):
        b_node = None
        e_node = None
        for blocked in self.blocked:
            if vertex.id_ == blocked.id_:
                b_node = blocked
                break
        for evacuees in self.evacuate:
            if vertex.id_ == evacuees.id_:
                e_node = evacuees
                break
        return b_node, e_node

    def print_info(self):
        print("WEATHER:")
        for key, value in self.weather.prob_dict.items():
            print(f"\tP({key}) = {value}")
        for vertex in self.original_world.G.nodes():
            b_node, e_node = self.b_and_e_nodes(vertex)
            print(f"\nVERTEX {vertex.id_ + 1}:")
            for key, value in b_node.prob_dict.items():
                print(f"\tP(blocked|{key}) = {value}")
            print("")
            for key, value in e_node.prob_dict.items():
                print(f"\tP(Evacuees|{key}) = {value}")
