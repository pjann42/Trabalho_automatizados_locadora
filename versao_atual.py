from criar_casos import criar_casos_aleatorios
from collections import deque
from heapq import heappush, heappop
import time
import matplotlib.pyplot as plt

class Estoque:
    def __init__(self, pilhas_inicial, pilhas_final):
        self.estado_inicial = pilhas_inicial
        self.estado_final = pilhas_final

    def mover_caixa(self, estado_atual, origem, destino):
        novo_estado = [list(pilha) for pilha in estado_atual]  # Copia o estado atual
        if len(novo_estado[origem]) > 0:
            caixa = novo_estado[origem].pop()
            novo_estado[destino].append(caixa)
            return novo_estado, caixa
        return estado_atual, None

    def busca_em_largura(self):
        fila = deque([(self.estado_inicial, [], [self.estado_inicial])])  # (estado_atual, caminho_percorrido, estados_visitados)
        visitados = set()  # Para armazenar estados já visitados
        estados_totais_visitados = 0

        while fila:
            estado_atual, caminho, estados_visitados = fila.popleft()
            estado_tupla = tuple(tuple(pilha) for pilha in estado_atual)  # Converte para tupla para hash
            estados_totais_visitados += 1

            if estado_atual == self.estado_final:
                return caminho, estados_visitados, estados_totais_visitados  # Retorna o caminho, estados visitados e total de estados visitados

            if estado_tupla in visitados:
                continue

            visitados.add(estado_tupla)

            # Gerar novos estados movendo caixas entre pilhas
            for origem in range(3):
                for destino in range(3):
                    if origem != destino:
                        novo_estado, caixa = self.mover_caixa(estado_atual, origem, destino)
                        if caixa is not None:  # Verifica se a caixa foi movida
                            novo_caminho = caminho + [(origem, destino, caixa)]
                            fila.append((novo_estado, novo_caminho, estados_visitados + [novo_estado]))

        return None, None, estados_totais_visitados  # Não encontrou solução

    def busca_profundidade_limitada(self, limite):
        estados_totais_visitados = 0
        pilha = [(self.estado_inicial, [], 0, [self.estado_inicial])]  # (estado_atual, caminho_percorrido, profundidade, estados_visitados)
        visitados = set()  # Para armazenar estados já visitados

        while pilha:
            estado_atual, caminho, profundidade, estados_visitados = pilha.pop()
            estado_tupla = tuple(tuple(pilha) for pilha in estado_atual)  # Converte para tupla para hash
            estados_totais_visitados += 1

            if estado_atual == self.estado_final:
                return caminho, estados_visitados, estados_totais_visitados  # Retorna o caminho, estados visitados e total de estados visitados

            if estado_tupla in visitados or profundidade >= limite:
                continue

            visitados.add(estado_tupla)

            # Gerar novos estados movendo caixas entre pilhas
            for origem in range(3):
                for destino in range(3):
                    if origem != destino:
                        novo_estado, caixa = self.mover_caixa(estado_atual, origem, destino)
                        if caixa is not None:  # Verifica se a caixa foi movida
                            novo_caminho = caminho + [(origem, destino, caixa)]
                            pilha.append((novo_estado, novo_caminho, profundidade + 1, estados_visitados + [novo_estado]))

        return None, None, estados_totais_visitados  # Não encontrou solução


    def heuristica(self, estado_atual):
        correto = 0
        for pilha_idx, pilha in enumerate(estado_atual):
            for caixa in pilha:
                if caixa in self.estado_final[pilha_idx]:
                    correto += 2
        return len(self.estado_final[0] + self.estado_final[1] + self.estado_final[2]) - correto

    def busca_a_estrela(self):
        fila = []
        heappush(fila, (0 + self.heuristica(self.estado_inicial), self.estado_inicial, [], [self.estado_inicial]))
        visitados = set()  # Para armazenar estados já visitados
        estados_totais_visitados = 0

        while fila:
            custo_total, estado_atual, caminho, estados_visitados = heappop(fila)
            estados_totais_visitados += 1

            if estado_atual == self.estado_final:
                return caminho, estados_visitados, estados_totais_visitados  # Retorna o caminho, estados visitados e total de estados visitados

            estado_tupla = tuple(tuple(pilha) for pilha in estado_atual)  # Converte para tupla para hash

            if estado_tupla in visitados:
                continue

            visitados.add(estado_tupla)

            # Gerar novos estados movendo caixas entre pilhas
            for origem in range(3):
                for destino in range(3):
                    if origem != destino:
                        novo_estado, caixa = self.mover_caixa(estado_atual, origem, destino)
                        if caixa is not None:  # Verifica se a caixa foi movida
                            novo_caminho = caminho + [(origem, destino, caixa)]
                            custo = len(novo_caminho)  # Custo é o número de movimentos
                            heuristica = self.heuristica(novo_estado)
                            custo_total_novo = custo + heuristica
                            heappush(fila, (custo_total_novo, novo_estado, novo_caminho, estados_visitados + [novo_estado]))

    def busca_profundidade_normal(self):

        pilha = [(self.estado_inicial, [], 0, [self.estado_inicial])]  # (estado_atual, caminho_percorrido, profundidade, estados_visitados)
        visitados = set()  # Para armazenar estados já visitados
        estados_totais_visitados = 0

        while pilha:
            estado_atual, caminho, profundidade, estados_visitados = pilha.pop()
            estado_tupla = tuple(tuple(pilha) for pilha in estado_atual)  # Converte para tupla para hash
            estados_totais_visitados += 1

            if estado_atual == self.estado_final:
                return caminho, estados_visitados, estados_totais_visitados  # Retorna o caminho, estados visitados e total de estados visitados

            if estado_tupla in visitados:
                continue

            visitados.add(estado_tupla)

            # Gerar novos estados movendo caixas entre pilhas
            for origem in range(3):
                for destino in range(3):
                    if origem != destino:
                        novo_estado, caixa = self.mover_caixa(estado_atual, origem, destino)
                        if caixa is not None:  # Verifica se a caixa foi movida
                            novo_caminho = caminho + [(origem, destino, caixa)]
                            pilha.append((novo_estado, novo_caminho, profundidade + 1, estados_visitados + [novo_estado]))

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
        print("Não foi possível encontrar uma solução (Busca em Largura).")

    print(f"Tempo de execução (Busca em Largura): {end_time - start_time:.4f} segundos")
    '''
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

# Exemplo de uso:

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

import matplotlib.pyplot as plt

# Inicialização das listas
import matplotlib.pyplot as plt

# Inicialização das listas
lista_nodos_largura = []
lista_nodos_profundiade = []
lista_nodos_a_estrela = []

# Defina o intervalo de k
k_min = 1
k_max = 8

# Executa as buscas para diferentes valores de k
for k in range(k_min, k_max):
    pilhas_inicial, pilhas_final = criar_casos_aleatorios((k))
    estoque = Estoque(pilhas_inicial, pilhas_final)
    lista_nodos_largura.append(chamar_busca_largura()[0])
    lista_nodos_profundiade.append(chamar_busca_profundidade_limitada()[0])
    lista_nodos_a_estrela.append(chamar_busca_a_estrela()[0])

# Ajusta os valores de k para o intervalo usado
k_values = list(range(k_min, k_max))

# Criação do gráfico
plt.figure(figsize=(10, 6))
plt.plot(k_values, lista_nodos_largura, marker='o', label='Busca em Largura')
plt.plot(k_values, lista_nodos_profundiade, marker='o', label='Busca em Profundidade Limitada')
plt.plot(k_values, lista_nodos_a_estrela, marker='o', label='Busca A*')

# Define o eixo y em escala logarítmica
plt.yscale('log')

# Adiciona título e rótulos aos eixos
plt.title('Número de Nós Visitados vs. Valor de k')
plt.xlabel('Valor de k')
plt.ylabel('Número de Nós Visitados (escala logarítmica)')

# Adiciona uma legenda
plt.legend()

# Exibe o gráfico

plt.show()

