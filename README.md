# 12402080601067_DAA-Mini-Project
Campus Navigation And Path Finding System
# Campus Navigation and Path-Finding System

## 📌 Project Overview

The **Campus Navigation and Path-Finding System** is a mini project developed as part of the **Design and Analysis of Algorithms (DAA)** course. The project aims to find routes between different locations on a college campus using graph-based path-finding algorithms.

In this system, campus buildings are represented as **nodes (vertices)**, while the walkways connecting them are represented as **weighted edges**. Each edge represents the distance between two locations.

The project implements and compares four popular graph traversal and path-finding algorithms: **Breadth-First Search (BFS), Depth-First Search (DFS), Dijkstra's Algorithm, and A\***.

The system evaluates these algorithms based on the path found, total distance, number of nodes explored, and execution time.

## 🎯 Objectives

- Represent the campus as a weighted graph using an adjacency list.
- Implement BFS, DFS, Dijkstra's Algorithm, and A* in Python.
- Find routes between a user-selected source and destination.
- Calculate the total distance of each route.
- Measure the number of nodes explored and execution time.
- Compare the performance of all four algorithms.
- Analyze their time and space complexity.
- Identify the most suitable algorithm for campus navigation.

## 🛠️ Technologies Used

- **Programming Language:** Python 3
- **Data Structure:** Graph using an adjacency list
- **Queue:** `collections.deque` for BFS
- **Stack:** Python list for DFS
- **Priority Queue:** `heapq` for Dijkstra and A*
- **Execution Time Measurement:** `time.perf_counter()`
- **Additional Libraries:** `math`, `random`

The current implementation uses Python's built-in libraries and does not require external packages.

## 🧠 Algorithms Implemented

### 1. Breadth-First Search (BFS)
BFS explores the graph level by level using a queue. It finds a path with the fewest edges in an unweighted graph, but it does not necessarily find the shortest-distance route when edges have different weights.

### 2. Depth-First Search (DFS)
DFS explores one branch of the graph as deeply as possible before backtracking. It uses a stack and can find a route between locations, but it does not guarantee the shortest path.

### 3. Dijkstra's Algorithm
Dijkstra's Algorithm finds the shortest-distance path in a graph with non-negative edge weights. It uses a priority queue to process locations in increasing order of their known distances.

### 4. A* Search Algorithm
A* combines the actual cost of reaching a location with a heuristic estimate of the remaining distance to the destination.

It uses the evaluation function:

**f(n) = g(n) + h(n)**

Where:
- `g(n)` is the actual cost from the source to node `n`.
- `h(n)` is the estimated cost from node `n` to the destination.
- `f(n)` is the estimated total route cost through node `n`.

With a suitable admissible heuristic, A* can find an optimal path while potentially exploring fewer nodes than Dijkstra's Algorithm.

## ⚙️ Features

- Sample campus map containing buildings and connecting walkways.
- User input for source and destination locations.
- Implementation of four graph algorithms.
- Route reconstruction and total distance calculation.
- Measurement of nodes explored.
- Execution time comparison.
- Optional scalability benchmark for graphs containing 10, 50, 100, and 500 nodes.
- Comparison of algorithm performance on the same graph.

## 📂 Project Structure

```text
Campus-Navigation/
│
├── campus_navigation.py
└── README.md
```

- `campus_navigation.py`: Contains the campus graph, four path-finding algorithms, performance comparison, and scalability benchmark.
- `README.md`: Contains the project description, objectives, algorithms, and instructions.

## 🚀 Installation and Execution

### Prerequisites

- Python 3 installed on your computer.
- A code editor such as Visual Studio Code, PyCharm, or any text editor.

### Steps to Run

**1. Download or clone the project.**

**2. Open the project folder in your terminal.**

**3. Run the Python program:**

```bash
python campus_navigation.py
```

If your system uses `python3`, run:

```bash
python3 campus_navigation.py
```

**4. Select the source and destination.**

The program displays the available campus locations. Enter the corresponding numbers to choose the starting and destination buildings.

**5. View the results.**

The program displays the route, total distance, nodes explored, and execution time for each algorithm.

**6. Run the scalability benchmark (optional).**

When prompted, enter `y` to compare algorithm performance on graphs containing 10, 50, 100, and 500 nodes.

## 📊 Performance Analysis

The system compares the algorithms using the following metrics:

| Metric | Description |
|---|---|
| Path | Sequence of buildings from source to destination |
| Total Distance | Sum of the weights of the edges in the selected path |
| Nodes Explored | Number of nodes processed during the search |
| Execution Time | Time required by the algorithm to find a route |

### Time Complexity

Let:
- `V` = Number of vertices (buildings).
- `E` = Number of edges (walkways).

| Algorithm | Time Complexity | Space Complexity |
|---|---|---|
| BFS | O(V + E) | O(V) |
| DFS | O(V + E) | O(V) |
| Dijkstra's Algorithm | O((V + E) log V) | O(V) |
| A* Search | O((V + E) log V) in the stated worst-case model | O(V) |

Actual performance depends on graph structure, implementation details, and the heuristic used by A*.

## 🌍 Applications

- Navigation within college campuses and universities.
- Finding routes in hospitals, malls, and office buildings.
- Indoor navigation and location-based services.
- Robot path planning.
- Game AI and graph-based route planning.
- Network routing and graph algorithm analysis.

## ⚠️ Limitations

- The current implementation uses a sample campus map.
- It does not include live GPS tracking or real-time traffic information.
- The map does not model multiple floors or indoor accessibility.
- The graph assumes non-negative edge weights.
- A* requires a suitable heuristic for optimal path-finding.
- Execution times may vary depending on the computer and system load.

## 🔮 Future Enhancements

- Replace the sample graph with actual college campus locations and distances.
- Develop a graphical user interface using Tkinter or a web interface using Flask.
- Visualize the campus graph and highlight the selected route.
- Add interactive maps and GPS integration.
- Support multi-floor indoor navigation.
- Include accessible routes for users with mobility requirements.
- Add bidirectional search and other advanced path-finding algorithms.

## ✅ Conclusion

The Campus Navigation and Path-Finding System demonstrates how graph-based algorithms can solve practical route-planning problems. By implementing BFS, DFS, Dijkstra's Algorithm, and A*, the project compares different approaches to searching for routes between campus locations.

The comparison highlights the difference between finding a path with fewer edges and finding a path with the minimum total distance. Dijkstra's Algorithm and A* are particularly suitable for weighted shortest-path problems, while A* can reduce the search effort when an effective heuristic is available.

Overall, the project provides a practical demonstration of graph representation, path-finding algorithms, complexity analysis, and performance evaluation in the field of Design and Analysis of Algorithms.

## 👨‍🎓 Academic Information

- **Project Title:** Campus Navigation and Path-Finding System
- **Subject:** Design and Analysis of Algorithms (DAA)
- **Programming Language:** Python 3
- **Institution:** A. D. Patel Institute of Technology (ADIT), CVM University
