
from collections import deque
from heapq import heappush, heappop
import time

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
        return estado_atual, None  # Caso não haja caixa para mover

    def busca_em_largura(self):
        fila = deque([(self.estado_inicial, [])])  # Fila contendo (estado_atual, caminho_percorrido)
        visitados = set()  # Para armazenar estados já visitados

        while fila:
            estado_atual, caminho = fila.popleft()
            estado_tupla = tuple(tuple(pilha) for pilha in estado_atual)  # Converte para tupla para hash

            if estado_atual == self.estado_final:
                return caminho  # Retorna o caminho percorrido até o estado final

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
                            fila.append((novo_estado, novo_caminho))

        return None  

    def busca_profundidade_iterativa(self):

        limite = 0  # Limite inicial

        while True:
            pilha = [(self.estado_inicial, [], 0)]  # (estado_atual, caminho_percorrido, profundidade)
            visitados = set()  # Para armazenar estados já visitados

            while pilha:
                estado_atual, caminho, profundidade = pilha.pop()
                estado_tupla = tuple(tuple(pilha) for pilha in estado_atual)  # Converte para tupla para hash

                if estado_atual == self.estado_final:
                    return caminho  # Retorna o caminho percorrido até o estado final

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
                                pilha.append((novo_estado, novo_caminho, profundidade + 1))
                
            limite += 1  # Aumenta o limite iterativamente

    
    def heuristica(self, estado_atual):
        correto = 0
        for pilha_idx, pilha in enumerate(estado_atual):
            for caixa in pilha:
                if caixa in self.estado_final[pilha_idx]:
                    correto += 1
        return len(self.estado_final[0] + self.estado_final[1] + self.estado_final[2]) - correto


    def busca_a_estrela(self):
        # Fila de prioridade (custo_total, estado_atual, caminho_percorrido)
        fila = []
        heappush(fila, (0 + self.heuristica(self.estado_inicial), self.estado_inicial, []))
        visitados = set()  # Para armazenar estados já visitados

        while fila:
            custo_total, estado_atual, caminho = heappop(fila)

            if estado_atual == self.estado_final:
                return caminho  # Retorna o caminho percorrido até o estado final

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
                            heappush(fila, (custo_total_novo, novo_estado, novo_caminho))
    

    def busca_profundidade_normal(self):
        pilha = [(self.estado_inicial, [], 0)]  # (estado_atual, caminho_percorrido, profundidade)
        visitados = set()  # Para armazenar estados já visitados

        while pilha:
            estado_atual, caminho, profundidade = pilha.pop()
            estado_tupla = tuple(tuple(pilha) for pilha in estado_atual)  # Converte para tupla para hash

            if estado_atual == self.estado_final:
                return caminho  # Retorna o caminho percorrido até o estado final

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
                            pilha.append((novo_estado, novo_caminho, profundidade + 1))



pilhas_inicial = [['c', 'b', 'a'], ['e', 'd'], ['g', 'f']]
pilhas_final = [[], ['f', 'g', 'd', 'b'], ['c', 'a', 'e']]
# pilhas_inicial = [['c', 'b', 'a'], [], []]
# pilhas_final = [[], ['b'], ['c', 'a']]

estoque = Estoque(pilhas_inicial, pilhas_final)

def chamar_busca_largura():

    start_time = time.time()  
    caminho_largura = estoque.busca_em_largura()
    end_time = time.time()  

    if caminho_largura:
        print("Movimentos para atingir o estado final (Busca em Largura):")
        for movimento in caminho_largura:
            print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")
    else:
        print("Não foi possível encontrar uma solução (Busca em Largura).")

    print(f"Tempo de execução (Busca em Largura): {end_time - start_time:.4f} segundos")

def chamar_busca_profundidade_iterativa():

    start_time = time.time()  
    caminho_profundidade_iterativa = estoque.busca_profundidade_iterativa()
    end_time = time.time()  

    if caminho_profundidade_iterativa:
        print("\nMovimentos para atingir o estado final (Busca em Profundidade Iterativa):")
        for movimento in caminho_profundidade_iterativa:
            print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")
    else:
        print("Não foi possível encontrar uma solução (Busca em Profundidade Iterativa).")

    print(f"Tempo de execução (Busca em Profundidade Iterativa): {end_time - start_time:.4f} segundos")

def chama_busca_A_star():

    start_time = time.time()  
    caminho_a_estrela = estoque.busca_a_estrela()
    end_time = time.time()  

    if caminho_a_estrela:
        print("\nMovimentos para atingir o estado final (Busca A*):")
        for movimento in caminho_a_estrela:
            print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")
    else:
        print("Não foi possível encontrar uma solução (Busca A*).")

    print(f"Tempo de execução (Busca A*): {end_time - start_time:.4f} segundos")


def chamar_busca_profundidade_normal():

    start_time = time.time()  # Início da medição
    caminho_profundidade_normal = estoque.busca_profundidade_normal()
    end_time = time.time()  # Fim da medição
    if caminho_profundidade_normal:
        print("\nMovimentos para atingir o estado final (Busca em Profundidade Normal):")
        for movimento in caminho_profundidade_normal:
            print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")
    else:
        print("Não foi possível encontrar uma solução (Busca em Profundidade Normal).")

    print(f"Tempo de execução (Busca A*): {end_time - start_time:.4f} segundos")



#chamar_busca_profundidade_normal()
chama_busca_A_star()
chamar_busca_largura()
chamar_busca_profundidade_iterativa()