# WebScraping do Portal Cidades do IBGE

![GitHub](https://img.shields.io/github/license/rvidals/WebScraping-Portal-Cidades-IBGE)

Dando continuidade aos meus estudo de Web Scraping, optei por capturar dados da API do portal [Cidades](https://cidades.ibge.gov.br/brasil/df/panorama), me inspirando no script desenvolvido para capturar informações da API do Shoppe e gerando uma planinha com diversas informações dos anúncios presentes na pesquisa. Ou seja, um simples exercício/diversão na programação pode ajudar no desenvolvimento de um script robusto e necessário, sobretudo para atualizar um base de dados que pode ser visitada com frequencia no intuito de subsidiar pesquisas de diferentes contextos. 

Diferente do painel [Cidades e Estados](https://www.ibge.gov.br/cidades-e-estados/df/brasilia.html) - no meu git há um [script]() que faz paspagem dos dados contidos nele, vale a pena conferir -, o  portal [IBGE-Cidades](https://cidades.ibge.gov.br/), possui uma diversidade superior de indicadores para todos os Estados e Municípios do Brasil, o que de falto torna-o uma fonte oficial e fundamental de dados para pesquisa.


<details>
  <summary>
    São cerca de 49 indicadores presentes no nível municipal: 
  </summary>
  1.  Estado
2.  Sigla do Estado
3.  Código do Estado
4.  Município
5.  Código do Município - 2016
6.  Aniversário
7.  Prefeito - 2021
8.  Gentílico
9.  Região
10.  Hierarquia urbana - 2018
11.  Região de Influência - 2018
12.  Região intermediária - 2021
13.  Região imediata - 2021
14.  Mesorregião - 2021
15.  Microrregião - 2021
16.  População estimada - 2021
17.  População no último censo - 2010
18.  População exposta ao risco - 2010
19.  Densidade demográfica - 2010
20.  Área urbanizada - 2019
21.  Área da unidade territorial - 2021
22.  IDEB – Anos iniciais do ensino fundamental (Rede pública) - 2021
23.  IDEB – Anos finais do ensino fundamental (Rede pública) - 2021
24.  Matrículas no ensino médio - 2021
25.  Docentes no ensino fundamental - 2021
26.  Docentes no ensino médio - 2021
27.  Número de estabelecimentos de ensino fundamental - 2021
28.  Número de estabelecimentos de ensino médio - 2021
29.  Taxa de escolarização de 6 a 14 anos de idade - 2010
30.  Estabelecimentos de Saúde SUS - 2009
31.  Mortalidade Infantil - 2020
32.  Internações por diarreia - 2016
33.  PIB per capita - 2020
34.  Pessoal ocupado - 2020
35.  População ocupada - 2020
36.  Total de receitas realizadas - 2017
37.  Total de despesas empenhadas - 2017
38.  Percentual da população com rendimento nominal mensal per capita de até 1/2 salário mínimo - 2010
39.  Percentual das receitas oriundas de fontes externas - 2015
40.  Salário médio mensal dos trabalhadores formais - 2020
41.  Índice de Desenvolvimento Humano Municipal (IDHM) - 2010
42.  Arborização de vias públicas - 2010
43.  Esgotamento sanitário adequado - 2010
44.  Urbanização de vias públicas - 2010
45.  Bioma - 2019
46.  Sistema Costeiro-Marinho - 2019
47.  Histórico
48.  Data de Extração
49.  Hora de Extração
</details>


<details>
  <summary>
    São cerca de 30 indicadores presentes no nível Estadual: 
  </summary>
1.  Código do Estado
2.  Governador - 2023
3.  Gentílico
4.  Capital - 2010
5.  População estimada - 2021
6.  População no último censo - 2010
7.  Área urbanizada - 2019
8.  Densidade demográfica - 2010
9.  Área da unidade territorial - 2021
10.  Matrículas no ensino médio - 2021
11.  Docentes no ensino fundamental - 2021
12.  Docentes no ensino médio - 2021
13.  IDEB – Anos iniciais do ensino fundamental (Rede pública) - 2021
14.  IDEB – Anos finais do ensino fundamental (Rede pública) - 2021
15.  Número de estabelecimentos de ensino fundamental - 2021
16.  Número de estabelecimentos de ensino médio - 2021
17.  Depósitos a prazo - 2021
18.  Depósitos à vista - 2021
19.  Número de agências - 2021
20.  Total de veículos - 2022
21.  Receitas orçamentárias realizadas - 2017
22.  Despesas orçamentárias empenhadas - 2017
23.  Índice de Desenvolvimento Humano (IDH) - 2010
24.  Pessoal ocupado na Administração pública, defesa e seguridade social - 2020
25.  Pessoas de 16 anos ou mais ocupadas na semana de referência - 2016
26.  Proporção de pessoas de 16 anos ou mais em trabalho formal, considerando apenas as ocupadas na semana de referência - 2016
27.  Proporção de pessoas de 14 anos ou mais de idade, ocupadas na semana de referência em trabalhos formais - 2022
28.  Rendimento médio real habitual do trabalho principal das pessoas de 14 anos ou mais de idade, ocupadas na semana de referência em trabalhos formais - 2022
29.  Data de Extração
30.  Hora de Extração
</details>




Um ponto importante é que que além de fazer a raspagem é possível fazer um tratamento básico nos dados, como converter dados do tipo objeto para numérico, utilizando basicamente a biblioteca pandas. Esse tipo de tratamento é importantíssimo, visto que ao salvar esses dados em uma tabela de banco de dados, é importante especificar o tipo de dado e até o seu tamanho, para não prejudicar o desempenho do banco. É claro não é o foco desse código, porém é importante considerar esse ponto.

# Sobre o projeto

A ideia é rodar o algoritmo de seis em seis meses ou ano a ano e assim gerar um relatório com essas informações, visto que não mudam com tanta frequencia. Assim,  dados atualizados para gerar esses indicadores são realizados por exemplo a partir do censo demográfico, que é gerado de 10 em 10 anos, resultado eleitoral de 4 a 4 anos e estimativa populacional é anual.

# Bibliotecas Utilizadas
- [Requests](https://requests.readthedocs.io/en/latest/)
- [Datetime](https://docs.python.org/3/library/datetime.html)
- [locale](https://docs.python.org/pt-br/3.8/library/locale.html)
- [Pandas](https://pandas.pydata.org/)
- [json](https://docs.python.org/pt-br/3/library/json.html)
- [Calendar](https://docs.python.org/3/library/calendar.html)
- [Functools](https://docs.python.org/3/library/functools.html)
- [tqdm](https://tqdm.github.io/)

# Autor
Rogerio Vidal de Siqueira

<a href="https://www.linkedin.com/in/rogerio-vidal-de-siqueira-9478aa136/" target="_blank" rel="noopener noreferrer">Meu Linkdin</a>


