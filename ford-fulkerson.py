from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
        self.graph[v][u] = 0

    def ford_fulkerson(self, source, sink):
        def bfs(s, t, parent):
            visited = [False] * len(self.graph)
            queue = []
            queue.append(s)
            visited[s] = True

            while queue:
                u = queue.pop(0)
                for v, capacity in self.graph[u].items():
                    if visited[v] == False and capacity > 0:
                        queue.append(v)
                        visited[v] = True
                        parent[v] = u
            return visited[t]

        parent = [-1] * len(self.graph)
        max_flow = 0

        while bfs(source, sink, parent):
            path_flow = float("inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow

def read_graph_from_file(file_name):
    with open(file_name, 'r') as file:
        V = int(file.readline())
        A = int(file.readline())
        graph = Graph()
        for _ in range(A):
            u, v, capacity = map(float, file.readline().split())
            graph.add_edge(int(u), int(v), capacity)
        return graph

def export_max_flow_graph(graph, max_flow, output_file):
    with open(output_file, 'w') as file:
        for u in graph.graph:
            for v, capacity in graph.graph[u].items():
                file.write(f"{u} {v} {capacity}\n")

if __name__ == "__main__":
    file_name = "graph.txt"  # Substitua pelo nome do seu arquivo
    graph = read_graph_from_file(file_name)
    source = int(input("Digite o vértice fonte: "))
    sink = int(input("Digite o vértice sorvedouro: "))
    max_flow = graph.ford_fulkerson(source, sink)
    export_max_flow_graph(graph, max_flow, 'saida.txt')
    print(f"\nMax Flow: {max_flow}")
