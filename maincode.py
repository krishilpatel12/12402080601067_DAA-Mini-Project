"""
=====================================================================
 CAMPUS NAVIGATION AND PATH-FINDING SYSTEM  (DAA Mini Project)
 Complete single-file code
=====================================================================
 What this program does:
   1. Builds a campus map as a weighted graph (locations + roads).
   2. Finds a route using 4 algorithms: BFS, DFS, Dijkstra, A*.
   3. Compares them (path length, nodes explored, time).
   4. Benchmarks them on bigger graphs (10, 50, 100, 500 nodes).
   5. Shows LIVE graphs in pop-up windows (nothing needs to be saved):
        - animated search on the campus map (watch the algorithm explore)
        - final routes of all 4 algorithms side by side
        - performance graphs (input size vs time, nodes explored)
      You choose which graphs to see; the program ALWAYS ends with the
      shortest-path graph.

 How to run:
   Step 1 (only once):   pip install matplotlib numpy
   Step 2:               python campus_navigation_complete.py
   Then type a source and destination when asked (or press Enter
   to use the defaults: Main Gate -> Hostel B).
 Close each graph window to move to the next one.
 (Tip: take your project screenshots directly from these windows.)
=====================================================================
"""

import heapq            # priority queue (min-heap) for Dijkstra and A*
import math             # square root / distance formula
import random           # random graphs for benchmarking
import time             # to measure execution time
from collections import deque   # queue for BFS

import matplotlib
# (No matplotlib.use("Agg") here: we WANT windows to open for live graphs)
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------
# PART 1: CAMPUS DATA  (nodes = locations, edges = walkways)
# ---------------------------------------------------------------------
# Each location has (x, y) coordinates in metres. A* uses these to
# estimate the remaining distance (heuristic).
LOCATIONS = {
    "Main Gate": (0, 0),        "Admin Block": (120, 40),
    "Library": (250, 60),       "CS Dept": (260, 200),
    "Auditorium": (130, 170),   "Canteen": (380, 90),
    "Hostel A": (520, 60),      "Hostel B": (540, 210),
    "Sports Ground": (400, 300), "Labs": (150, 310),
    "Medical Centre": (40, 230), "Parking": (30, 110),
}

# Walkways between locations (they work in both directions).
ROADS = [
    ("Main Gate", "Parking"), ("Main Gate", "Admin Block"),
    ("Parking", "Admin Block"), ("Parking", "Medical Centre"),
    ("Admin Block", "Library"), ("Admin Block", "Auditorium"),
    ("Library", "Canteen"), ("Library", "CS Dept"),
    ("Auditorium", "CS Dept"), ("Auditorium", "Labs"),
    ("Medical Centre", "Auditorium"), ("Medical Centre", "Labs"),
    ("CS Dept", "Labs"), ("CS Dept", "Sports Ground"),
    ("Canteen", "Hostel A"), ("Canteen", "Hostel B"),
    ("Hostel A", "Hostel B"), ("Hostel B", "Sports Ground"),
    ("Canteen", "CS Dept"),
]


def distance(a, b, pos):
    """Straight-line (Euclidean) distance between two nodes."""
    return math.hypot(pos[a][0] - pos[b][0], pos[a][1] - pos[b][1])


def build_graph(locations=LOCATIONS, roads=ROADS):
    """Graph representation: ADJACENCY LIST.
    graph[node] = [(neighbour, weight), ...]   -> space O(V + E)
    The weight of a road is its length in metres."""
    graph = {node: [] for node in locations}
    for a, b in roads:
        w = round(distance(a, b, locations), 1)
        graph[a].append((b, w))     # a -> b
        graph[b].append((a, w))     # b -> a (two-way road)
    return graph


def random_graph(n, seed=1):
    """Create a random CONNECTED graph with n nodes (used for benchmarking)."""
    rnd = random.Random(seed)       # fixed seed = same graph every run
    pos = {i: (rnd.uniform(0, 1000), rnd.uniform(0, 1000)) for i in range(n)}
    graph = {i: [] for i in range(n)}

    def add_edge(a, b):
        if all(v != b for v, _ in graph[a]):        # avoid duplicate roads
            w = distance(a, b, pos)
            graph[a].append((b, w))
            graph[b].append((a, w))

    # Connect every new node to its nearest earlier node (graph stays connected)
    for i in range(1, n):
        nearest = min(range(i), key=lambda j: distance(i, j, pos))
        add_edge(i, nearest)
    # Add a few extra roads to the 3 nearest neighbours of every node
    for i in range(n):
        for j in sorted(range(n), key=lambda j: distance(i, j, pos))[1:4]:
            add_edge(i, j)
    return graph, pos


