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


class Locadora:
    def __init__(self):
        self.catalogo = []

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
