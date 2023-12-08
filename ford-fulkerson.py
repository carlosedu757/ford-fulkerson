from collections import defaultdict
from collections import deque

inf = float('inf')

def bfsAug(G, H, s, t, f):
	P, Q, F = {s: None}, deque([s]), {s: inf}	# Árvore, fila, rótulo de fluxo
	def label(inc):								# Aumento de fluxo em vindo de u?
		if v in P or inc <= 0: return 			# Visto? Inalcançável? Ignorar
		F[v], P[v] = min(F[u], inc), u 			# Fluxo máximo aqui? De onde?
		Q.append(v)								# Descoberto -- visitar depois
	while Q:									# Descoberto, não visitado
		u = Q.popleft()							# Pegar um (FIFO)
		if u == t: return P, F[t]				# Chegou em t? Caminho de aumento!
		try:
			for v in G[u]: label(G[u][v] - f[u,v])	# Rótulo ao longo das arestas de saída
			for v in H[u]: label(f[v,u])			# Rótulo ao longo das arestas de entrada
		except Exception as e:
			raise e
	return None, 0	

def fordFulkerson(G, s, t, aug=bfsAug):	# Fluxo máximo de s para t
	H, f = tr(G), defaultdict(int)			# Transposta e fluxo
	while True:								# Enquanto pudermos melhorar as coisas
		P, c = aug(G, H, s, t, f)			# Caminho de aumento e capacidade/folga
		#print('p', P, 'c', c)
		if c == 0: return f 				# Nenhum caminho de aumento encontrado? Feito!
		u = t 								# Começar o aumento
		while u != s:						# Retroceder até s
			u, v = P[u], u 					# Avançar um passo
			if v in G[u]:	f[u,v] += c 	# Aresta direta? Adicionar folga
			else:			f[v,u] -= c 	# Aresta inversa? Cancelar folga
			
def tr(G):						# Transposta (arestas reversas de) G
	GT = {}
	for u in G: GT[u] = set()	# Pegar todos os nós lá
	for u in G:
		for v in G[u]:
			GT[v].add(u)		# Adicionar todas as arestas reversas
	return GT
	
def ler_grafo_de_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        linhas = file.readlines()

        num_vertices = int(linhas[0])
        num_arcos = int(linhas[1])

        grafo = {str(i): {} for i in range(num_vertices)}

        for linha in linhas[2:]:
            origem, destino, capacidade = linha.split()
            origem, destino = int(origem), int(destino)
            capacidade = float(capacidade)

            grafo[str(origem)][str(destino)] = capacidade

        return grafo	

if __name__ == "__main__": 
    grafo = ler_grafo_de_arquivo('arcos.txt')
    
    fonte = input("Digite o nó de origem (fonte): ")
    sorvedouro = input("Digite o nó de destino (sorvedouro): ")
    
    fluxo_maximo = fordFulkerson(grafo, fonte, sorvedouro)
    
    valor_maximo = 0
    with open('saida.txt', 'w') as f:
    	for chave, valor in fluxo_maximo.items():
    		string = str(chave) + ' ' + str(valor) + '\n'
    		f.write(string)
    		if((str(chave)[7] == sorvedouro)):
        		valor_maximo += valor
    
    print('Fluxo Total do Grafo:', valor_maximo)
