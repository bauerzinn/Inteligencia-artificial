import random

# ----- Parâmetros do problema -----
ITENS = [(10, 60), (20, 100), (30, 120), (5, 40), (15, 80)]  # (peso, valor)
CAPACIDADE = 50
TAMANHO_POP = 30
GERACOES = 100

# ----- Funções do AG -----
def inicializar_populacao(heuristica=False):
    pop = []
    for _ in range(TAMANHO_POP):
        if heuristica:
            individuo = heuristica_inicial()
        else:
            individuo = [random.randint(0, 1) for _ in ITENS]
        pop.append(individuo)
    return pop

def heuristica_inicial():
    itens_ordenados = sorted(enumerate(ITENS), key=lambda x: x[1][1]/x[1][0], reverse=True)
    individuo = [0] * len(ITENS)
    peso_total = 0
    for idx, (peso, _) in itens_ordenados:
        if peso_total + peso <= CAPACIDADE:
            individuo[idx] = 1
            peso_total += peso
    return individuo

def fitness(individuo):
    peso = sum(gene * ITENS[i][0] for i, gene in enumerate(individuo))
    valor = sum(gene * ITENS[i][1] for i, gene in enumerate(individuo))
    return valor if peso <= CAPACIDADE else 0

def selecao_roleta(pop, aptidoes):
    total = sum(aptidoes)
    pick = random.uniform(0, total)
    atual = 0
    for i, apt in enumerate(aptidoes):
        atual += apt
        if atual > pick:
            return pop[i]

def crossover(pai1, pai2, tipo='um_ponto'):
    if tipo == 'um_ponto':
        ponto = random.randint(1, len(pai1) - 1)
        return pai1[:ponto] + pai2[ponto:]
    elif tipo == 'dois_pontos':
        p1, p2 = sorted(random.sample(range(len(pai1)), 2))
        return pai1[:p1] + pai2[p1:p2] + pai1[p2:]
    elif tipo == 'uniforme':
        return [pai1[i] if random.random() > 0.5 else pai2[i] for i in range(len(pai1))]

def mutacao(individuo, taxa):
    return [gene if random.random() > taxa else 1 - gene for gene in individuo]

# ----- Loop principal do AG -----
def algoritmo_genetico(config):
    pop = inicializar_populacao(heuristica=config['heuristica'])
    melhor_solucao = None
    melhor_aptidao = 0

    for gen in range(GERACOES):
        aptidoes = [fitness(ind) for ind in pop]
        nova_pop = []

        for _ in range(TAMANHO_POP):
            pai1 = selecao_roleta(pop, aptidoes)
            pai2 = selecao_roleta(pop, aptidoes)
            filho = crossover(pai1, pai2, tipo=config['crossover'])
            filho = mutacao(filho, config['mutacao'])
            nova_pop.append(filho)

        pop = nova_pop
        melhor_gen = max(pop, key=fitness)
        if fitness(melhor_gen) > melhor_aptidao:
            melhor_solucao = melhor_gen
            melhor_aptidao = fitness(melhor_gen)

    return melhor_solucao, melhor_aptidao

# ----- Testes -----
if __name__ == "__main__":
    configuracoes = [
        {'crossover': 'um_ponto', 'mutacao': 0.01, 'heuristica': False},
        {'crossover': 'dois_pontos', 'mutacao': 0.05, 'heuristica': False},
        {'crossover': 'uniforme', 'mutacao': 0.10, 'heuristica': True},
    ]

    for i, config in enumerate(configuracoes):
        melhor, apt = algoritmo_genetico(config)
        print(f"Configuração {i+1}: {config}")
        print(f"Melhor aptidão: {apt}, Solução: {melhor}")
        print("-" * 40)
