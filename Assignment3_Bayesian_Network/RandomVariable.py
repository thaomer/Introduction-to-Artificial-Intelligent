import random

from BooleanProb import BooleanProb


def boolean_combinations1(n):
    if n == 0:
        return [[]]
    sub_combinations = boolean_combinations1(n - 1)
    return [[False] + c for c in sub_combinations] + [[True] + c for c in sub_combinations]


def boolean_combinations(parents):
    if len(parents) == 0:
        return [[]]
    first_parent = parents[0]
    sub_combinations = boolean_combinations(parents[1:])
    return [[frozenset([first_parent, False])] + c for c in sub_combinations] + [[frozenset([first_parent, True])] + c
                                                                                 for c in sub_combinations]


def count_true(lst):
    res = []
    for index, ele in enumerate(lst):
        if ele:
            res.append(index)
    return res


def calculate_probability(evacuate_var, combination, parents, graph):
    if True not in combination:
        evacuate_var.prob_dict[tuple(list(zip(parents, combination)))] = 0
    else:
        only_true = count_true(combination)
        probability = 1
        for index in only_true:
            true_parent_brock = parents[index]
            if evacuate_var.vertex == true_parent_brock.vertex:
                probability = probability * graph.p2
            else:
                probability = probability * min(1,
                                                graph.p1 * graph.G[evacuate_var.vertex][true_parent_brock.vertex]["weight"])
        evacuate_var.prob_dict[tuple(list(zip(parents, combination)))] = 1 - probability


class RandomVariable:
    def __init__(self, vertex):
        self.vertex = vertex
        self.id_ = vertex.id_
        self.prob_dict = dict()
        self.options = [True, False]


class RandomVariableEvacuate(RandomVariable):
    def __init__(self, vertex):
        super().__init__(vertex)

    def set_probability(self, parents, world):
        combination_list = boolean_combinations1(len(parents))
        for combination in combination_list:
            calculate_probability(self, combination, parents, world)

    def get_probability(self, parents_value, p_happen):
        if p_happen:
            return self.prob_dict[tuple(parents_value)]
        else:
            return 1 - self.prob_dict[tuple(parents_value)]


    def __eq__(self, other):
        if other.__class__.__name__ == "RandomVariableWeather":
            return False
        return self.vertex == other.vertex

    def __hash__(self):
        return hash(self.vertex.id_)

    def __repr__(self):
        return f"Evacuate {self.id_ + 1}"

    def __str__(self):
        return f"Evacuate {self.id_ + 1}"


class RandomVariableBlockage(RandomVariable):
    def __init__(self, vertex):
        super().__init__(vertex)
        self.prob_dict = dict()

    def set_probability(self, weather):
        blocked_given_mild = float(self.vertex.bloc)
        self.prob_dict[tuple([weather, "mild"])] = min([1, blocked_given_mild])
        self.prob_dict[tuple([weather, "stormy"])] = min([1, blocked_given_mild*2])
        self.prob_dict[tuple([weather, "extreme"])] = min([1, blocked_given_mild*3])
        # for key, value in self.prob_dict.items():
        #     print(key[0], ",", key[1], "---> ", value)

    def __repr__(self):
        return f"Blockage {self.id_ + 1}"

    def __str__(self):
        return f"Blockage {self.id_ + 1}"

    def get_probability(self, parents_value, p_happen):
        if p_happen:
            return self.prob_dict[tuple(parents_value[0])]
        else:
            return 1 - self.prob_dict[tuple(parents_value[0])]


class RandomVariableWeather:
    def __init__(self, mild, stormy, extreme):
        self.mild = float(mild)
        self.stormy = float(stormy)
        self.extreme = float(extreme)
        self.prob_dict = dict()
        self.options = ["mild", "stormy", "extreme"]
        self.id_ = -1

    def __iter__(self, other):
        return self

    def get_probability(self, weather):
        return self.prob_dict[weather]

    def set_probability(self):
        self.prob_dict["mild"] = self.mild
        self.prob_dict["stormy"] = self.stormy
        self.prob_dict["extreme"] = self.extreme

    def __repr__(self):
        return "WeatherNode"

    def __str__(self):
        return "WeatherNode"
