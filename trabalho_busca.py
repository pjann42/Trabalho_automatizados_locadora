# Trabalho Busca

# Partes comentadas do código foram utilizadas para observar o comportamento do sistema e debugar

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

    def busca_profundidade_iterativa(self):
        profundidade = 1
        nodos_observados = []  

        while True:
            caminho, estados_visitados, estados_totais_visitados = self.busca_profundidade_limitada(profundidade)
            nodos_observados.extend(estados_visitados)  

            if caminho:  
                return caminho, nodos_observados, estados_totais_visitados
            
            profundidade += 1  

            
            if profundidade > 200:  
                break

        return [], nodos_observados, 0  

    def heuristica(self, estado_atual):
        penalidade = 0
        for pilha_idx, pilha in enumerate(estado_atual):
            for posicao, caixa in enumerate(pilha):
                
                if caixa not in self.estado_final[pilha_idx]:
                    penalidade += 1
                else:
                    
                    posicao_final = self.estado_final[pilha_idx].index(caixa)
                    if posicao > posicao_final:
                        penalidade += 1  
        return penalidade

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


def chamar_busca_largura():

    start_time = time.time()
    caminho_largura, estados_largura, total_estados_largura = estoque.busca_em_largura()
    end_time = time.time()
    total_time = end_time - start_time
    
    # if caminho_largura:
    #     print("Movimentos para atingir o estado final (Busca em Largura):")
    #     for movimento in caminho_largura:
    #         print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")

    #     print("\nTransições de estados (Busca em Largura):")
    #     for estado in estados_largura:
    #         print(estado)
    # else:
    #     print("Não foi possível encontrar uma solução (Busca em Largura).")

    print(f"Tempo de execução (Busca em Largura): {end_time - start_time:.4f} segundos")
    
    return total_estados_largura, total_time, estados_largura

def chamar_busca_profundidade_normal():

    start_time = time.time()
    caminho_profundidade, estados_profundidade, total_estados_profundidade = estoque.busca_profundidade_normal()
    end_time = time.time()
    total_time = end_time - start_time
    
    if caminho_profundidade:
        print("Movimentos para atingir o estado final (Busca em Largura):")
        for movimento in caminho_profundidade:
            print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")

        print("\nTransições de estados (Busca em Largura):")
        for estado in estados_profundidade:
            print(estado)
    else:
        print("Não foi possível encontrar uma solução (Busca em Largura).")

    print(f"Tempo de execução (Busca em Largura): {end_time - start_time:.4f} segundos")

    return total_estados_profundidade, total_time, estados_profundidade

def chamar_busca_profundidade_iterativa():

    start_time = time.time()
    caminho_profundidade, nodos_profundidade, total_estados_profundidade = estoque.busca_profundidade_iterativa()
    end_time = time.time()
    total_time = end_time - start_time

    # if caminho_profundidade:
    #     print("Movimentos para atingir o estado final (Busca em Profundidade Iterativa):")
    #     for movimento in caminho_profundidade:
    #         print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")

    #     print("\nTransições de estados (Busca em Profundidade Iterativa):")
    #     for estado in nodos_profundidade:
    #         print(estado)
    # else:
    #     print("Não foi possível encontrar uma solução (Busca em Profundidade Iterativa).")
    
    print(f"Tempo de execução (Busca em Profundidade Iterativa): {end_time - start_time:.4f} segundos")

    return total_estados_profundidade, total_time, nodos_profundidade

def chamar_busca_profundidade_limitada(limite = 150):

    start_time = time.time()
    caminho_profundidade_limitada, estados_profundidade_limitada, total_estados_profundidade_limitada = estoque.busca_profundidade_limitada(limite)
    end_time = time.time()
    total_time = end_time - start_time

    # if caminho_profundidade_limitada:
    #     print("Movimentos para atingir o estado final (Busca em Profundidade Limitada):")
    #     for movimento in caminho_profundidade_limitada:
    #         print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")

    #     print("\nTransições de estados (Busca em Profundidade Limitada):")
    #     for estado in estados_profundidade_limitada:
    #         print(estado)
    # else:
    #     print("Não foi possível encontrar uma solução (Busca em Profundidade Limitada).")
    
    print(f"Tempo de execução (Busca em Profundidade Limitada): {end_time - start_time:.4f} segundos")
    return total_estados_profundidade_limitada, total_time, estados_profundidade_limitada

