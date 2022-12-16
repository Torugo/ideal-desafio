# Desafio Ideal

Esse repositório foi criado para a reprodução do desafio descrito [nesse repositório](https://github.com/idealctvm-administrator/backend-challenge-node)

Optou-se por desenvolver a solução utilizando a linguagem Pytyhon, bem como a biblioteca [flask-restful](https://flask-restful.readthedocs.io/en/latest/)

## Instruções de execução

A aplicação encontra se estruturada em dois containers Docker:

- Banco de dados PostgreSQL 14
- Aplicação Python/Flask

Essa decisão foi tomada considerando que em um ambiente de produção as duas aplicações costumam serem executadas em locais diferentes.

Para executar os containers basta executar o comando 

``docker-compose up -d``

O banco de dados estará disponivel na porta 5432 e o a API na porta 5050.

Durante o processo de build do container todas as tabelas do banco de dados serão criadas através do uso do ORM [SqlAlchemy](https://www.sqlalchemy.org/) e sua integração com o Flask. 

Dado a baixa complexidade das tabelas e das relações entre elas não foram desenvolvidos scripts para a criação manual das tabelas.

## Documentação

Para a documentação das rotas, optou-se por utilizar o padrão swagger. Para acessar a documentação basta acessar o endereço ``http://localhost:5050/apidocs`` com os containers ativos

## Pontos de melhoria

- Inclusão de testes: devido ao tempo de desenvolvimento do desafio, os testes não foram desenvolvidos.
- Melhor: Criação de rotas para alteração nos produtos cadastrados, diversos verbos disponiveis no protocolo http podem ser utilizados para a implementação dessas funcionalides.

