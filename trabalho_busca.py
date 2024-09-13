#Trabalho Busca

from collections import deque
import time
import matplotlib.pyplot as plt
import random
from heapq import heappush, heappop

class Estoque:
    def __init__(self, pilhas_inicial, pilhas_final):
        self.estado_inicial = pilhas_inicial
        self.estado_final = pilhas_final

    def mover_caixa(self, estado_atual, origem, destino):
        novo_estado = [list(pilha) for pilha in estado_atual]  
        if len(novo_estado[origem]) > 0:
            caixa = novo_estado[origem].pop()
            novo_estado[destino].append(caixa)
            return novo_estado, caixa
        return estado_atual, None

    def busca_em_largura(self):
        fila = deque([(self.estado_inicial, [], [self.estado_inicial])])  
        visitados = set()  
        estados_totais_visitados = 0

        while fila:
            estado_atual, caminho, estados_visitados = fila.popleft()
            estado_tupla = tuple(tuple(pilha) for pilha in estado_atual)  
            estados_totais_visitados += 1

            if estado_atual == self.estado_final:
                return caminho, estados_visitados, estados_totais_visitados  

            if estado_tupla in visitados:
                continue

            visitados.add(estado_tupla)

            for origem in range(3):
                for destino in range(3):
                    if origem != destino:
                        novo_estado, caixa = self.mover_caixa(estado_atual, origem, destino)
                        if caixa is not None:  
                            novo_caminho = caminho + [(origem, destino, caixa)]
                            fila.append((novo_estado, novo_caminho, estados_visitados + [novo_estado]))

        return None, None, estados_totais_visitados 

    def busca_profundidade_limitada(self, limite):
        estados_totais_visitados = 0
        pilha = [(self.estado_inicial, [], 0, [self.estado_inicial])]  
        visitados = set()  

        while pilha:
            estado_atual, caminho, profundidade, estados_visitados = pilha.pop()
            estado_tupla = tuple(tuple(pilha) for pilha in estado_atual)  
            estados_totais_visitados += 1

            if estado_atual == self.estado_final:
                return caminho, estados_visitados, estados_totais_visitados  

            if estado_tupla in visitados or profundidade >= limite:
                continue

            visitados.add(estado_tupla)

            
            for origem in range(3):
                for destino in range(3):
                    if origem != destino:
                        novo_estado, caixa = self.mover_caixa(estado_atual, origem, destino)
                        if caixa is not None:  
                            novo_caminho = caminho + [(origem, destino, caixa)]
                            pilha.append((novo_estado, novo_caminho, profundidade + 1, estados_visitados + [novo_estado]))

        return [], [], estados_totais_visitados 

    def heuristica(self, estado_atual):
        correto = 0
        for pilha_idx, pilha in enumerate(estado_atual):
            for caixa in pilha:
                if caixa in self.estado_final[pilha_idx]:
                    correto += 1
        return len(self.estado_final[0] + self.estado_final[1] + self.estado_final[2]) - correto

    def busca_a_estrela(self):
        fila = []
        heappush(fila, (0 + self.heuristica(self.estado_inicial), self.estado_inicial, [], [self.estado_inicial]))
        visitados = set()  
        estados_totais_visitados = 0

        while fila:
            custo_total, estado_atual, caminho, estados_visitados = heappop(fila)
            estados_totais_visitados += 1

            if estado_atual == self.estado_final:
                return caminho, estados_visitados, estados_totais_visitados  

            estado_tupla = tuple(tuple(pilha) for pilha in estado_atual)  

            if estado_tupla in visitados:
                continue

            visitados.add(estado_tupla)

            for origem in range(3):
                for destino in range(3):
                    if origem != destino:
                        novo_estado, caixa = self.mover_caixa(estado_atual, origem, destino)
                        if caixa is not None: 
                            novo_caminho = caminho + [(origem, destino, caixa)]
                            custo = len(novo_caminho)  
                            heuristica = self.heuristica(novo_estado)
                            custo_total_novo = custo + heuristica
                            heappush(fila, (custo_total_novo, novo_estado, novo_caminho, estados_visitados + [novo_estado]))

    def busca_profundidade_normal(self):

        pilha = [(self.estado_inicial, [], 0, [self.estado_inicial])] 
        visitados = set()  
        estados_totais_visitados = 0

        while pilha:
            estado_atual, caminho, profundidade, estados_visitados = pilha.pop()
            estado_tupla = tuple(tuple(pilha) for pilha in estado_atual)  
            estados_totais_visitados += 1

            if estado_atual == self.estado_final:
                return caminho, estados_visitados, estados_totais_visitados  

            if estado_tupla in visitados:
                continue

            visitados.add(estado_tupla)

            for origem in range(3):
                for destino in range(3):
                    if origem != destino:
                        novo_estado, caixa = self.mover_caixa(estado_atual, origem, destino)
                        if caixa is not None:  
                            novo_caminho = caminho + [(origem, destino, caixa)]
                            pilha.append((novo_estado, novo_caminho, profundidade + 1, estados_visitados + [novo_estado]))

