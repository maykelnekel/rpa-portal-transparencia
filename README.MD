# RPA Portal da Transparência

## Descrição

Este projeto é um uma API, que gerencia um RPA para automatizar a coleta de dados de pessoa física do [Portal da Transparência](https://portaldatransparencia.gov.br/pessoa/visao-geral). O objetivo é fornecer uma forma eficiente e escalável de coletar dados de interesse público.

A API conta com um deploy realizado na plataforma [Render](https://render.com), porém está no tier free. Portanto a primeira requisição à API depois de um longo período sem acessos, pode levar até 50 segundo. Isso ocorre pois no tier free os serviços entram automaticamente em modo de hibernação.

Além disso, o poder de processamento da máquina no tier free é baixo, o que pode causar lentidões e instabilidades.

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

5. **Feito!**

## Postman

Nesse repositório você encontrará um arquivo chamado [rpa-p-t.postman_collection.json](rpa-p-t.postman_collection.json).

Ele contém uma coleção base para o Postman, pré definida com endpoints e dados úteis para os testes.

Além disso, esses endpoints também possuem **testes básicos de integração**, utilizando a ferramenta de testes do Postman.

### Configurando a coleção

1.  Acesse o postman através da sua plataforma de preferência

2.  Crie ou acesse um workspace

3.  Na aba `Collections`. Clique no botão `import` que aparece à direita do nome do seu workspace e importe o arquivo mencionado anteriormente

4.  Na aba `Environments` crie um novo enviroment contendo:

    4.1. **base_url**: sendo a **url base da api** + sufixo **/api/v1**.

         localhost:8000/api/v1

    4.3. você também pode utilizar a versão em produção,

          https://rpa-portal-transparencia.onrender.com/api/v1

5.  **Feito!**

## Considerações finais

Esse projeto foi desenvolvido com o único intuito de apresentar habilidades de desenvolvimento e resolução de problemas. Sem quaisquer iniciativas ou incentivo a danos à plataforma do governo a que se aplica.

Para mais informaçõesb, você pode me contatar através do [meu linkedin](https://www.linkedin.com/in/maykelnekel/).
