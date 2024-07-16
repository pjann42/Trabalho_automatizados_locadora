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

class Cliente:
    def __init__(self, nome):
        self.nome = nome
        self.filmes_emprestados = {}

    def emprestar_filme(self, filme, tempo_devolucao):
        if filme.quantidade_disponivel > 0:
            filme.emprestar()
            data_emprestimo = datetime.now()
            self.filmes_emprestados[filme] = (data_emprestimo, tempo_devolucao)

class Locadora:
    def __init__(self):
        self.catalogo = []
        self.clientes = []

    def adicionar_filme(self, filme):
        self.catalogo.append(filme)

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def criar_dataframe_clientes(self):
        data = []
        for cliente in self.clientes:
            for filme, (data_emprestimo, tempo_devolucao) in cliente.filmes_emprestados.items():
                data.append({
                    'Cliente': cliente.nome,
                    'Filme': filme.titulo,
                    'Data de Empréstimo': data_emprestimo,
                    'Prazo de Devolução (dias)': tempo_devolucao,
                    'Preço de Aluguel': filme.preco_aluguel
                })
        return pd.DataFrame(data)

    def criar_dataframe_filmes(self):
        data = []
        for filme in self.catalogo:
            data.append({
                'Filme': filme.titulo,
                'Diretor': filme.diretor,
                'Quantidade Disponível': filme.quantidade_disponivel,
                'Preço de Aluguel': filme.preco_aluguel
            })
        return pd.DataFrame(data)

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
locadora.adicionar_cliente(cliente1)
locadora.adicionar_cliente(cliente2)

# Emprestando filmes
cliente1.emprestar_filme(filme1, 7)

# Mostrar filmes disponíveis
mostrar_filmes_disponiveis()

# Salvar PDF com informações dos clientes
locadora.salvar_pdf_clientes()
