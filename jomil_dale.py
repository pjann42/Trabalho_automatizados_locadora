class Estoque:
   
   # o topo da pilha é o final da lista
   # a caixa mais em baixo da pilha é o inicio da lista

    def __init__(self, pilhas):  
        self.pilhas = pilhas

    def mover_caixa(self, origem, destino):
        """Move uma caixa do topo da pilha de origem para o topo da pilha de destino."""
        if len(self.pilhas[origem]) > 0:
            caixa = self.pilhas[origem].pop()
            self.pilhas[destino].append(caixa)
        else:
            print(f"A pilha {origem + 1} está vazia. Não é possível mover caixas.")

    def exibir_pilhas(self):
        """Exibe o estado atual das pilhas."""
        for i, pilha in enumerate(self.pilhas):
            print(f"Pilha {i + 1}: {pilha}")

# Configuração inicial das pilhas
pilhas_inicial = [['c', 'b', 'a'], ['e', 'd'], ['g', 'f']]
estoque = Estoque(pilhas_inicial)

# Exibir o estado inicial das pilhas
print("Estado inicial das pilhas:")
estoque.exibir_pilhas()

# Exemplo de movimentação de caixas
estoque.mover_caixa(0, 1)  # Move a caixa do topo da pilha 1 para a pilha 2
estoque.mover_caixa(2, 0)  # Move a caixa do topo da pilha 3 para a pilha 1

# Exibir o estado final das pilhas
print("\nEstado final das pilhas após movimentações:")
estoque.exibir_pilhas()