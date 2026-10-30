INF = float('inf')

def floyd_warshall(graph):
    n = len(graph)
    dist = [row[:] for row in graph]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(
                    dist[i][j],
                    dist[i][k] + dist[k][j]
                )

    return dist

if __name__ == "__main__":
    graph = [
        [0, 3, INF, 5],
        [2, 0, INF, 4],
        [INF, 1, 0, INF],
        [INF, INF, 2, 0]
    ]

    shortest_paths = floyd_warshall(graph)

    print("Shortest Distance Matrix:")
    for row in shortest_paths:
        print([
            "INF" if val == INF else int(val)
            for val in row
        ])
