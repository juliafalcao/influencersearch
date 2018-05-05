from graph import *
import fb_init
import yt_init

import random
import sys

TOTAL_NODES = 1134890

# heuristic IDs
FRIENDS = 1
GROUPS = 2


def main():
    graph = yt_init.build_graph()

    """
    print("RANDOM RESTART HILL CLIMBING:")
    solution = search(graph, FRIENDS, k = 3)
    print("solution: " + str(solution))
    """
      
    print("EXACT DFS:")
    print("global max: " + str(dfs(graph, FRIENDS)))
    # global max: 1072

    

def heuristic_function(heuristic_id, graph, node):
    if heuristic_id == FRIENDS:
        return graph.neighbor_count(node)
    
    elif heuristic_id == GROUPS:
        return graph.group_count(node)
    
    else:
        print("ERROR: Invalid heuristic ID.")
        return


# main random-restart hill climbing search function
# decides initial node, runs hill climbing search iteratively,
# checks when to stop iterations
def search(graph, heuristic_id, k = 1):
    influencers = []

    while (len(set(influencers)) < k): # para encontrar k soluções diferentes
        initial_node = random_node(graph)

        for local_max in set(influencers):
            while initial_node in graph.neighbors[local_max]:
                print("guided restart")
                print("last local max: " + str(last_local_max))
                print("change initial node to: ")
                initial_node = random_node(graph)
                print(initial_node)


        print("k = " + str(k))
        print("initial node: " + str(initial_node))
        local_max = hill_climbing(graph, initial_node, heuristic_id)
        print("local max: " + str(local_max))
        print("\n")
        influencers.append(local_max)
    
    return set(influencers)

"""
# circle count
def next_node_2(graph, current_node):
    neighbors = graph.neighbors[current_node]

    max_circle_count = 0
    max_neighbor = None

    for n in neighbors:
        circle_count = graph.group_count(n)

        if circle_count is None:
            circle_count = 0

        if circle_count > max_circle_count:
            max_circle_count = circle_count
            max_neighbor = n
    
    return max_neighbor

# friend count
def next_node_1(graph, current_node):
    neighbors = graph.neighbors[current_node]
    
    max_friend_count = 0
    max_neighbor = None
    
    for n in neighbors:
        friend_count = graph.neighbor_count(n)

        if friend_count > max_friend_count:
            max_friend_count = friend_count
            max_neighbor = n

    return max_neighbor
"""

def next_node(graph, current_node, heuristic_id):
    neighbors = graph.neighbors[current_node]

    max_count = 0
    max_neighbor = None

    for n in neighbors:
        count = heuristic_function(heuristic_id, graph, current_node)
        if count > max_count:
            max_count = count
            max_neighbor = n
    
    return max_neighbor

# hill climbing search
# next is the function that returns the next node to visit (the one with the highest heuristic value)
def hill_climbing(graph, initial_node, heuristic_id):
    if initial_node not in graph.neighbors:
        print("ERROR: Initial node given is not in graph.")
        return

    current = initial_node
    
    while True:
        # !!
        next = next_node(graph, current, heuristic_id)

        if heuristic_function(heuristic_id, graph, next) < heuristic_function(heuristic_id, graph, current):
            return current # fim da busca

        current = next

# choose a random node from the graph
def random_node(graph):
    nodes = list(graph.neighbors.keys())
    return random.choice(nodes)


# exact depth-first search
def dfs(graph, heuristic_id):
    initial_node = random_node(graph)
    visited = set()
    stack = []
    max_value = 0
    global_max = None

    stack.append(initial_node)

    while stack:
        current = stack.pop()

        if current not in visited:
            value = heuristic_function(heuristic_id, graph, current)

            if value > max_value:
                max_value = value
                global_max = current

                visited.add(current)
                stack.extend(graph.neighbors[current] - visited)
    
    return global_max




main()