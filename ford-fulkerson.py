from collections import defaultdict

class Grafo:
    def __init__(self):
        self.grafo = defaultdict(dict)

    def add_edge(self, u, v, capacidade):
        self.grafo[u][v] = capacidade
        self.grafo[v][u] = 0

    def ford_fulkerson(self, fonte, sorvedouro):
        def bfs(s, t, pai):
            visitado = [False] * len(self.grafo)
            fila = []
            fila.append(s)
            visitado[s] = True

            while fila:
                u = fila.pop(0)
                for v, capacidade in self.grafo[u].items():
                    if visitado[v] == False and capacidade > 0:
                        fila.append(v)
                        visitado[v] = True
                        pai[v] = u
            return visitado[t]

        pai = [-1] * len(self.grafo)
        fluxo_max = 0

        while bfs(fonte, sorvedouro, pai):
            caminho_fluxo = float("inf")
            s = sorvedouro
            while s != fonte:
                caminho_fluxo = min(caminho_fluxo, self.grafo[pai[s]][s])
                s = pai[s]

            fluxo_max += caminho_fluxo
            v = sorvedouro
            while v != fonte:
                u = pai[v]
                self.grafo[u][v] -= caminho_fluxo
                self.grafo[v][u] += caminho_fluxo
                v = pai[v]

        return fluxo_max

def read_grafo_from_file(file_name):
    with open(file_name, 'r') as file:
        V = int(file.readline())
        A = int(file.readline())
        grafo = Grafo()
        for _ in range(A):
            u, v, capacidade = map(float, file.readline().split())
            grafo.add_edge(int(u), int(v), capacidade)
        return grafo

def export_fluxo_max_grafo(grafo, fluxo_max, output_file):
    with open(output_file, 'w') as file:
        for u in grafo.grafo:
            for v, capacidade in grafo.grafo[u].items():
                file.write(f"{u} {v} {capacidade}\n")

if __name__ == "__main__":
    file_name = "grafo.txt"  # Substitua pelo nome do seu arquivo
    grafo = read_grafo_from_file(file_name)
    fonte = int(input("Digite o vértice fonte: "))
    sorvedouro = int(input("Digite o vértice sorvedouro: "))
    fluxo_max = grafo.ford_fulkerson(fonte, sorvedouro)
    export_fluxo_max_grafo(grafo, fluxo_max, 'saida.txt')
    print(f"\nMax Flow: {fluxo_max}")
