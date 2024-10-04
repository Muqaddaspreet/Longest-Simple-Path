from collections import deque
import random
from collections import defaultdict, deque
import sys
#usage of threads to allow faster procesing of larger no of nodes
sys.setrecursionlimit(10000)
class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.vertices = set()

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)  # Assuming the graph is undirected
        self.vertices.update([u, v])

    def get_largest_connected_component(self):
        visited = set()
        largest_cc = []
        component_edges = 0
        for start in self.vertices:
            if start not in visited:
                current_cc = []
                queue = deque([start])
                while queue:
                    node = queue.popleft()
                    if node not in visited:
                        visited.add(node)
                        current_cc.append(node)
                        for neighbor in self.graph[node]:
                            if neighbor not in visited:
                                queue.append(neighbor)
                            if node < neighbor:  # count each edge only once
                                component_edges += 1
                if len(current_cc) > len(largest_cc):
                    largest_cc = current_cc
                    largest_component_edges = component_edges
        return largest_cc, largest_component_edges

    def degree_of(self, vertex):
        degree = len(self.graph[vertex])
        return degree

    def maximum_degree(self, vertices):
        max_degree = 0
        max_vertex = None
        for v in vertices:
            degree = self.degree_of(v)
            if degree > max_degree:
                max_degree = degree
                max_vertex = v
        return max_degree

    def average_degree(self, vertices, edges):
        if len(vertices) == 0:
            return 0
        return 2 * edges / len(vertices)

    def longest_path_heuristic(self):
        def dfs(node, path, visited):
            visited.add(node)
            path = path + [node]
            longest_path = path[:]

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    new_path = dfs(neighbor, path, visited)
                    longest_path = max(longest_path, new_path, key=len)
            return longest_path 

        longest_path = []
        for node in self.vertices:
            path = dfs(node, [], set())
            longest_path = max(longest_path, path, key=len)

        return longest_path

def dfs(graph, start):
    visited = {}
    stack = [(start, 0)]
    max_depth = 0
    deepest_vertex = start

    while stack:
        vertex, depth = stack.pop()
        if vertex not in visited:
            visited[vertex] = depth
            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    stack.append((neighbor, depth + 1))
            if depth > max_depth:
                max_depth = depth
                deepest_vertex = vertex

    return visited, deepest_vertex, max_depth


def longest_simple_path_dfs(graph, vertices_lcc, iterations=10):
    best_path_length = 0

    for _ in range(iterations):
        initial_vertex = random.choice(vertices_lcc)
        _, deepest_vertex, _ = dfs(graph, initial_vertex)
        _, _, path_length = dfs(graph, deepest_vertex)

        if path_length > best_path_length:
            best_path_length = path_length

    return best_path_length


def read_graph_from_file(filename):
    g = Graph()
    with open(filename, 'r') as file:
        for line in file:
            u,v = line.split()
            node1 = u
            node2 = v
            g.add_edge(node1, node2)
    return g


# change the file name to datafile_name 
filename = "inf-euroroad.edges"
graph = read_graph_from_file(filename)
#calculate LCC for the given graph
vertices_lcc, edges_lcc = graph.get_largest_connected_component()

# Compute the longest simple path using DFS heuristic
longest_path_length = longest_simple_path_dfs(graph, vertices_lcc)

n = len(graph.vertices)
VLCC = len(vertices_lcc)
Delta_LCC = graph.maximum_degree(vertices_lcc)
k_LCC = graph.average_degree(vertices_lcc, edges_lcc)
Lmax = len(graph.longest_path_heuristic())-1 #to convert it in edges since longest path is calculated in terms of nodes


print("|VLCC| (nodes in LCC):", VLCC)
print("∆(LCC) (max degree in LCC):", Delta_LCC)
print("k(LCC) (average degree in LCC):", k_LCC)
print("Lmax (longest simple path):", Lmax)