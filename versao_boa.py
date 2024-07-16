
import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

class Item:
    def __init__(self, id, titulo, preco_aluguel, quantidade_disponivel):
        self.id = id
        self.titulo = titulo
        self.preco_aluguel = preco_aluguel
        self.quantidade_disponivel = quantidade_disponivel

    def emprestar(self):
        if self.quantidade_disponivel > 0:
            self.quantidade_disponivel -= 1
            print(f"O item '{self.titulo}' foi emprestado.")
        else:
            print(f"O item '{self.titulo}' não está disponível.")

    def devolver(self):
        self.quantidade_disponivel += 1
        print(f"O item '{self.titulo}' foi devolvido.")

class Filme(Item):
    
    def __init__(self, id, titulo, diretor, duracao, preco_aluguel, quantidade_disponivel):
        super().__init__(id, titulo, preco_aluguel, quantidade_disponivel)

        self.diretor = diretor
        self.duracao = duracao

    def detalhes(self):
        disponibilidade = "disponível" if self.quantidade_disponivel > 0 else "não disponível"
        print(f"Filme: {self.titulo} (ID: {self.id})")
        print(f"Diretor: {self.diretor}")
        print(f"Duração: {self.duracao} minutos")
        print(f"Preço de Aluguel: R${self.preco_aluguel:.2f}")
        print(f"Quantidade disponível: {self.quantidade_disponivel}")
        print(f"Disponibilidade: {disponibilidade}")

class Cliente:
    def __init__(self, nome):
        self.nome = nome
        self.filmes_emprestados = {}

    def emprestar_filme(self, filme, tempo_devolucao):
        if filme.quantidade_disponivel > 0:
            filme.emprestar()
            data_emprestimo = datetime.now()
            self.filmes_emprestados[filme] = (data_emprestimo, tempo_devolucao)
            print(f"Filme '{filme.titulo}' emprestado a {self.nome} em {data_emprestimo}. Prazo de devolução: {tempo_devolucao} dias.")
        else:
            print(f"Filme '{filme.titulo}' não está disponível para empréstimo.")

    def devolver_filme(self, filme, tempo_demorado):
        if filme in self.filmes_emprestados:
            filme.devolver()
            data_emprestimo, tempo_devolucao = self.filmes_emprestados.pop(filme)
            print(f"Filme '{filme.titulo}' devolvido por {self.nome}. Tempo que demorou para devolver: {tempo_demorado} dias.")
            if tempo_demorado > tempo_devolucao:
                print(f"{self.nome} está devendo por não devolver '{filme.titulo}' no prazo.")
            else:
                print(f"Filme '{filme.titulo}' devolvido dentro do prazo.")
        else:
            print(f"{self.nome} não tem o filme '{filme.titulo}' emprestado.")

    def listar_filmes_emprestados(self):
        if not self.filmes_emprestados:
            print(f"{self.nome} não tem filmes emprestados.")
        else:
            for filme, (data_emprestimo, _) in self.filmes_emprestados.items():
                tempo_com_filme = datetime.now() - data_emprestimo
                print(f"Filme: {filme.titulo}, Emprestado em: {data_emprestimo}, Tempo com o filme: {tempo_com_filme.days} dias")

