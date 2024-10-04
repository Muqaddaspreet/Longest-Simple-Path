# Longest Simple Path Heuristic Algorithms

## Project Overview

This project focuses on exploring various graph algorithms to approximate the **Longest Simple Path (LSP)** in undirected, unweighted geometric and online graphs. The LSP problem is classified as NP-hard, and we aim to develop and analyze several heuristic algorithms to tackle this problem.

### Key Objectives:
1. **Geometric Graph Generator Development**: Producing undirected, unweighted geometric graphs with nodes placed randomly within a unit square, using a given radius for connectivity.
2. **Graph Selection and Preparation**: Utilizing both custom-generated Euclidean graphs and graphs from online repositories to analyze the heuristics.
3. **Analysis of Graph Components**: Identifying the Largest Connected Component (LCC) for each graph, which serves as the basis for the heuristic evaluations.
4. **Implementation of Pathfinding Heuristics**: Implementing and testing four different heuristic algorithms for calculating the longest simple path.
5. **Metric Compilation and Evaluation**: Comparing the performance of the heuristics based on their ability to find the longest simple paths.

## Heuristic Algorithms Implemented:
1. **DFS-Based Longest Simple Path**: Uses depth-first search (DFS) with restarts to find the longest path.
2. **Dijkstra's Algorithm for Longest Simple Path**: A modified version of Dijkstra's algorithm that finds the longest path in terms of the number of edges.
3. **A* Algorithm for Longest Simple Path**: Utilizes the A* search algorithm with Euclidean distance as the heuristic.
4. **Custom Heuristic for Longest Simple Path**: Introduces a new heuristic based on node degrees to prioritize unexplored areas of the graph.

## Implementation Details

1. **Geometric Graph Generator**: 
   - Function: `generate_geometric_graph(n, r)`
   - This function generates undirected, unweighted geometric graphs by randomly placing `n` nodes within a unit square and connecting nodes based on a radius `r`.

2. **Largest Connected Component (LCC)**:
   - Function: `find_lcc(vertices, edges)`
   - Finds and returns the largest connected component in a given graph using a DFS-based approach.

3. **Pathfinding Heuristics**:
   - DFS, Dijkstra, A*, and the custom heuristic were applied to find the longest simple path within the largest connected component of each graph.

## Correctness and Results
To validate the correctness of our algorithms, we tested them on smaller datasets and compared the results across various metrics such as the size of the largest connected component (LCC), maximum degree, and longest simple path (LSP). 

**Sample Result Table (Graph Size: n=300):**
| Algorithm          | Nodes in LCC | Maximum Degree | Average Degree | LSP Length |
|--------------------|--------------|----------------|----------------|------------|
| DFS-Heuristic      | 282          | 24             | 11.26          | 133        |
| Dijkstra-Heuristic | 282          | 24             | 11.26          | 132        |
| A* Heuristic       | 282          | 24             | 11.26          | 118        |
| Custom Heuristic   | 282          | 24             | 11.26          | 135        |

## Conclusion
The custom heuristic often performs comparably to traditional heuristics and even excels in certain metrics, particularly for larger or more complex graphs. However, its performance can vary based on the graph's characteristics, indicating potential for further optimization.

## References
- **T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein**: Introduction to Algorithms, 4th Edition, The MIT Press, 2022.
- **Wikipedia Contributors**: A* Search Algorithm, Wikipedia, 2024.
