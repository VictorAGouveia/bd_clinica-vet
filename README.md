# Banco de Dados: Clínica Veterinária
Esse repositório contém os códigos para uma API de uma rede de clínicas veterinárias, onde são registrados pets, tutores, veterinários, atendimentos e clínicas, integrando todas as informações por meio de um banco de dados.
## Estrutura do código
O código do programa é estruturado seguindo o modelo representado abaixo.
```
├ /api
├ /models
├ /repositories
├ db.py
├ main.py
├ requirements.txt
└ swagger_template.json
```
- `/models` é a pasta contendo as classes que definem as tabelas do banco de dados, além de suas relações;
- `/repositories` é a pasta que contém os repositórios responsáveis por comunicar o programa com o banco de dados, criando funções intermediárias entre as classes e o programa;
- `/api` é a pasta que possui as definições de rotas da api, para acesso por protocolo `http` por meio da bilbioteca `Flask`;
- `db.py` é a parte do programa responsável por iniciar a comunicação com o banco de dados. **É recomendado alterar as informações de comunicação** *(endereço do banco de dados, credenciais...)* **aqui antes de executar o programa**;
- `main.py` é responsável por iniciar a API em `http://localhost:5000`, além de, quando executado, cria as tabelas *vazias* no banco de dados automaticamente;
- `requirements.txt` possui as bibliotecas python necessárias para execução da API;
- `swagger_template.json` contém as definições de exemplos que são mostrados na interface Swagger.
## Interface Swagger
O programa possui uma interface Swagger implementada por meio da biblioteca `Flasgger`, que pode ser acessada por meio de `http://127.0.0.1:5000/apidocs/`, por onde é possível testar todas as funcções implementadas na API de forma fácil e interativa.
