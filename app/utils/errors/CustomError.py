# crie um CustomError que herda de Exception
class CustomError(Exception):
    def __init__(self, mensagem, termo_da_busca, data_consulta):
        self.mensagem = mensagem
        self.termo_da_busca = termo_da_busca
        self.data_consulta = data_consulta