def rebuild_path(parent, target):
    """Walk backwards through the 'parent' map to get the final path."""
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]               # reverse: source -> target


def path_cost(graph, path):
    """Total length of a path (sum of edge weights)."""
    total = 0
    for a, b in zip(path, path[1:]):
        total += next(w for v, w in graph[a] if v == b)
    return round(total, 1)


# ---------------------------------------------------------------------
# PART 2: THE FOUR ALGORITHMS
# Each returns (path, explored_order)
#   path           = list of nodes from source to target
#   explored_order = nodes visited, in order (shows search effort)
# ---------------------------------------------------------------------
def bfs(graph, src, dst):
    """BFS - explores level by level using a QUEUE.
    Finds the path with the FEWEST roads (ignores road length).
    Time O(V+E), Space O(V)."""
    parent = {src: None}
    queue = deque([src])
    explored = []
    while queue:
        u = queue.popleft()                 # take oldest node
        explored.append(u)
        if u == dst:
            return rebuild_path(parent, dst), explored
        for v, _ in graph[u]:
            if v not in parent:             # not visited yet
                parent[v] = u
                queue.append(v)
    return None, explored


def dfs(graph, src, dst):
    """DFS - goes as deep as possible first using a STACK.
    Finds A path (often long, NOT the shortest).
    Time O(V+E), Space O(V)."""
    parent = {src: None}
    stack = [src]
    visited = set()
    explored = []
    while stack:
        u = stack.pop()                     # take newest node
        if u in visited:
            continue
        visited.add(u)
        explored.append(u)
        if u == dst:
            return rebuild_path(parent, dst), explored
        for v, _ in graph[u]:
            if v not in visited:
                parent[v] = u
                stack.append(v)
    return None, explored


def dijkstra(graph, src, dst):
    """Dijkstra - always expands the node with the SMALLEST distance
    so far (min-heap). Gives the SHORTEST path (weights >= 0).
    Time O((V+E) log V), Space O(V)."""
    best = {n: math.inf for n in graph}     # best known distance to each node
    best[src] = 0
    parent = {src: None}
    heap = [(0, src)]                       # (distance so far, node)
    done = set()
    explored = []
    while heap:
        d, u = heapq.heappop(heap)          # closest unfinished node
        if u in done:
            continue
        done.add(u)
        explored.append(u)
        if u == dst:
            return rebuild_path(parent, dst), explored
        for v, w in graph[u]:
            if d + w < best[v]:             # found a shorter way to v
                best[v] = d + w
                parent[v] = u
                heapq.heappush(heap, (best[v], v))
    return None, explored


def astar(graph, src, dst, pos):
    """A* - like Dijkstra but ranks nodes by  f = g + h
       g = distance travelled so far
       h = straight-line distance to the destination (heuristic)
    The heuristic guides the search toward the goal, so fewer nodes
    are explored. Still optimal because h never over-estimates.
    Time O((V+E) log V) worst case, usually much faster."""
    h = lambda n: distance(n, dst, pos)
    g = {n: math.inf for n in graph}
    g[src] = 0
    parent = {src: None}
    heap = [(h(src), src)]                  # (f value, node)
    done = set()
    explored = []
    while heap:
        _, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        explored.append(u)
        if u == dst:
            return rebuild_path(parent, dst), explored
        for v, w in graph[u]:
            if g[u] + w < g[v]:
                g[v] = g[u] + w
                parent[v] = u
                heapq.heappush(heap, (g[v] + h(v), v))
    return None, explored


def algorithm_table(graph, src, dst, pos):
    """Return the 4 algorithms as ready-to-call functions."""
    return {
        "BFS": lambda: bfs(graph, src, dst),
        "DFS": lambda: dfs(graph, src, dst),
        "Dijkstra": lambda: dijkstra(graph, src, dst),
        "A*": lambda: astar(graph, src, dst, pos),
    }


