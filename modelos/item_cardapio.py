class Produto:
    def __init__(self, nome, descricao, preco):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco

    def get_nome(self):
        return self.nome

    def get_descricao(self):
        return self.descricao

    def get_preco(self):
        return self.preco


class Bebida(Produto):
    def __init__(self, nome, descricao, preco):
        super().__init__(nome, descricao, preco)


class Lanche(Produto):
    def __init__(self, nome, descricao, preco):
        super().__init__(nome, descricao, preco)


class Sobremesa(Produto):
    def __init__(self, nome, descricao, preco):
        super().__init__(nome, descricao, preco)