def criar_casos_aleatorios(num_caixas):
    num_pilhas = 3

    caixas = [chr(i) for i in range(97, 97 + num_caixas)] 

    caixas_iniciais = caixas[:]
    random.shuffle(caixas_iniciais)

    caixas_finais = caixas[:]
    random.shuffle(caixas_finais)

    pilhas_inicial = [[] for _ in range(num_pilhas)]
    pilhas_final = [[] for _ in range(num_pilhas)]

    for caixa in caixas_iniciais:
        pilhas_inicial[random.randint(0, num_pilhas - 1)].append(caixa)

    for caixa in caixas_finais:
        pilhas_final[random.randint(0, num_pilhas - 1)].append(caixa)

    if num_caixas > 2:

        max_certas = num_caixas - 2
        while True:
            corretas = 0
            for i in range(num_pilhas):
                for caixa in pilhas_inicial[i]:
                    if caixa in pilhas_final[i]:
                        corretas += 1
            if corretas <= max_certas:
                break
            # Se há mais do que o permitido, embaralhe as caixas finais novamente
            random.shuffle(caixas_finais)
            pilhas_final = [[] for _ in range(num_pilhas)]
            for caixa in caixas_finais:
                pilhas_final[random.randint(0, num_pilhas - 1)].append(caixa)

    return pilhas_inicial, pilhas_final

def plot_estados_visitados(nos_a_estrela, nos_largura, nos_profundidade_limitada):

    algoritmos = ['Busca A*', 'Busca em Largura', 'Busca em Profundidade Limitada']
    visitados = [nos_a_estrela, nos_largura, nos_profundidade_limitada]
    plt.figure(figsize=(10, 6))
    plt.bar(algoritmos, visitados, color=['blue', 'green', 'orange'])
    plt.title("Número Total de Estados Visitados por Algoritmo")
    plt.xlabel("Algoritmo")
    plt.ylabel("Número Total de Estados Visitados")
    plt.show()

def chamar_busca_largura():

    start_time = time.time()
    caminho_largura, estados_largura, total_estados_largura = estoque.busca_em_largura()
    end_time = time.time()
    '''
    if caminho_largura:
        print("Movimentos para atingir o estado final (Busca em Largura):")
        for movimento in caminho_largura:
            print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")

        print("\nTransições de estados (Busca em Largura):")
        for estado in estados_largura:
            print(estado)
    else:
        print("Não foi possível encontrar uma solução (Busca em Largura).")'''

    print(f"Tempo de execução (Busca em Largura): {end_time - start_time:.4f} segundos")
    
    total_time = end_time - start_time

    return total_estados_largura, total_time, estados_largura

def chamar_busca_profundidade_limitada(limite=60):

    start_time = time.time()
    caminho_profundidade_limitada, estados_profundidade_limitada, total_estados_profundidade_limitada = estoque.busca_profundidade_limitada(limite)
    end_time = time.time()
    '''
    if caminho_profundidade_limitada:
        print("Movimentos para atingir o estado final (Busca em Profundidade Limitada):")
        for movimento in caminho_profundidade_limitada:
            print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")

        print("\nTransições de estados (Busca em Profundidade Limitada):")
        for estado in estados_profundidade_limitada:
            print(estado)
    else:
        print("Não foi possível encontrar uma solução (Busca em Profundidade Limitada).")
    '''
    total_time = (end_time - start_time)

    print(f"Tempo de execução (Busca em Profundidade Limitada): {end_time - start_time:.4f} segundos")
    return total_estados_profundidade_limitada, total_time, estados_profundidade_limitada

def chamar_busca_a_estrela():

    start_time = time.time()
    caminho_a_estrela, estados_a_estrela, total_estados_a_estrela = estoque.busca_a_estrela()
    end_time = time.time()
    '''
    if caminho_a_estrela:
        print("Movimentos para atingir o estado final (Busca A*):")
        for movimento in caminho_a_estrela:
            print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")

        print("\nTransições de estados (Busca A*):")
        for estado in estados_a_estrela:
            print(estado)
    else:
        print("Não foi possível encontrar uma solução (Busca A*).")
    '''
    total_time = end_time - start_time

    print(f"Tempo de execução (Busca A*): {end_time - start_time:.4f} segundos")
    return total_estados_a_estrela, total_time, estados_a_estrela