# ---------------------------------------------------------------------
# PART 3: RUN ALL ALGORITHMS ON ONE QUERY AND MEASURE THEM
# ---------------------------------------------------------------------
def run_all(graph, src, dst, pos):
    results = {}
    for name, run in algorithm_table(graph, src, dst, pos).items():
        t0 = time.perf_counter()
        path, explored = run()
        ms = (time.perf_counter() - t0) * 1000      # time in milliseconds
        results[name] = {"path": path, "explored": explored, "ms": ms,
                         "cost": path_cost(graph, path)}
    return results


def benchmark(sizes=(10, 50, 100, 500), repeats=200):
    """Input size vs execution time. Each algorithm runs `repeats` times
    and the average is taken, because one run is too fast to measure."""
    table = {}
    for n in sizes:
        graph, pos = random_graph(n)
        src, dst = 0, n - 1
        table[n] = {}
        for name, run in algorithm_table(graph, src, dst, pos).items():
            t0 = time.perf_counter()
            for _ in range(repeats):
                path, explored = run()
            avg_ms = (time.perf_counter() - t0) * 1000 / repeats
            table[n][name] = {"ms": avg_ms, "explored": len(explored),
                              "cost": path_cost(graph, path)}
    return table


# ---------------------------------------------------------------------
# PART 4: LIVE GRAPHS (windows open while the program runs)
# ---------------------------------------------------------------------
NAMES = ("BFS", "DFS", "Dijkstra", "A*")


def draw_map(ax, path=None, explored=None, title="", src=None, dst=None):
    """Draw the campus map on a given axes.
    grey lines = roads | dark dots = locations | orange dots = explored
    teal line = final path | green = source | red = destination"""
    ax.clear()
    for a, b in ROADS:
        ax.plot(*zip(LOCATIONS[a], LOCATIONS[b]), color="#c5ccd6", lw=1.5, zorder=1)
    for name, (x, y) in LOCATIONS.items():
        color = "#1B3A4B"
        if explored and name in explored:
            color = "#f4a261"
        if name == src:
            color = "#2a9d4a"
        if name == dst:
            color = "#d62828"
        ax.scatter(x, y, s=90, color=color, zorder=3)
        ax.text(x + 8, y + 10, name, fontsize=7)
    if path:
        ax.plot(*zip(*[LOCATIONS[n] for n in path]), color="#0E9AA7", lw=4, zorder=2)
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.invert_yaxis()                       # y grows downward like a map
    ax.axis("off")


def live_search(name, result, src, dst, delay=0.5):
    """WINDOW 1: animate the search. Each step turns the next explored
    location orange, then the final shortest path is drawn in teal."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.canvas.manager.set_window_title(f"Live search: {name}")
    seen = []
    for node in result["explored"]:
        seen.append(node)
        draw_map(ax, None, seen, f"{name} is searching...  explored {len(seen)} node(s): {node}", src, dst)
        plt.pause(delay)                    # pause so we can SEE each step
    draw_map(ax, result["path"], seen,
             f"{name} finished: {result['cost']} m, explored {len(seen)} nodes", src, dst)
    print(f"\n[Window open] {name} animation finished. Close the window to continue.")
    plt.show()                              # keep window open until closed


def compare_routes(results, src, dst):
    """WINDOW 2: the 4 algorithms side by side (path + nodes explored)."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.canvas.manager.set_window_title("Route comparison")
    for ax, name in zip(axes.flat, NAMES):
        r = results[name]
        draw_map(ax, r["path"], r["explored"],
                 f"{name}: {r['cost']} m, explored {len(r['explored'])}", src, dst)
    fig.suptitle(f"{src} to {dst}  (green=start, red=goal, orange=explored, teal=path)")
    fig.tight_layout()
    print("[Window open] Route comparison. Close the window to continue.")
    plt.show()


def performance_graphs(bench):
    """WINDOW 3: input size vs time, and nodes explored vs input size."""
    sizes = list(bench)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.canvas.manager.set_window_title("Performance")
    for k in NAMES:
        axes[0].plot(sizes, [bench[n][k]["ms"] for n in sizes], marker="o", label=k)
    axes[0].set(xlabel="Number of nodes", ylabel="Average time (ms)",
                title="Input size vs execution time")
    axes[0].legend(); axes[0].grid(alpha=0.3)
    w = 0.2
    for i, k in enumerate(NAMES):
        axes[1].bar(np.arange(len(sizes)) + i * w, [bench[n][k]["explored"] for n in sizes], w, label=k)
    axes[1].set_xticks(np.arange(len(sizes)) + 0.3); axes[1].set_xticklabels(sizes)
    axes[1].set(xlabel="Number of nodes", ylabel="Nodes explored", title="Search effort")
    axes[1].legend()
    fig.tight_layout()
    print("[Window open] Performance graphs. Close the window to continue.")
    plt.show()


