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

    def busca_profundidade_limitada(self, limite=2):
        estados_totais_visitados = 0

        while True:
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
                
            limite += 1  # Aumenta o limite iterativamente

    def heuristica(self, estado_atual):
        correto = 0
        for pilha_idx, pilha in enumerate(estado_atual):
            for caixa in pilha:
                if caixa in self.estado_final[pilha_idx]:
                    correto += 1
        return len(self.estado_final[0] + self.estado_final[1] + self.estado_final[2]) - correto

    def busca_a_estrela(self):
        # Fila de prioridade (custo_total, estado_atual, caminho_percorrido, estados_visitados)
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

def plot_estados_visitados(nos_a_estrela, nos_largura, nos_profundidade_iterativa):
    algoritmos = ['Busca A*', 'Busca em Largura', 'Busca em Profundidade Iterativa']
    visitados = [nos_a_estrela, nos_largura, nos_profundidade_iterativa]

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

    if caminho_largura:
        '''print("Movimentos para atingir o estado final (Busca em Largura):")'''
        for movimento in caminho_largura:
            print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")

        '''print("\nTransições de estados (Busca em Largura):")'''
        for estado in estados_largura:
            '''print(estado)'''
    else:
        '''print("Não foi possível encontrar uma solução (Busca em Largura).")'''

    print(f"Tempo de execução (Busca em Largura): {end_time - start_time:.4f} segundos")
    return total_estados_largura

def chamar_busca_profundidade_iterativa(limite=20):

    start_time = time.time()  
    caminho_profundidade_iterativa, estados_profundidade_iterativa, total_estados_profundidade_iterativa = estoque.busca_profundidade_limitada(limite)
    end_time = time.time()  

    if caminho_profundidade_iterativa:
        '''print("Movimentos para atingir o estado final (Busca em Profundidade Iterativa):")'''
        for movimento in caminho_profundidade_iterativa:
            '''print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")'''

        '''print("\nTransições de estados (Busca em Profundidade Iterativa):")'''
        for estado in estados_profundidade_iterativa:
           print(estado)
    else:
        print("Não foi possível encontrar uma solução (Busca em Profundidade Iterativa).")

    print(f"Tempo de execução (Busca em Profundidade Iterativa): {end_time - start_time:.4f} segundos")
    return total_estados_profundidade_iterativa

def chamar_busca_a_estrela():

    start_time = time.time()  
    caminho_a_estrela, estados_a_estrela, total_estados_a_estrela = estoque.busca_a_estrela()
    end_time = time.time()  

    if caminho_a_estrela:
        '''print("Movimentos para atingir o estado final (Busca A*):")'''
        for movimento in caminho_a_estrela:
            '''print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")'''

        print("\nTransições de estados (Busca A*):")
        for estado in estados_a_estrela:
            '''print(estado)'''
    else:
        print("Não foi possível encontrar uma solução (Busca A*).")

    print(f"Tempo de execução (Busca A*): {end_time - start_time:.4f} segundos")
    return total_estados_a_estrela

def chamar_busca_profundidade_normal():
    start_time = time.time()  
    caminho_profundidade_normal, estados_profundidade_normal, total_estados_profundidade_normal = estoque.busca_profundidade_normal()
    end_time = time.time()  

    if caminho_profundidade_normal:
        print("Movimentos para atingir o estado final (Busca em Profundidade Normal):")
        for movimento in caminho_profundidade_normal:
            print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")

        print("\nTransições de estados (Busca em Profundidade Normal):")
        for estado in estados_profundidade_normal:
            print(estado)
    else:
        print("Não foi possível encontrar uma solução (Busca em Profundidade Normal).")

    print(f"Tempo de execução (Busca em Profundidade Normal): {end_time - start_time:.4f} segundos")
    return total_estados_profundidade_normal

# Exemplo de uso


pilhas_inicial = [['c', 'b', 'a'], ['e', 'd'], ['g', 'f']]
pilhas_final = [[], ['f', 'g', 'd', 'b'], ['c', 'a', 'e']]

estoque = Estoque(pilhas_inicial, pilhas_final)

nos_largura = chamar_busca_largura()
nos_profundidade_iterativa = chamar_busca_profundidade_iterativa(limite=50)
nos_a_estrela = chamar_busca_a_estrela()
#nos_profundidade_normal = chamar_busca_profundidade_normal()

# Plotando o número de estados visitados
plot_estados_visitados(nos_a_estrela, nos_largura, nos_profundidade_iterativa)
