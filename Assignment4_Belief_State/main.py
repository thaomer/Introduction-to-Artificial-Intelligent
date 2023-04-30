from Graph import Graph
from BeliefState import BeliefState
from Agent import Agent
import itertools

#V 6
#E1 1 2 W1
#E2 1 3 W1
#E3 2 4 W1
#E4 3 4 W1
#E5 3 5 W1
#E6 5 6 W1
#E7 4 6 W1
#B 2 0.5
#B 3 0.5
#B 4 0.5
#B 5 0.5
#Start 1
#Target 6


def generate_states(graph):
    b_states = []
    vertices = graph.vertices
    blockable_vertices = [vertex for vertex in vertices if vertex.get_probability()]
    blockable_vertices_states = itertools.product([True, False, "unknown"], repeat=len(blockable_vertices))
    for state in blockable_vertices_states:
        vertices_state_dict = dict(zip(blockable_vertices, state))
        for vertex in vertices:
            legal_state = True
            # neighbours = graph.get_neighbors(vertex) + [vertex]
            # for neighbour in neighbours:
            #     if (neighbour in vertices_state_dict) and (vertices_state_dict[neighbour] == "unknown"):
            #         legal_state = False
            #         break
            if (vertex in vertices_state_dict) and (vertices_state_dict[vertex] == True):
                legal_state = False

            if legal_state:
                b_states.append(BeliefState(vertex, vertices_state_dict))
    return b_states

def generate_policies(belief_states, graph):
    utility_scores = {}
    for state in belief_states:
        if state.vertex == graph.target:
            utility_scores[state] = 0
        else:
            utility_scores[state] = -10000

    change = True
    while change:
        change = False
        for state in [state for state in belief_states if state.vertex != graph.target]:
            max_utility = -10000
            for neighbour in graph.get_neighbors(state.vertex):
                # if neighbour is blocked in observation no need to check
                if (neighbour in state.observation) and (state.observation[neighbour] == True):
                    continue

                for neighbour_state in [n_state for n_state in belief_states if n_state.vertex == neighbour and n_state.observation == state.observation]:
                    if (neighbour in state.observation) and (state.observation[neighbour] == "unknown"):
                        prob = neighbour.get_probability()
                    else:
                        prob = 0
                    utility = (-1 * graph.G[state.vertex][neighbour]['weight']) + \
                            1 * ((utility_scores[neighbour_state] * (1 - prob)) + \
                                 (prob * utility_scores[state]))
                    if utility > max_utility:
                        max_utility = utility

            if max_utility > utility_scores[state]:
                utility_scores[state] = max_utility
                change = True

    print("=============== utility scores ==============")
    for b_state in utility_scores:
        print("belief_state[%s] score=%s" % (b_state, utility_scores[b_state]))

    policies = {}
    for state in [state for state in belief_states if state.vertex != graph.target]:
        max_score = -100000
        target_vertex = None
        for neighbour in graph.get_neighbors(state.vertex):
            for neighbour_state in [n_state for n_state in belief_states if
                                n_state.vertex == neighbour and n_state.observation == state.observation]:
                score = utility_scores[neighbour_state] - graph.G[state.vertex][neighbour]['weight']
                if score >= max_score:
                    max_score = score
                    target_vertex = neighbour
        policies[state] = target_vertex

    return policies

if __name__ == "__main__":
    # create graph
    with open('input_graph.txt') as f:
        input_txt = f.read()
    graph = Graph(input_txt)
    graph.print_graph()

    # create policies
    belief_states = generate_states(graph)
    policies = generate_policies(belief_states, graph)
    print("============== policy ================")
    for b_state in policies:
        print("belief_state[%s] optimal_target_vertex=%s" % (b_state, policies[b_state]))
    graph.set_policies(policies)

    # create agent
    agent = Agent(0)
    observation = {}
    blockable_vertices = [vertex for vertex in graph.vertices if vertex.get_probability()]
    for vertex in blockable_vertices:
        observation[vertex] = "unknown"
    agent.state.set_observation(observation)
    graph.insert_agent(agent, graph.start.id_)

    # run agent
    print("================== simulation =================")
    while graph.agent_locations[agent.id_] != graph.target:
        action = agent(graph)
        is_terminated = action()
        if is_terminated:
            print("agent is terminated")
            break
