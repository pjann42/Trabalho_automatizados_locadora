from collections import deque

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

    def busca_em_profundidade(self):
        pilha = [(self.estado_inicial, [])]  # Pilha contendo (estado_atual, caminho_percorrido)
        visitados = set()  # Para armazenar estados já visitados

        while pilha:
            estado_atual, caminho = pilha.pop()
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
                            pilha.append((novo_estado, novo_caminho))

        return None  

pilhas_inicial = [['c', 'b', 'a'], ['e', 'd'], ['g', 'f']]
pilhas_final = [[], ['f', 'g', 'd', 'b'], ['c', 'a', 'e']]

estoque = Estoque(pilhas_inicial, pilhas_final)

'''# Busca em Largura
caminho_largura = estoque.busca_em_largura()
if caminho_largura:
    print("Movimentos para atingir o estado final (Busca em Largura):")
    for movimento in caminho_largura:
        print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")
else:
    print("Não foi possível encontrar uma solução (Busca em Largura).")'''

# Busca em Profundidade
caminho_profundidade = estoque.busca_em_profundidade()
if caminho_profundidade:
    print("\nMovimentos para atingir o estado final (Busca em Profundidade):")
    for movimento in caminho_profundidade:
        print(f"Mover a caixa '{movimento[2]}' da pilha {movimento[0] + 1} para a pilha {movimento[1] + 1}")
else:
    print("Não foi possível encontrar uma solução (Busca em Profundidade).")
