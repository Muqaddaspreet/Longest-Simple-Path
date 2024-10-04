import heapq

def read_graph_from_file(file_path):
    with open(file_path, 'r') as file:
        edges = {}
        for line in file.readlines():
            u,v = line.split()
            u, v = int(u), int(v)
            if u not in edges:
                edges[u] = set()
            if v not in edges:
                edges[v] = set()
            edges[u].add(v)
            edges[v].add(u)
    return edges

def dfs(graph, start, visited):
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited

def find_lcc(edges):
    visited = set()
    largest_component = set()
    for vertex in edges:
        if vertex not in visited:
            component = set()
            dfs(edges, vertex, component)
            if len(component) > len(largest_component):
                largest_component = component
            visited.update(component)
    return largest_component

def calculate_degrees(edges, lcc):
    degrees = {v: len(edges[v]) for v in lcc}
    max_degree = max(degrees.values())
    avg_degree = sum(degrees.values()) / len(lcc)
    return max_degree, avg_degree, degrees

def dijkstra_max(edges, s):
    distances = {v: float('-inf') for v in edges}
    distances[s] = 0
    max_heap = [(-dist, u) for u, dist in distances.items()]
    heapq.heapify(max_heap)
    visited = set()

    while max_heap:
        dist, u = heapq.heappop(max_heap)
        dist = -dist  # Convert back to positive distance
        if u in visited:
            continue
        visited.add(u)
        for v in edges.get(u, []):
            if v not in visited and distances[v] < dist + 1:
                distances[v] = dist + 1
                heapq.heappush(max_heap, (-distances[v], v))

    return distances

def find_longest_path_end(edges):
    lcc = find_lcc(edges)
    subgraph = {v: edges[v] & lcc for v in lcc}
    max_degree, avg_degree, degrees = calculate_degrees(edges, lcc)
    max_distance = float('-inf')
    max_vertex = None
    for s in subgraph:
        distances = dijkstra_max(subgraph, s)
        farthest_vertex = max(distances, key=distances.get)
        if distances[farthest_vertex] > max_distance:
            max_distance = distances[farthest_vertex]
            max_vertex = farthest_vertex
    return max_vertex, max_distance, len(lcc), max_degree, avg_degree

# Main execution
file_path = 'inf-power.edges'  # Replace with the data_file name
edges = read_graph_from_file(file_path)
max_vertex, longest_path_length, lcc_size, max_degree, avg_degree = find_longest_path_end(edges)


print(f"|VLCC| (number of nodes in LCC): {lcc_size}")
print(f"∆(LCC) (maximum degree within LCC): {max_degree}")
print(f"k(LCC) (average degree within LCC): {avg_degree}")
print(f"Lmax (length of longest simple path in LCC): {longest_path_length}")