from concurrent.futures import ThreadPoolExecutor
import math
from collections import defaultdict
from heapq import heappop, heappush

#The usage of threads to improve running time when number of nodes is large

# Function to read the graph from the EDGES file
def read_graph_from_edges_file(file_path):
    graph = defaultdict(list)
    positions = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            u, ux, uy, v, vx, vy = int(parts[0]), float(parts[1]), float(parts[2]), int(parts[3]), float(parts[4]), float(parts[5])
            graph[u].append(v)
            graph[v].append(u)
            positions[u] = (ux, uy)
            positions[v] = (vx, vy)
    
    return graph, positions

# Function to find the largest connected component (LCC)
def find_lcc(graph):
    visited = set()
    largest_component = []
    
    for node in graph:
        if node not in visited:
            component = []
            stack = [node]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    component.append(current)
                    stack.extend(graph[current])
            if len(component) > len(largest_component):
                largest_component = component
    return largest_component

# Function to calculate degree metrics
def calculate_degree_metrics(lcc, graph):
    degrees = [len(graph[node]) for node in lcc]
    max_degree = max(degrees)
    average_degree = sum(degrees) / len(lcc)
    return max_degree, average_degree

# Heuristic function for A* (Euclidean distance)
def heuristic(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Function for A* heuristic search for longest simple path
def a_star_longest_path(graph, positions, start, goal):
    open_set = []
    heappush(open_set, (0, start, [start]))
    visited = {start: 0}

    longest_path = []
    longest_length = 0

    while open_set:
        _, current, path = heappop(open_set)

        if current == goal and len(path) > longest_length:
            longest_path = path
            longest_length = len(path)
        
        for neighbor in graph[current]:
            if neighbor in path:
                continue
            new_path = path + [neighbor]
            path_length = len(new_path)
            if path_length > visited.get(neighbor, 0):
                visited[neighbor] = path_length
                priority = path_length - heuristic(positions[neighbor], positions[goal])
                heappush(open_set, (priority, neighbor, new_path))
    
    return longest_path

#function to calculate the compute_metrics function to use multithreading for A* path calculations
def compute_metrics_multithreaded(graph, positions):
    lcc = find_lcc(graph)
    max_degree, average_degree = calculate_degree_metrics(lcc, graph)
    def longest_path_length(pair):
        start_node, goal_node = pair
        path = a_star_longest_path(graph, positions, start_node, goal_node)
        return len(path)
    node_pairs = [(v1, v2) for idx, v1 in enumerate(lcc) for v2 in lcc[idx + 1:]]
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(longest_path_length, node_pairs))
    lmax = max(results) - 1  # Subtract one because the length is edges, not vertices
    metrics = {
        'VLCC': len(lcc),
        'Delta(LCC)': max_degree,
        'k(LCC)': average_degree,
        'Lmax': lmax
    }
    return metrics

# Sample file path for the graph data
sample_file_path = 'graph_n5.edges'

# Load the graph and positions from the sample file
graph, positions = read_graph_from_edges_file(sample_file_path)

# Compute metrics using parallel processing
metrics = compute_metrics_multithreaded(graph, positions)
print(metrics)
