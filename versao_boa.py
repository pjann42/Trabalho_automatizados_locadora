# Disciplina: Programação de sistemas automatizados
# Professor: Carlos  Montez
# Grupo: Pedro Luna, Vinicius Mendonça, Marcus Ferrari

# ---- Locadora de Filmes -----#

# Este projeto tem como objetivo simular o funcionamento de uma locadora de filmes onde são criadas 4 classes:

# Classe "item" : Essa classe possui alguns atributos básicos de filmes de uma locadora, além de métodos para aumentar e diminuir a quantidade de filmes disponíveis
# Classe "Filme": Essa classe herda alguns atributos da superclasse "item" e tem como objetivo detalhar quais são as características dos filmes
# Classe "Clientes" : Essa classe tem como objetivo criar os clientes e se relacionar com as outras classes com seus métodos no quesito emprestar, devolver e listar filmes
# Classe "Locadora" : Possivelmente a classe mais importante do projeto, possui duas listas como atributos (clientes e catálogo) onde são inseridas as informações importantes
# e diversos métodos que possibilitam a manipulação dos filmes dentro da locadora

# O projeto apresenta duas interfaces gráficas: Uma que mostra o relatório de quais filmes foram emprestados e outra que mostra os filmes disponíveis e quantidade.
# Ambas podem ser salvas como PDF

# Bibliotescas Utilizadas: 

# tkinter para interface gráfica
# pandas para criar dataframe com as informações
# matplot para salvar o PDF com os dados
# Módulo datetime para verificar a data e horário de locação

import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

class Item: #Principais características a métodos dos itens (Que é a superclasse de Filmes)

    def __init__(self, id, titulo, preco_aluguel, quantidade_disponivel): # Método Inicializador
        self.id = id 
        self.titulo = titulo
        self.preco_aluguel = preco_aluguel
        self.quantidade_disponivel = quantidade_disponivel
 
    def emprestar(self): # Empresta uma das unidades disponíveis, se houver.

        if self.quantidade_disponivel > 0: # Verifica se existem unidades disponíveis
            self.quantidade_disponivel -= 1 # Se houver, diminui 1 na quantidade
            print(f"O item '{self.titulo}' foi emprestado.") # Informao usuário
        else:
            print(f"O item '{self.titulo}' não está disponível.")

    def devolver(self): # Devolve uma das unidades, se houver.
        self.quantidade_disponivel += 1 # Acrescenta uma unidade nos filmes disponíveis
        print(f"O item '{self.titulo}' foi devolvido.")  # Informa o usuário se o filme foi devolvido

class Filme(Item): 
    
    def __init__(self, id, titulo, diretor, duracao, preco_aluguel, quantidade_disponivel):
        super().__init__(id, titulo, preco_aluguel, quantidade_disponivel) # Herda alguns atributos da classe "Item" além dos respectivos métodos

        self.diretor = diretor # Adiciona novos atributos 
        self.duracao = duracao

    def detalhes(self): # Detalhamento das informações do filme
        disponibilidade = "disponível" if self.quantidade_disponivel > 0 else "não disponível" # Verifica se o filme está disponível
        print(f"Filme: {self.titulo} (ID: {self.id})") # Nome do filme com seu respectivo identificador
        print(f"Diretor: {self.diretor}") # Diretor do filme 
        print(f"Duração: {self.duracao} minutos") # Duração do filme em minutos
        print(f"Preço de Aluguel: R${self.preco_aluguel:.2f}") # Preço do Aluguel
        print(f"Quantidade disponível: {self.quantidade_disponivel}") # Quantidade de filmes diponíveis
        print(f"Disponibilidade: {disponibilidade}") # informa o usuário se o filme está disponível

