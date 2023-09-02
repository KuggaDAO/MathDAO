import random

def random_walk(graph, start_node, walk_length):
    walk = [start_node]
    for _ in range(walk_length-1):
        neighbors = list(graph.neighbors(walk[-1]))
        if len(neighbors) > 0:
            walk.append(random.choice(neighbors))
        else:
            break
    return walk

def generate_walks(graph, num_walks, walk_length):
    walks = []
    nodes = list(graph.nodes())
    for _ in range(num_walks):
        random.shuffle(nodes)
        for node in nodes:
            walk = random_walk(graph, node, walk_length)
            walks.append(walk)
    return walks