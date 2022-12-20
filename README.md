# Ranked ML



Repositório destinado à criação de um modelo de Machine Learning com os dados da GC. A finalidade deste projeto é levar o conhecimento de Data Science e Analytics para o maior número de pessoas possível.


## Sumário
- [Motivação](#motivação)
- [Sobre o Curso](#sobre-o-curso)
- [Sobre o Professor](#sobre-o-professor)
- [Sobre os Dados](#sobre-os-dados)
- [Setup e requisitos](#setup-e-requisitos)
- [Calendário](#calendário)
- [FAQ](#faq)

## Motivação

Dentro de minhas capacidades, posso ajudar com estatística, dados e uma pitada de programação. Então vamos utilizar os dados da Gamers Club para atacar um problema de negócio em um projeto de Data Science de começo ao fim!

Acredito que exemplos são a maneira mais didática para cativar e incentivar.

Vale ressaltar que o mercado na área de Tecnlogia e Dados está extremamente aquecido! Muitas vagas são abertas diariamente no Linkedin e outras plataformas de recrutamento. O pessoal de dados é cada vez mais demandado.

## Sobre o Projeto

Algumas oportunidades que teremos de soluções para a GC:

1. Predição de jogadores que jogarão na próxima semana/mês
2. Predição de churn
3. Predição de assinatura
4. Predição churn de assinatura

Mas antes de debruçar no algoritmo, precisamos preparar os dados. Assim, passaremos pela criação de um book de variáveis (feature store) e posteriormente criar a nossa variável resposta (target), i.e. aquilo que queremos prever.

Pretendemos realizar este projeto para apresentar como um algoritmo por ajudar a resolver problemas reais de negócio. Bem como, passar pelas dificuldades e preparação de dados para desenvolver uma solução end-to-end.


## Sobre os dados

Para este Projeto utilizaremos dados de partidas que ocorreram nos servidores da Gamers Club. São partidas referentes à 2.500 jogadores, havendo mais de 30 estatísticas de seus partidas. Tais como Abates, Assistências, Mortes, Flash Assist, Head Shot, etc.

Alem disso, temos informações de medalhas destes players, como:
- Assinatura Premium, Plus
- Medalhas da Comunidade

Para ter uma melhor descrição destes dados, confira na [página oficial do Kaggle](https://www.kaggle.com/gamersclub/brazilian-csgo-plataform-dataset-by-gamers-club) onde os dados foram disponibilizados.

Abaixo temos o schema (relacionamentos) dos nossos dados.

<img src="https://user-images.githubusercontent.com/4283625/157664295-45b60786-92a4-478d-a044-478cdc6261d7.jpg" alt="" width="500">

## Setup e requisitos

### 1. Python / Anaconda

Você pode fazer o download do Python no site oficial: [www.python.org/](https://www.python.org/)

Como utilizaremos bibliotecas voltadas à análise de dados e modelagem, sera necessário realizar as instalações destas libs. Assim, por amor a simplicidade, eu recomendo fazer uso do [Anaconda](https://www.anaconda.com/).

A instalação do Anaconda é bem simples, só deve ficar atento em adicionar seu endereço à variável `PATH`.

### 2. Visual Studio Code

Esta ferramenta é uma interface de desenvolvimento. Não é necessária pois e apenas mais um sabor dentre tantos. Porém, como gosto bastante bastante, o curso será conduzido a partir da mesma.

Para instalar o [Visual Studio Code](https://code.visualstudio.com/) basta realizar o download na [página oficial](https://code.visualstudio.com/) da ferramenta e seguir os passos de instalação.

### 2. Dados

Como vamos utilizar os dados da GC, você precisa baixar estes dados de nossa pasta no [google drive](https://drive.google.com/file/d/1QR53whL3BCj6W9zawjMhGhFog-FbAySP/view?usp=sharing).

### 3. Conhecimentos técnicos

Faremos uso das seguintes bibliotecas:
- SQLalchemy
- Pandas
- Numpy
- Scikit-learn
- Feature-engine
- XGBoost
- Scikit-plot
- Yellowbrick

## Calendário

|Descrição|Data|VOD|
|---|:---:|:---:|
| 1. Introdução **Machine Learning** e Definição do problema 
| 2. Criação do book de Variáveis - Parte I 
| 3. Criação do book de Variáveis - Parte II 
| 4. Criação da ABT (*Analytical Base Table*) 
| 5. SEMMA e primeiro pipeline 
| 6. Tunning do melhor modelo 
| 7. Deploy | 28.04.22 

