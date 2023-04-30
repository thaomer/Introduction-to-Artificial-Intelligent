we created a belief state for every possible observation and location.
calculated each policy ulitity score usine value iteration
and the choose the move according to the policy
** for every vertex name we did -1

input:
#V 5
#E1 1 2 W3
#E2 2 3 W2
#E3 3 4 W3
#E4 4 5 W1
#E5 2 4 W4
#B 2 0.3
#B 3 0.8
#Start 1
#Target 5

output:
search: current_belief_state[curr_vertex=V0, observation={V1: False, V2: 'unknown'}]
agent 0 has moved from 0 to 1

search: current_belief_state[curr_vertex=V1, observation={V1: False, V2: True}]
agent 0 has moved from 1 to 3

search: current_belief_state[curr_vertex=V3, observation={V1: False, V2: True}]
agent 0 has moved from 3 to 4


input:
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

output:
search: current_belief_state[curr_vertex=V0, observation={V1: True, V2: False, V3: 'unknown', V4: 'unknown'}]
agent 0 has moved from 0 to 2

search: current_belief_state[curr_vertex=V2, observation={V1: True, V2: False, V3: True, V4: True}]
agent 0 has moved from 2 to 0

search: current_belief_state[curr_vertex=V0, observation={V1: True, V2: False, V3: True, V4: True}]
agent 0 has moved from 0 to 5