def chamar_busca_a_estrela():

    start_time = time.time()
    caminho_a_estrela, estados_a_estrela, total_estados_a_estrela = estoque.busca_a_estrela()
    end_time = time.time()
    total_time = end_time - start_time
    
    # if caminho_a_estrela:
    #     print("Movimentos para atingir o estado final (Busca A*):")
    #     for movimento in caminho_a_estrela:
    #         print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")

    #     print("\nTransições de estados (Busca A*):")
    #     for estado in estados_a_estrela:
    #         print(estado)
    # else:
    #     print("Não foi possível encontrar uma solução (Busca A*).")
    
    print(f"Tempo de execução (Busca A*): {end_time - start_time:.4f} segundos")
    return total_estados_a_estrela, total_time, estados_a_estrela

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

        max_certas = 0

        while True:

            corretas = 0

            for i in range(num_pilhas):
                for caixa in pilhas_inicial[i]:
                    if caixa in pilhas_final[i]:
                        corretas += 1
            if corretas == max_certas:

                break

            random.shuffle(caixas_finais)
            pilhas_final = [[] for _ in range(num_pilhas)]
            for caixa in caixas_finais:
                pilhas_final[random.randint(0, num_pilhas - 1)].append(caixa)

    return pilhas_inicial, pilhas_final

####################################### PROBLEMA ######################################

lista_nodos_largura = []
lista_tempo_largura = []
lista_passos_largura = []

lista_nodos_profundidade = []
lista_tempo_profundidade = []
lista_passos_profundidade = []

lista_nodos_profundidade_iterativa = []
lista_tempo_profundidade_iterativa = []
lista_passos_profundidade_iterativa = []

lista_nodos_a_estrela = []
lista_tempo_a_estrela = []
lista_passos_a_estrela = []

lista_nodos_profundidade_normal = []
lista_tempo_profundidade_normal = []
lista_passos_profundidade_normal = []

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

    total_estados_profundidade_iterativa, total_time_profundidade_iterativa, estados_profundidade_iterativa = chamar_busca_profundidade_iterativa()
    lista_nodos_profundidade_iterativa.append(total_estados_profundidade_iterativa)
    lista_tempo_profundidade_iterativa.append(total_time_profundidade_iterativa)
    lista_passos_profundidade_iterativa.append(estados_profundidade_iterativa)

    total_estados_a_estrela, total_time_a_estrela, estados_a_estrela = chamar_busca_a_estrela()
    lista_nodos_a_estrela.append(total_estados_a_estrela)
    lista_tempo_a_estrela.append(total_time_a_estrela)
    lista_passos_a_estrela.append(estados_a_estrela)

    # Adicionar a busca em profundidade normal
    total_estados_profundidade_normal, total_time_profundidade_normal, estados_profundidade_normal = chamar_busca_profundidade_normal()
    lista_nodos_profundidade_normal.append(total_estados_profundidade_normal)
    lista_tempo_profundidade_normal.append(total_time_profundidade_normal)
    lista_passos_profundidade_normal.append(estados_profundidade_normal)
 
k_values = list(range(k_min, k_max))
lista_passos_largura_count = [len(steps) for steps in lista_passos_largura]
lista_passos_profundidade_count = [len(steps) for steps in lista_passos_profundidade]
lista_passos_profundidade_iterativa_count = [len(steps) for steps in lista_passos_profundidade_iterativa]
lista_passos_a_estrela_count = [len(steps) for steps in lista_passos_a_estrela]
lista_passos_profundidade_normal_count = [len(steps) for steps in lista_passos_profundidade_normal]

plt.figure(figsize=(10, 6))
plt.plot(k_values, lista_nodos_largura, marker='o', label='Busca em Largura')
plt.plot(k_values, lista_nodos_profundidade, marker='o', label='Busca em Profundidade Limitada')
plt.plot(k_values, lista_nodos_profundidade_iterativa, marker='o', label='Busca em Profundidade Iterativa')
plt.plot(k_values, lista_nodos_a_estrela, marker='o', label='Busca A*')
plt.plot(k_values, lista_nodos_profundidade_normal, marker='o', label='Busca em Profundidade Normal')
plt.title('Número de Nós Visitados x Número de Caixas')
plt.xlabel('Número de Caixas')
plt.ylabel('Número de Nós Visitados')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(k_values, lista_nodos_largura, marker='o', label='Busca em Largura')
plt.plot(k_values, lista_nodos_profundidade, marker='o', label='Busca em Profundidade Limitada')
plt.plot(k_values, lista_nodos_profundidade_iterativa, marker='o', label='Busca em Profundidade Iterativa')
plt.plot(k_values, lista_nodos_a_estrela, marker='o', label='Busca A*')
plt.plot(k_values, lista_nodos_profundidade_normal, marker='o', label='Busca em Profundidade Normal')
plt.yscale('log')
plt.title('Número de Nós Visitados x Número de Caixas')
plt.xlabel('Número de Caixas')
plt.ylabel('Número de Nós Visitados')
plt.legend()
plt.show()

