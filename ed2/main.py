from queue import Queue, LifoQueue, PriorityQueue
import time

# Labirinto baseado na imagem enviada
labirinto = [
    ['S', 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
    [0  , 0 , 1 , 0 , 0 , 0 , 1 , 0 , 0 , 1 ],
    [1  , 0 , 1 , 1 , 1 , 0 , 1 , 0 , 1 , 1 ],
    [1  , 0 , 0 , 0 , 1 , 0 , 0 , 0 , 1 , 1 ],
    [1  , 1 , 1 , 0 , 1 , 1 , 1 , 0 , 0 , 1 ],
    [1  , 0 , 0 , 0 , 0 , 1 , 0 , 0 , 1 , 1 ],
    [1  , 0 , 1 , 1 , 0 , 1 , 1 , 0 , 1 , 1 ],
    [1  , 0 , 1 , 0 , 0 , 0 , 1 , 0 , 0 , 1 ],
    [1  , 0 , 1 , 0 , 1 , 0 , 1 , 1 , 0 , 'E'],
    [1  , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ]
]

# Conversão para números: 'S' = 0, 'E' = 0
start = (0, 0)
end = (8, 9)
labirinto[start[0]][start[1]] = 0
labirinto[end[0]][end[1]] = 0

# Heurística de Manhattan
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Vizinhos válidos
def vizinhos(pos, lab):
    direcoes = [(-1,0), (1,0), (0,-1), (0,1)]
    result = []
    for dx, dy in direcoes:
        x, y = pos[0] + dx, pos[1] + dy
        if 0 <= x < len(lab) and 0 <= y < len(lab[0]) and lab[x][y] == 0:
            result.append((x, y))
    print(f"Posição atual: {pos}, Vizinhos encontrados: {result}")  # Debug
    return result

# Caminho reverso
def reconstruir(caminho, atual):
    trajeto = []
    while atual in caminho:
        trajeto.append(atual)
        atual = caminho[atual]
    trajeto.append(start)
    trajeto.reverse()
    return trajeto

# BFS
def bfs(lab, inicio, fim):
    fila = Queue()
    fila.put(inicio)
    caminho = {}
    visitados = set()
    visitados.add(inicio)
    while not fila.empty():
        atual = fila.get()
        if atual == fim:
            return reconstruir(caminho, fim), len(visitados)
        for viz in vizinhos(atual, lab):
            if viz not in visitados:
                visitados.add(viz)
                caminho[viz] = atual
                fila.put(viz)
    return [], len(visitados)

# DFS
def dfs(lab, inicio, fim):
    pilha = LifoQueue()
    pilha.put(inicio)
    caminho = {}
    visitados = set()
    visitados.add(inicio)
    while not pilha.empty():
        atual = pilha.get()
        if atual == fim:
            return reconstruir(caminho, fim), len(visitados)
        for viz in vizinhos(atual, lab):
            if viz not in visitados:
                visitados.add(viz)
                caminho[viz] = atual
                pilha.put(viz)
    return [], len(visitados)

# Gulosa
def gulosa(lab, inicio, fim):
    fila = PriorityQueue()
    fila.put((heuristica(inicio, fim), inicio))
    caminho = {}
    visitados = set()
    while not fila.empty():
        _, atual = fila.get()
        if atual == fim:
            return reconstruir(caminho, fim), len(visitados)
        if atual in visitados:
            continue
        visitados.add(atual)
        for viz in vizinhos(atual, lab):
            if viz not in visitados:
                caminho[viz] = atual
                fila.put((heuristica(viz, fim), viz))
    return [], len(visitados)

# A*
def a_estrela(lab, inicio, fim):
    fila = PriorityQueue()
    fila.put((0, inicio))
    caminho = {}
    custo = {inicio: 0}
    visitados = set()
    while not fila.empty():
        _, atual = fila.get()
        if atual == fim:
            return reconstruir(caminho, fim), len(visitados)
        if atual in visitados:
            continue
        visitados.add(atual)
        for viz in vizinhos(atual, lab):
            novo_custo = custo[atual] + 1
            if viz not in custo or novo_custo < custo[viz]:
                custo[viz] = novo_custo
                prioridade = novo_custo + heuristica(viz, fim)
                fila.put((prioridade, viz))
                caminho[viz] = atual
    return [], len(visitados)

def visualizar_caminho(lab, caminho):
    # Criar uma cópia do labirinto para não modificar o original
    visual = []
    for linha in lab:
        nova_linha = []
        for cel in linha:
            nova_linha.append(str(cel))  # Converter para string
        visual.append(nova_linha)
    
    # Marcar o caminho com '*'
    for x, y in caminho:
        if (x, y) != start and (x, y) != end:
            visual[x][y] = '*'
    
    # Colocar 'S' e 'E' de volta
    visual[start[0]][start[1]] = 'S'
    visual[end[0]][end[1]] = 'E'
    
    # Imprimir o labirinto
    print("Visualização do caminho:")
    for linha in visual:
        for cel in linha:
            if cel == '1':  # Agora comparamos com string
                print('█', end=' ')  # parede
            elif cel == '*':
                print('*', end=' ')  # caminho
            elif cel == 'S':
                print('S', end=' ')  # início
            elif cel == 'E':
                print('E', end=' ')  # fim
            else:
                print(' ', end=' ')  # espaço vazio
        print()
    print()

def testar_algoritmo(nome, funcao):
    print(f"\n{'-'*50}")
    print(f"Testando {nome}")
    print(f"Ponto inicial: {start}")
    print(f"Ponto final: {end}")
    
    inicio_tempo = time.time()
    caminho, visitados = funcao(labirinto, start, end)
    fim_tempo = time.time()
    
    print(f"\n{nome}:")
    print(f"  -> Nós visitados: {visitados}")
    print(f"  -> Tempo: {fim_tempo - inicio_tempo:.6f} segundos")
    print(f"  -> Caminho encontrado: {caminho}")  # Debug
    print(f"\nEstado do labirinto no final:")
    for linha in labirinto:
        print(linha)
    visualizar_caminho(labirinto, caminho)

# Executar testes
testar_algoritmo("Busca em Largura (BFS)", bfs)
testar_algoritmo("Busca em Profundidade (DFS)", dfs)
testar_algoritmo("Busca Gulosa", gulosa)
testar_algoritmo("Algoritmo A*", a_estrela)