from BayesianNetwork import BayesianNetWork
from Graph import Graph
import networkx as nx

if __name__ == "__main__":
    with open('input_graph.txt') as f:
        input_txt = f.read()
    graph = Graph(input_txt)
    bs = BayesianNetWork(graph)
    bs.print_info()
    bs.add_evidence(tuple([bs.all_random_vars[0], "extreme"]))
    bs.add_evidence(tuple([bs.all_random_vars[1], True]))
    bs.add_evidence(tuple([bs.all_random_vars[2], False]))
    bs.add_evidence(tuple([bs.all_random_vars[4], True]))
    bs.add_evidence(tuple([bs.all_random_vars[5], True]))
    bs.add_evidence(tuple([bs.all_random_vars[3], True]))
    print(bs.reasoning(bs.all_random_vars[6]))
    # terminate = False
    # while terminate != True:
    #     print("1. reset evidence list")
    #     print("2. Add piece of evidence")
    #     print("3. Do probabilistic reasoning")
    #     print("4. Quit")
    #     choose_option = int(input("\n"))
    #     if choose_option == 1:
    #         bs.reset_evidence()
    #     elif choose_option == 2:
    #         print("1. weather")
    #         print("2. blockage")
    #         print("3. evacuees")
    #         lvl = int(input("\n"))
    #         if lvl == 1:
    #             print("1. mild")
    #             print("2. stormy")
    #             print("3. extreme")
    #         elif lvl == 2: #blockage
    #             for node in graph.vertices:
    #                 print("%d. %d" % (node.id_, node.id_))
    #         elif lvl == 3: #evacuees
    #             for node in graph.vertices:
    #                 print("%d. %d" % (node.id_, node.id_))
    #         num = int(input("\n"))
    #         bs.add_evidence(lvl, num)
    #     elif choose_option == 3:
    #         bs.do_probabilistic_reasoning()
    #     elif choose_option == 4:
    #         exit(0)