k_values_filtrados = [k for k in k_values if k >= 4]
lista_tempo_largura_filtrados = [tempo if tempo != 0 else None for k, tempo in zip(k_values, lista_tempo_largura) if k >= 4]
lista_tempo_profundidade_filtrados = [tempo if tempo != 0 else None for k, tempo in zip(k_values, lista_tempo_profundidade) if k >= 4]
lista_tempo_profundidade_iterativa_filtrados = [tempo if tempo != 0 else None for k, tempo in zip(k_values, lista_tempo_profundidade_iterativa) if k >= 4]
lista_tempo_a_estrela_filtrados = [tempo if tempo != 0 else None for k, tempo in zip(k_values, lista_tempo_a_estrela) if k >= 4]
lista_tempo_profundidade_normal_filtrados = [tempo if tempo != 0 else None for k, tempo in zip(k_values, lista_tempo_profundidade_normal) if k >= 4]

plt.figure(figsize=(10, 6))
plt.plot(k_values_filtrados, lista_tempo_largura_filtrados, marker='o', label='Busca em Largura')
plt.plot(k_values_filtrados, lista_tempo_profundidade_filtrados, marker='o', label='Busca em Profundidade Limitada')
plt.plot(k_values_filtrados, lista_tempo_profundidade_iterativa_filtrados, marker='o', label='Busca em Profundidade Iterativa')
plt.plot(k_values_filtrados, lista_tempo_a_estrela_filtrados, marker='o', label='Busca A*')
plt.plot(k_values_filtrados, lista_tempo_profundidade_normal_filtrados, marker='o', label='Busca em Profundidade Normal')
plt.yscale('log')
plt.title('Tempo Total x Número de Caixas')
plt.xlabel('Número de Caixas')
plt.ylabel('Tempo Total (s)')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(k_values, lista_passos_largura_count, marker='s', markersize=8, linestyle='-', label='Busca em Largura')
plt.plot(k_values, lista_passos_profundidade_count, marker='o', markersize=6, linestyle='-', label='Busca em Profundidade Limitada')
plt.plot(k_values, lista_passos_profundidade_iterativa_count, marker='o', markersize=6, linestyle='-', label='Busca em Profundidade Iterativa')
plt.plot(k_values, lista_passos_a_estrela_count, marker='o', markersize=6, linestyle='-', label='Busca A*')
plt.plot(k_values, lista_passos_profundidade_normal_count, marker='o', markersize=6, linestyle='-', label='Busca em Profundidade Normal')
plt.title('Número de Passos/Estados x Número de Caixas')
plt.xlabel('Número de Caixas')
plt.ylabel('Número de Passos/Estados')
plt.legend()
plt.show()


# pilhas_inicial = [['c', 'b', 'a'], ['e', 'd'], ['g', 'f']]
# pilhas_final = [[], ['f', 'g', 'd', 'b'], ['c', 'a', 'e']]

# pilhas_inicial, pilhas_final = criar_casos_aleatorios(8)
# estoque = Estoque(pilhas_inicial, pilhas_final)


# def plot_estados_visitados(nos_a_estrela, nos_largura, nos_profundidade_limitada):

#     algoritmos = ['Busca A*', 'Busca em Largura', 'Busca em Profundidade Limitada']
#     visitados = [nos_a_estrela, nos_largura, nos_profundidade_limitada]
#     plt.figure(figsize=(10, 6))
#     plt.bar(algoritmos, visitados, color=['blue', 'green', 'orange'])
#     plt.title("Número Total de Estados Visitados por Algoritmo")
#     plt.xlabel("Algoritmo")
#     plt.ylabel("Número Total de Estados Visitados")
#     plt.show()

# total_largura, time_largura, estados_largura = chamar_busca_largura()
# total_profundidade_limitada, time_profundidade, estados_profundidade_limitado = chamar_busca_profundidade_limitada()
# total_a_estrela, time_a_estrela, estados_busca_estrela = chamar_busca_a_estrela()

# plot_estados_visitados(total_a_estrela, total_largura, total_profundidade_limitada)

# print(f'Nós totais A*: {total_a_estrela}, tempo total: {time_a_estrela},número de passos até solução: {len(estados_busca_estrela)}')
# print(f'Nós totais Largura: {total_largura}, tempo total: {time_largura},número de passos até solução: {len(estados_largura)}')
# print(f'Nós totais Profundidade Limitada*: {total_profundidade_limitada}, tempo total: {time_profundidade},número de passos até solução: {len(estados_profundidade_limitado)}')


# Pilha Errada: Se uma caixa está na pilha errada, adicionamos uma penalidade de +1. Isso é o mínimo necessário para movê-la para a pilha correta.
# Ordem Correta: Se a caixa está na pilha correta, verificamos se está fora de ordem (por exemplo, se uma caixa mais acima na pilha deveria estar abaixo dela). Se estiver fora de ordem, penalizamos com +1.
# Admissibilidade: A heurística não superestima o custo real. Cada caixa que precisa ser movida gera apenas o número mínimo de penalizações necessárias, garantindo que o A* explore o caminho correto para encontrar a solução ótima.

# pilhas_inicial, pilhas_final = criar_casos_aleatorios(6)
# estoque = Estoque(pilhas_inicial, pilhas_final)
# a,b,c = chamar_busca_profundidade_normal()
# print(a,b,c)