class Cliente: # Principais ações que o cliente pode realizar, conversando com as outras classes

    def __init__(self, nome):

        self.nome = nome
        self.filmes_emprestados = {} # Dicionário com os filmes emprestados

    def emprestar_filme(self, filme, tempo_devolucao): # esse método realiza efetivamente o emprestimo do filme

        if filme.quantidade_disponivel > 0:
            filme.emprestar() # Método da classe item acessado indiretamente por meio do objeto da classe Filme
            data_emprestimo = datetime.now() # horário e data da locação (Atual)
            self.filmes_emprestados[filme] = (data_emprestimo, tempo_devolucao) #Informações quanto ao tempo de devolução e data de emprestimo
            print(f"Filme '{filme.titulo}' emprestado a {self.nome} em {data_emprestimo}. Prazo de devolução: {tempo_devolucao} dias.") #Informa o usuário
        else:
            print(f"Filme '{filme.titulo}' não está disponível para empréstimo.")

    def devolver_filme(self, filme, tempo_demorado): # Mesma ideia de emprestar filme, mas para devolver e verifica se o usário está devendo 

        if filme in self.filmes_emprestados:
            filme.devolver() # Método da classe item acessado indiretamente por meio do objeto da classe Filme
            data_emprestimo, tempo_devolucao = self.filmes_emprestados.pop(filme)
            print(f"Filme '{filme.titulo}' devolvido por {self.nome}. Tempo que demorou para devolver: {tempo_demorado} dias.") # Informa o usuário
            if tempo_demorado > tempo_devolucao: # Verifica se o filme foi devolvido dentro do prazo
                print(f"{self.nome} está devendo por não devolver '{filme.titulo}' no prazo.") # informa o usuário
            else:
                print(f"Filme '{filme.titulo}' devolvido dentro do prazo.")
        else:
            print(f"{self.nome} não tem o filme '{filme.titulo}' emprestado.")

    def listar_filmes_emprestados(self): # Lista os filmes emprestados por um usuário

        if not self.filmes_emprestados:
            print(f"{self.nome} não tem filmes emprestados.")
        else:
            for filme, (data_emprestimo, _) in self.filmes_emprestados.items():
                tempo_com_filme = datetime.now() - data_emprestimo
                print(f"Filme: {filme.titulo}, Emprestado em: {data_emprestimo}, Tempo com o filme: {tempo_com_filme.days} dias") #informa o usuário

class Locadora: # Classe destinada as ações dentro da locadora

    def __init__(self): 

        self.catalogo = []
        self.clientes = []

    def adicionar_filme(self, filme): # Adiciona filme à lista do catálogo
        self.catalogo.append(filme)
        print(f"Filme '{filme.titulo}' adicionado ao catálogo.")
    
    def remover_filme(self, titulo): # Remove filme da lista do catálogo
        for filme in self.catalogo:
            if filme.titulo == titulo:
                self.catalogo.remove(filme)
                print(f"Filme '{titulo}' removido do catálogo.")
                return
        print(f"Filme '{titulo}' não encontrado no catálogo.")

    def listar_filmes(self): #Lista os filmes no catálogo
        if not self.catalogo:
            print("Nenhum filme no catálogo.")
        else:
            for filme in self.catalogo:
                filme.detalhes()

    def buscar_filme_por_titulo(self, titulo): # Busca filme por título no catálogo
        for filme in self.catalogo:
            if filme.titulo == titulo:
                print(f'O filme {filme.titulo} está no catálogo')
                return filme
            
        print(f"Filme '{titulo}' não encontrado no catálogo.")
        return None

    def adicionar_cliente(self, cliente): # Adiciona um cleinte a lista de clientes
        self.clientes.append(cliente)
        print(f"Cliente '{cliente.nome}' adicionado.")

    def listar_clientes(self): # Lista os clientes da lista clientes
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for cliente in self.clientes:
                print(f"Cliente: {cliente.nome}, Filmes emprestados: {len(cliente.filmes_emprestados)}")

    def criar_dataframe_clientes(self): # Cria um dataframe dos clientes com informações importantes acerca do aluguel dos filmes
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

    def criar_dataframe_filmes(self): # Cria um dataframe com as informações principais dos filmes do catálogo
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

    def salvar_pdf_clientes(self): # Salva um pdf do dataframe com as informações do cliente 
        df_clientes = self.criar_dataframe_clientes()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df_clientes.values, colLabels=df_clientes.columns, cellLoc='center', loc='center')
        plt.title("Informações dos Clientes")
        plt.savefig("informacoes_clientes.pdf", bbox_inches='tight')
        plt.close()
        print("PDF com informações dos clientes salvo como 'informacoes_clientes.pdf'.")

    def salvar_pdf_filmes(self): # Sala um pdf do dataframe com as informações dos filmes
        df_filmes = self.criar_dataframe_filmes()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df_filmes.values, colLabels=df_filmes.columns, cellLoc='center', loc='center')
        plt.title("Filmes Disponíveis")
        plt.savefig("filmes_disponiveis.pdf", bbox_inches='tight')
        plt.close()
        print("PDF com filmes disponíveis salvo como 'filmes_disponiveis.pdf'.")

# Funções para criar a interface gráfica de filmes disponíveis

def mostrar_filmes_disponiveis(): # Interface gráfica dos filmes disponíveis
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


def mostrar_informacoes_clientes():

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

filme2 = Filme(2, "Inception", "Christopher Nolan", 148, 7.50, 2)
filme3 = Filme(3, "Princesa da Ilha", "Tarantino", 120, 4.00, 5)
filme1 = Filme(1, "Matrix", "Wachowskis", 136, 20.00, 3)

locadora.remover_filme('Matrix')

locadora.adicionar_filme(filme1)
locadora.adicionar_filme(filme2)
locadora.adicionar_filme(filme3)

locadora.remover_filme('Matrix')

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

mostrar_informacoes_clientes()
