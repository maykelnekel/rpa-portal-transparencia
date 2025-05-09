# crie um CustomError que herda de Exception
class CustomError(Exception):
    def __init__(self, mensagem, status_code):
        self.mensagem = mensagem
        self.status_code = status_code
