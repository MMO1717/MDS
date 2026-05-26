"""
Interactive BFS Demonstration
============================

This script demonstrates breadth‑first search (BFS) on a simple
undirected graph using an adjacency matrix.  It mirrors the structure
of the C code presented in the user’s question and prints an
explanation at each step.  The goal is to help you understand what
each line in the BFS algorithm does.

How to Use
----------

Run this script from a terminal.  When prompted, press Enter to
advance through the algorithm.  Each prompt corresponds to a line or
operation in the original C function.  After running, you will see
how the queue and visited arrays change over the course of the BFS.

Graph Example
-------------

The example graph used here contains five vertices labelled ‘A’
through ‘E’.  The adjacency matrix for the graph is defined as

```
    A  B  C  D  E
A [ 0, 1, 1, 0, 0 ]
B [ 1, 0, 0, 1, 1 ]
C [ 1, 0, 0, 0, 0 ]
D [ 0, 1, 0, 0, 0 ]
E [ 0, 1, 0, 0, 0 ]
```

Vertices `A` and `B` are connected, `A` and `C` are connected,
`B` connects to `D` and `E`, and so on.  BFS starts at vertex `A`.

Copyright © 2025
"""

from collections import deque


def bfs_explanation():
    """Perform BFS on a simple graph while explaining each step."""
    # Define vertices and their labels.  In C this would be part of the
    # `MGraph` structure (the list of vertex names isn't always
    # necessary but it helps humans follow along).
    vertices = ["A", "B", "C", "D", "E"]
    # Adjacency matrix representing the graph.  If G.arcs[u][w].adj == 1
    # then there is an edge between u and w.
    adjacency = [
        [0, 1, 1, 0, 0],  # A connects to B and C
        [1, 0, 0, 1, 1],  # B connects to A, D, and E
        [1, 0, 0, 0, 0],  # C connects to A
        [0, 1, 0, 0, 0],  # D connects to B
        [0, 1, 0, 0, 0],  # E connects to B
    ]
    num_vertices = len(vertices)

    # visited array: corresponds to `visited` in the C code.  It keeps
    # track of which vertices have been processed.  Initialize all to 0.
    visited = [0] * num_vertices

    # Use deque from Python's collections as the queue.  This mirrors
    # `Queue Q = initQueue();` in C.  The BFS algorithm uses a queue
    # (FIFO) to process vertices in the order they are discovered.
    queue = deque()

    print("Breadth–First Search Demonstration")
    print("----------------------------------\n")
    # Explain variable declarations
    print("1. Declare variables u and w (used for current and adjacent vertices).")
    print("2. Initialize the queue.")
    print("3. Choose a starting vertex (i = 0, which corresponds to {} in this example).".format(vertices[0]))
    input("\nPress Enter to mark the starting vertex as visited...")

    # Start BFS from vertex 0 ('A').  Mark it as visited and enqueue it.
    i = 0
    visited[i] = 1  # corresponds to `visited[i] = 1;` in C
    print(f"Mark vertex {vertices[i]} as visited. visited = {visited}")
    queue.append(i)  # corresponds to `EnQueue(&Q, i);`
    print(f"Enqueue starting vertex {vertices[i]}. Queue = {[vertices[x] for x in queue]}")

    # Enter the main loop: keep processing until the queue is empty.
    step_count = 1
    while queue:
        input("\nPress Enter to dequeue the next vertex...")
        # Dequeue: remove the front of the queue and assign it to u
        u = queue.popleft()  # corresponds to `DeQueue(&Q, &u);`
        print(f"Step {step_count}: Dequeue vertex {vertices[u]}. Queue = {[vertices[x] for x in queue]}")
        step_count += 1
        # Visit all adjacent vertices
        for w in range(num_vertices):
            # Check if there is an edge from u to w and if w has not been visited
            if visited[w] == 0 and adjacency[u][w] == 1:
                print(
                    f"  Vertex {vertices[w]} is adjacent to {vertices[u]} and not visited "
                    f"(visited[{w}] == 0 and adjacency[{u}][{w}] == 1)."
                )
                # Mark the vertex as visited
                visited[w] = 1  # corresponds to `visited[w] = 1;`
                print(
                    f"  Mark {vertices[w]} as visited. visited = {visited}"
                )
                # Enqueue the vertex
                queue.append(w)  # corresponds to `EnQueue(&Q, w);`
                print(
                    f"  Enqueue vertex {vertices[w]}. Queue = {[vertices[x] for x in queue]}"
                )

    print("\nBFS complete. All reachable vertices have been visited.")


if __name__ == "__main__":
    bfs_explanation()
