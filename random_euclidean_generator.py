import random
import math

def generate_geometric_graph(n, r):
    """Generates a geometric graph with n nodes and radius r."""
    vertices = {i: (random.uniform(0, 1), random.uniform(0, 1)) for i in range(n)}
    edges = set()
    for u in vertices:
        for v in vertices:
            if u != v:
                if math.dist(vertices[u], vertices[v]) <= r:
                    edges.add((u, v))
    return vertices, edges

def dfs(graph, start):
    """Performs DFS on the graph from start node and returns all visited nodes."""
    stack = [start]
    visited = set()
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(set(graph[vertex]) - visited)
    return visited

def find_lcc(vertices, edges):
    """Finds the largest connected component (LCC) in the graph."""
    graph = {u: set() for u in vertices}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
        
    largest_component = set()
    visited_nodes = set()
    size = 0
    for vertex in graph:
        if vertex not in visited_nodes:
            component = dfs(graph, vertex)
            if len(component) > len(largest_component):
                largest_component = component
            visited_nodes.update(component)
    return largest_component,len(largest_component) 

def save_graph(filename, vertices, edges):
    """Saves the graph to a file in EDGES format with positional data."""
    with open(filename, 'w') as file:
        for u, v in edges:
            u_pos = vertices[u]
            v_pos = vertices[v]
            line1 = f"{u} {u_pos[0]} {u_pos[1]} {v} {v_pos[0]} {v_pos[1]}\n"
            file.write(line1)


def main():
    n_values = [300, 400, 500]
    target_lcc_ratios = [(0.9, 0.95), (0.8, 0.9), (0.7, 0.8)]

    for n, (lower_ratio, upper_ratio) in zip(n_values, target_lcc_ratios):
        r_min, r_max = 0, math.sqrt(2)  # Start with possible maximum distance in unit square
        successful_r = None
        while r_max - r_min > 0.005:  # A precision threshold for r
            r = (r_min + r_max) / 2
            vertices, edges = generate_geometric_graph(n, r)
            lcc,size = find_lcc(vertices, edges)
            if lower_ratio * n <= len(lcc) <= upper_ratio * n:
                successful_r = r
                break
            elif len(lcc) < lower_ratio * n:
                r_min = r
            else:
                r_max = r

        if successful_r is not None:
            filename = f"graph_n{n}.edges"
            save_graph(filename, vertices, edges)
            print(f"Graph saved with n={n}, r={successful_r:.4f} satisfying LCC constraints with vlcc {size}.")
        else:
            print(f"No suitable r found for n={n} within the given LCC size range with vlcc {size}.")

if __name__ == "__main__":
    main()