class Locadora:

    def __init__(self):

        self.catalogo = []
        self.clientes = []

    def adicionar_filme(self, filme):
        self.catalogo.append(filme)
        print(f"Filme '{filme.titulo}' adicionado ao catálogo.")

    def listar_filmes(self):
        if not self.catalogo:
            print("Nenhum filme no catálogo.")
        else:
            for filme in self.catalogo:
                filme.detalhes()

    def buscar_filme_por_titulo(self, titulo):
        for filme in self.catalogo:
            if filme.titulo == titulo:
                print(f'O filme {filme.titulo} está no catálogo')
                return filme
            
        print(f"Filme '{titulo}' não encontrado no catálogo.")
        return None

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)
        print(f"Cliente '{cliente.nome}' adicionado.")

    def listar_clientes(self):
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for cliente in self.clientes:
                print(f"Cliente: {cliente.nome}, Filmes emprestados: {len(cliente.filmes_emprestados)}")

    def criar_dataframe_clientes(self):
        data = []
        for cliente in self.clientes:
            if cliente.filmes_emprestados:
                for filme, (data_emprestimo, tempo_devolucao) in cliente.filmes_emprestados.items():
                    data.append({
                        'Cliente': cliente.nome,
                        'Filme': filme.titulo,
                        'Data de Empréstimo': data_emprestimo,
                        'Prazo de Devolução (dias)': tempo_devolucao,
                        'Preço de Aluguel': filme.preco_aluguel
                    })
            else:
                data.append({
                    'Cliente': cliente.nome,
                    'Filme': None,
                    'Data de Empréstimo': None,
                    'Prazo de Devolução (dias)': 7,
                    'Preço de Aluguel': 0.0
                })
        df = pd.DataFrame(data)
        return df

    def criar_dataframe_filmes(self):
        data = []
        for filme in self.catalogo:
            data.append({
                'Filme': filme.titulo,
                'Diretor': filme.diretor,
                'Quantidade Disponível': filme.quantidade_disponivel,
                'Preço de Aluguel': filme.preco_aluguel
            })
        df = pd.DataFrame(data)
        return df

    def salvar_pdf_clientes(self):
        df_clientes = self.criar_dataframe_clientes()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df_clientes.values, colLabels=df_clientes.columns, cellLoc='center', loc='center')
        plt.title("Informações dos Clientes")
        plt.savefig("informacoes_clientes.pdf", bbox_inches='tight')
        plt.close()
        print("PDF com informações dos clientes salvo como 'informacoes_clientes.pdf'.")

    def salvar_pdf_filmes(self):
        df_filmes = self.criar_dataframe_filmes()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df_filmes.values, colLabels=df_filmes.columns, cellLoc='center', loc='center')
        plt.title("Filmes Disponíveis")
        plt.savefig("filmes_disponiveis.pdf", bbox_inches='tight')
        plt.close()
        print("PDF com filmes disponíveis salvo como 'filmes_disponiveis.pdf'.")

# Função para criar a interface gráfica de filmes disponíveis

def mostrar_filmes_disponiveis():
    root = tk.Tk()
    root.title("Filmes Disponíveis")

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    df_filmes = locadora.criar_dataframe_filmes()
    tree = ttk.Treeview(frame, columns=list(df_filmes.columns), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    for col in df_filmes.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    for index, row in df_filmes.iterrows():
        tree.insert("", tk.END, values=list(row))

    btn_salvar_pdf = ttk.Button(frame, text="Salvar como PDF", command=locadora.salvar_pdf_filmes)
    btn_salvar_pdf.pack(pady=10)

    root.mainloop()

# Função para criar a interface gráfica para as informações dos clientes
def mostrar_dataframe():
    root = tk.Tk()
    root.title("Informações dos Clientes")

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    df_clientes = locadora.criar_dataframe_clientes()
    tree = ttk.Treeview(frame, columns=list(df_clientes.columns), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    for col in df_clientes.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    for index, row in df_clientes.iterrows():
        tree.insert("", tk.END, values=list(row))

    btn_salvar_pdf = ttk.Button(frame, text="Salvar como PDF", command=locadora.salvar_pdf_clientes)
    btn_salvar_pdf.pack(pady=10)

    root.mainloop()

# Exemplo de uso
locadora = Locadora()

# Adicionando filmes ao catálogo
filme1 = Filme(1, "Matrix", "Wachowskis", 136, 5.00, 3)
filme2 = Filme(2, "Inception", "Christopher Nolan", 148, 7.50, 2)
filme3 = Filme(3, "Princesa da Ilha", "Tarantino", 120, 4.00, 5)

locadora.adicionar_filme(filme1)
locadora.adicionar_filme(filme2)
locadora.adicionar_filme(filme3)

# Criando clientes
cliente1 = Cliente("João")
cliente2 = Cliente("Maria")

# Adicionando clientes à locadora
locadora.adicionar_cliente(cliente1)
locadora.adicionar_cliente(cliente2)

locadora.buscar_filme_por_titulo('Matrix')

locadora.listar_filmes()

# Emprestando filmes aos clientes com o tempo de devolução
cliente1.emprestar_filme(filme1, 7)  # 7 dias
cliente2.emprestar_filme(filme2, 5)  # 5 dias
cliente1.emprestar_filme(filme3, 10) # 10 dias
cliente2.emprestar_filme(filme1, 3)  # 3 dias
cliente1.devolver_filme(filme3, 2)   # Devolveu em 2 dias

# Mostrar a nova interface gráfica com filmes disponíveis
mostrar_filmes_disponiveis()

# Mostrar a interface gráfica para as informações dos clientes
mostrar_dataframe()