def shortest_path_graph(graph, results, src, dst):
    """FINAL WINDOW: the shortest path on the campus map, with the distance
    of every road on the route and the total. Dijkstra and A* both give the
    optimal path, so we use A* (and confirm it matches Dijkstra)."""
    best = results["A*"]
    assert best["cost"] == results["Dijkstra"]["cost"]      # both optimal
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.canvas.manager.set_window_title("Shortest path")
    draw_map(ax, best["path"], None,
             f"SHORTEST PATH: {src} to {dst}  |  Total = {best['cost']} m", src, dst)
    # Write the length of each road on the route, halfway along it.
    for a, b in zip(best["path"], best["path"][1:]):
        w = next(w for v, w in graph[a] if v == b)
        mx = (LOCATIONS[a][0] + LOCATIONS[b][0]) / 2
        my = (LOCATIONS[a][1] + LOCATIONS[b][1]) / 2
        ax.text(mx, my, f"{w:.0f} m", fontsize=8, color="#0E9AA7", fontweight="bold",
                bbox=dict(facecolor="white", edgecolor="none", pad=1))
    fig.tight_layout()
    print("\n[Window open] Shortest path: " + " -> ".join(best["path"]))
    plt.show()


# ---------------------------------------------------------------------
# PART 5: MAIN PROGRAM
# ---------------------------------------------------------------------
def main():
    graph = build_graph()
    print("Campus locations:", ", ".join(LOCATIONS))
    src = input("Enter source      [Main Gate]: ").strip() or "Main Gate"
    dst = input("Enter destination [Hostel B] : ").strip() or "Hostel B"
    if src not in LOCATIONS or dst not in LOCATIONS:
        print("Unknown location. Type names exactly as listed above.")
        return

    # Run all four algorithms and print the comparison table.
    results = run_all(graph, src, dst, LOCATIONS)
    print(f"\nRoute from {src} to {dst}")
    print("-" * 70)
    for name, r in results.items():
        print(f"{name:9s} distance = {r['cost']:7.1f} m | nodes explored = "
              f"{len(r['explored']):2d} | time = {r['ms']:.4f} ms")
        print("          path:", " -> ".join(r["path"]))

    # Benchmark on bigger graphs.
    print("\nBenchmark: average time in ms (200 runs each)")
    print(f"{'Nodes':>6} {'BFS':>8} {'DFS':>8} {'Dijkstra':>9} {'A*':>8}")
    bench = benchmark()
    for n, row in bench.items():
        print(f"{n:>6} {row['BFS']['ms']:8.3f} {row['DFS']['ms']:8.3f} "
              f"{row['Dijkstra']['ms']:9.3f} {row['A*']['ms']:8.3f}")

    # ---- Ask which graph(s) the user wants to see ----
    print("\nWhich graph do you want to see?")
    print("  1 = Live search animation (one algorithm)")
    print("  2 = Route comparison (all 4 algorithms)")
    print("  3 = Performance graphs (time and nodes explored)")
    print("  4 = ALL graphs")
    print("  0 = Skip (only show the shortest path)")
    choice = input("Enter choice(s), e.g. 1 or 1,3 or 4 [4]: ").strip() or "4"
    picks = {c.strip() for c in choice.replace(" ", ",").split(",") if c.strip()}
    if "4" in picks:
        picks = {"1", "2", "3"}

    if "1" in picks:
        algo = input("Algorithm to animate (BFS/DFS/Dijkstra/A*) [A*]: ").strip() or "A*"
        if algo not in NAMES:
            algo = "A*"
        live_search(algo, results[algo], src, dst)
    if "2" in picks:
        compare_routes(results, src, dst)
    if "3" in picks:
        performance_graphs(bench)

    # ---- Always finish with the shortest-path graph ----
    shortest_path_graph(graph, results, src, dst)


if __name__ == "__main__":
    main()