# pilhas_inicial = [['c', 'b', 'a'], ['e', 'd'], ['g', 'f']]
# pilhas_final = [[], ['f', 'g', 'd', 'b'], ['c', 'a', 'e']]

# pilhas_inicial, pilhas_final = criar_casos_aleatorios(8)
# estoque = Estoque(pilhas_inicial, pilhas_final)

# total_largura, time_largura, estados_largura = chamar_busca_largura()
# total_profundidade_limitada, time_profundidade, estados_profundidade_limitado = chamar_busca_profundidade_limitada()
# total_a_estrela, time_a_estrela, estados_busca_estrela = chamar_busca_a_estrela()

# plot_estados_visitados(total_a_estrela, total_largura, total_profundidade_limitada)

# print(f'Nós totais A*: {total_a_estrela}, tempo total: {time_a_estrela},número de passos até solução: {len(estados_busca_estrela)}')
# print(f'Nós totais Largura: {total_largura}, tempo total: {time_largura},número de passos até solução: {len(estados_largura)}')
# print(f'Nós totais Profundidade Limitada*: {total_profundidade_limitada}, tempo total: {time_profundidade},número de passos até solução: {len(estados_profundidade_limitado)}')

lista_nodos_largura = []
lista_tempo_largura = []
lista_passos_largura = []

lista_nodos_profundidade = []
lista_tempo_profundidade = []
lista_passos_profundidade = []

lista_nodos_a_estrela = []
lista_tempo_a_estrela = []
lista_passos_a_estrela = []

k_min = 2
k_max = 8

for n_caixas in range(k_min, k_max):

    pilhas_inicial, pilhas_final = criar_casos_aleatorios(n_caixas)
    estoque = Estoque(pilhas_inicial, pilhas_final)

    total_estados_largura, total_time_largura, estados_largura = chamar_busca_largura()
    lista_nodos_largura.append(total_estados_largura)
    lista_tempo_largura.append(total_time_largura)
    lista_passos_largura.append(estados_largura)
 
    total_estados_profundidade, total_time_profundidade, estados_profundidade = chamar_busca_profundidade_limitada()
    lista_nodos_profundidade.append(total_estados_profundidade)
    lista_tempo_profundidade.append(total_time_profundidade)
    lista_passos_profundidade.append(estados_profundidade)

    total_estados_a_estrela, total_time_a_estrela, estados_a_estrela = chamar_busca_a_estrela()
    lista_nodos_a_estrela.append(total_estados_a_estrela)
    lista_tempo_a_estrela.append(total_time_a_estrela)
    lista_passos_a_estrela.append(estados_a_estrela)
 

k_values = list(range(k_min, k_max))
lista_passos_largura_count = [len(steps) for steps in lista_passos_largura]
lista_passos_profundidade_count = [len(steps) for steps in lista_passos_profundidade]
lista_passos_a_estrela_count = [len(steps) for steps in lista_passos_a_estrela]

plt.figure(figsize=(10, 6))
plt.plot(k_values, lista_nodos_largura, marker='o', label='Busca em Largura')
plt.plot(k_values, lista_nodos_profundidade, marker='o', label='Busca em Profundidade Limitada')
plt.plot(k_values, lista_nodos_a_estrela, marker='o', label='Busca A*')
#plt.yscale('log')
plt.title('Número de Nós Visitados x Número de Caixas')
plt.xlabel('Número de Caixas')
plt.ylabel('Número de Nós Visitados')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(k_values, lista_tempo_largura, marker='o', label='Busca em Largura')
plt.plot(k_values, lista_tempo_profundidade, marker='o', label='Busca em Profundidade Limitada')
plt.plot(k_values, lista_tempo_a_estrela, marker='o', label='Busca A*')
plt.yscale('log')
plt.title('Tempo Total x Número de Caixas')
plt.xlabel('Número de Caixas')
plt.ylabel('Tempo Total (s)')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
# Busca em Largura com quadrados maiores
plt.plot(k_values, lista_passos_largura_count, marker='s', markersize=8, linestyle='-', label='Busca em Largura')

# Busca em Profundidade Limitada e Busca A* com marcadores circulares
plt.plot(k_values, lista_passos_profundidade_count, marker='o', markersize=6, linestyle='-', label='Busca em Profundidade Limitada')
plt.plot(k_values, lista_passos_a_estrela_count, marker='o', markersize=6, linestyle='-', label='Busca A*')

plt.yscale('log')
plt.title('Número de Passos/Estados x Número de Caixas')
plt.xlabel('Número de Caixas')
plt.ylabel('Número de Passos/Estados')

plt.legend()
plt.show()

