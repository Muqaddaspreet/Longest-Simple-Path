import heapq
from collections import defaultdict, deque

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.vertices = set()

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.vertices.update([u, v])

    def dfs(self, start):
        stack = [start]
        visited = set()
        component = []
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                component.append(node)
                stack.extend(self.graph[node])
        return visited, component

    def get_lcc(self):
        visited_global = set()
        largest_cc = []
        for vertex in self.vertices:
            if vertex not in visited_global:
                visited, component = self.dfs(vertex)
                visited_global.update(visited)
                if len(component) > len(largest_cc):
                    largest_cc = component
        return largest_cc

    def degree_metrics(self, lcc):
        max_degree = 0
        total_degrees = sum(len(self.graph[v]) for v in lcc)
        for v in lcc:
            if len(self.graph[v]) > max_degree:
                max_degree = len(self.graph[v])
        avg_degree = total_degrees / len(lcc) if lcc else 0
        return max_degree, avg_degree


def heuristic(node, goal, graph):
    # Since the graph is unweighted and we don't have spatial data, heuristic could be simply the negative degree of the node
    return -len(graph[node])


def a_star_longest_path(graph, start):
    open_set = []
    heapq.heappush(open_set, (0, start, [start]))
    visited = {start: 0}

    longest_path = []
    longest_length = 0

    while open_set:
        _, current, path = heapq.heappop(open_set)

        if len(path) > longest_length:
            longest_path = path
            longest_length = len(path)

        for neighbor in graph.graph[current]:
            if neighbor not in path:
                new_path = path + [neighbor]
                new_cost = len(new_path)
                if new_cost > visited.get(neighbor, 0):
                    visited[neighbor] = new_cost
                    heapq.heappush(open_set, (new_cost + heuristic(neighbor, None, graph.graph), neighbor, new_path))

    return longest_path


def read_graph_from_file(filename):
    g = Graph()
    with open(filename, 'r') as file:
        for line in file:
            u, _, _, v, _, _ = line.split()
            g.add_edge(int(u), int(v))
    return g


# Usage Example
filename = "graph_n5.edges"
graph = read_graph_from_file(filename)
largest_cc = graph.get_lcc()
max_degree, avg_degree = graph.degree_metrics(largest_cc)
longest_path = a_star_longest_path(graph, largest_cc[0])

print("|VLCC| (nodes in LCC):", len(largest_cc))
print("∆(LCC) (max degree in LCC):", max_degree)
print("k(LCC) (average degree in LCC):", avg_degree)
print("Lmax (longest simple path):", len(longest_path))
