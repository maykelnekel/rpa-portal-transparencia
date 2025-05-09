# RPA Portal da Transparência

## Descrição

Este projeto é um Robô de Processamento de Atividades (RPA) que automatiza a coleta de dados de pessoa física do [Portal da Transparência](https://portaldatransparencia.gov.br/pessoa/visao-geral). O objetivo é fornecer uma forma eficiente e escalável de coletar dados de interesse público.

## Funcionalidades

- Coleta de dados de pessoa física do Portal da Transparência, através do nome, CPF ou NIS
- Filtro por beneficiário de programa social
- Retorno de dados em formato JSON

## Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic.dev/)
- [Playwright](https://playwright.dev/)
- [Patchright](https://pypi.org/project/patchright/)

## Documentação

**Essa api foi documentada com Swagger.**

[Clique aqui para acessar a documentação](https://rpa-portal-transparencia.onrender.com/docs)

Se estiver rodando a API localmente, você terá acesso à documentação através do endpoint `/docs`. Deverá conseguir acessar em [localhost:8000/docs](localhost:8000/docs)

## Instalação

1. Clone o repositório: `git clone https://github.com/maykelnekel/rpa-portal-transparencia.git`

2. Crie e entre no ambiente venv:

   - Linux/Mac: `python3 -m venv venv && source venv/bin/activate`
   - Windows: `python -m venv venv && venv\Scripts\activate.bat`

3. Instale as dependências: `pip install -r requirements.txt`

   3.1. Talvez você precise instalar o **Chromium-Driver** para o **Patchright**. Caso seja necessário execute: `patchright install chromium`

4. Execute o projeto: `uvicorn main:app --reload`
