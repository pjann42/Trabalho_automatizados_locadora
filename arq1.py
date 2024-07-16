import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime, timedelta

class Item:
    def __init__(self, id, titulo):
        self.id = id
        self.titulo = titulo
        self.disponivel = True

    def emprestar(self):
        if self.disponivel:
            self.disponivel = False
            print(f"O item '{self.titulo}' foi emprestado.")
        else:
            print(f"O item '{self.titulo}' não está disponível.")

    def devolver(self):
        if not self.disponivel:
            self.disponivel = True
            print(f"O item '{self.titulo}' foi devolvido.")
        else:
            print(f"O item '{self.titulo}' já está disponível.")

class Filme(Item):
    def __init__(self, id, titulo, diretor, duracao):
        super().__init__(id, titulo)
        self.diretor = diretor
        self.duracao = duracao

    def detalhes(self):
        disponibilidade = "disponível" if self.disponivel else "não disponível"
        print(f"Filme: {self.titulo} (ID: {self.id})")
        print(f"Diretor: {self.diretor}")
        print(f"Duração: {self.duracao} minutos")
        print(f"Disponibilidade: {disponibilidade}")

class Cliente:
    def __init__(self, nome):
        self.nome = nome
        self.filmes_emprestados = {}  # Dicionário para armazenar filmes e suas datas de empréstimo
        self.divida = False

    def emprestar_filme(self, filme):
        if filme.disponivel:
            filme.emprestar()
            data_emprestimo = datetime.now()
            self.filmes_emprestados[filme] = data_emprestimo
            print(f"Filme '{filme.titulo}' emprestado a {self.nome} em {data_emprestimo}.")
        else:
            print(f"Filme '{filme.titulo}' não está disponível para empréstimo.")

    def devolver_filme(self, filme):
        if filme in self.filmes_emprestados:
            filme.devolver()
            data_emprestimo = self.filmes_emprestados.pop(filme)
            tempo_com_filme = datetime.now() - data_emprestimo
            if tempo_com_filme > timedelta(days=7):
                self.divida = True
                print(f"{self.nome} está devendo por não devolver '{filme.titulo}' no prazo. Tempo com o filme: {tempo_com_filme.days} dias.")
            else:
                print(f"Filme '{filme.titulo}' devolvido por {self.nome} no prazo. Tempo com o filme: {tempo_com_filme.days} dias.")
        else:
            print(f"{self.nome} não tem o filme '{filme.titulo}' emprestado.")

    def listar_filmes_emprestados(self):
        if not self.filmes_emprestados:
            print(f"{self.nome} não tem filmes emprestados.")
        else:
            for filme, data_emprestimo in self.filmes_emprestados.items():
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
                for filme, data_emprestimo in cliente.filmes_emprestados.items():
                    tempo_com_filme = datetime.now() - data_emprestimo
                    dias_restantes = 7 - tempo_com_filme.days
                    data.append({
                        'Cliente': cliente.nome,
                        'Filme': filme.titulo,
                        'Data de Empréstimo': data_emprestimo,
                        'Tempo Restante (dias)': dias_restantes,
                        'Devedor': 'Sim' if tempo_com_filme > timedelta(days=7) else 'Não'
                    })
            else:
                data.append({
                    'Cliente': cliente.nome,
                    'Filme': None,
                    'Data de Empréstimo': None,
                    'Tempo Restante (dias)': None,
                    'Devedor': 'Não'
                })
        df = pd.DataFrame(data)
        return df

# Função para criar a interface gráfica
def mostrar_dataframe(df):
    root = tk.Tk()
    root.title("Informações dos Clientes")

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    root.mainloop()

# Exemplo de uso
# Criando uma locadora
locadora = Locadora()

# Adicionando filmes ao catálogo
filme1 = Filme(1, "Matrix", "Wachowskis", 136)
filme2 = Filme(2, "Inception", "Christopher Nolan", 148)

locadora.adicionar_filme(filme1)
locadora.adicionar_filme(filme2)

# Criando clientes
cliente1 = Cliente("João")
cliente2 = Cliente("Maria")

# Adicionando clientes à locadora
locadora.adicionar_cliente(cliente1)
locadora.adicionar_cliente(cliente2)

# Emprestando filmes aos clientes
cliente1.emprestar_filme(filme1)
cliente2.emprestar_filme(filme2)

# Criando e exibindo o DataFrame dos clientes e filmes emprestados antes da devolução
df_clientes = locadora.criar_dataframe_clientes()
print(df_clientes)

# Mostrar DataFrame na interface gráfica
mostrar_dataframe(df_clientes)
