# WebScraping do Portal Cidades do IBGE

![GitHub](https://img.shields.io/github/license/rvidals/WebScraping-Portal-Cidades-IBGE)

Dando continuidade aos meus estudo de Web Scraping, optei por capturar dados da API do portal [Cidades](https://cidades.ibge.gov.br/brasil/df/panorama), me inspirando no script desenvolvido para capturar informações da API do Shoppe e gerando uma planinha com diversas informações dos anúncios presentes na pesquisa. Ou seja, um simples exercício/diversão na programação pode ajudar no desenvolvimento de um script robusto e necessário, sobretudo para atualizar um base de dados que pode ser visitada com frequencia no intuito de subsidiar pesquisas de diferentes contextos. 

Diferente do painel [Cidades e Estados](https://www.ibge.gov.br/cidades-e-estados/df/brasilia.html) - no meu git há um [script]() que faz paspagem dos dados contidos nele, vale a pena conferir -, o  portal [IBGE-Cidades](https://cidades.ibge.gov.br/), possui uma diversidade superior de indicadores para todos os Estados e Municípios do Brasil, o que de falto torna-o uma fonte oficial e fundamental de dados para pesquisa.


<details>
  <summary>
    São cerca de 49 indicadores presentes no nível municipal: 
  </summary>
<ul>
<li>Estado</li>
<li>Sigla do Estado</li>
<li>Código do Estado</li>
<li>Município</li>
<li>Código do Município - 2016</li>
<li>Aniversário</li>
<li>Prefeito - 2021</li>
<li>Gentílico</li>
<li>Região</li>
<li>Hierarquia urbana - 2018</li>
<li>Região de Influência - 2018</li>
<li>Região intermediária - 2021</li>
<li>Região imediata - 2021</li>
<li>Mesorregião - 2021</li>
<li>Microrregião - 2021</li>
<li>População estimada - 2021</li>
<li>População no último censo - 2010</li>
<li>População exposta ao risco - 2010</li>
<li>Densidade demográfica - 2010</li>
<li>Área urbanizada - 2019</li>
<li>Área da unidade territorial - 2021</li>
<li>IDEB – Anos iniciais do ensino fundamental (Rede pública) - 2021</li>
<li>IDEB – Anos finais do ensino fundamental (Rede pública) - 2021</li>
<li>Matrículas no ensino médio - 2021</li>
<li>Docentes no ensino fundamental - 2021</li>
<li>Docentes no ensino médio - 2021</li>
<li>Número de estabelecimentos de ensino fundamental - 2021</li>
<li>Número de estabelecimentos de ensino médio - 2021</li>
<li>Taxa de escolarização de 6 a 14 anos de idade - 2010</li>
<li>Estabelecimentos de Saúde SUS - 2009</li>
<li>Mortalidade Infantil - 2020</li>
<li>Internações por diarreia - 2016</li>
<li>PIB per capita - 2020</li>
<li>Pessoal ocupado - 2020</li>
<li>População ocupada - 2020</li>
<li>Total de receitas realizadas - 2017</li>
<li>Total de despesas empenhadas - 2017</li>
<li>Percentual da população com rendimento nominal mensal per capita de até 1/2 salário mínimo - 2010</li>
<li>Percentual das receitas oriundas de fontes externas - 2015</li>
<li>Salário médio mensal dos trabalhadores formais - 2020</li>
<li>Índice de Desenvolvimento Humano Municipal (IDHM) - 2010</li>
<li>Arborização de vias públicas - 2010</li>
<li>Esgotamento sanitário adequado - 2010</li>
<li>Urbanização de vias públicas - 2010</li>
<li>Bioma - 2019</li>
<li>Sistema Costeiro-Marinho - 2019</li>
<li>Histórico</li>
<li>Data de Extração</li>
<li>Hora de Extração</li>
</ul>
</details>


<details>
  <summary>
    São cerca de 30 indicadores presentes no nível Estadual: 
  </summary>
<ul>
<li>Código do Estado</li>
<li>Governador - 2023</li>
<li>Gentílico</li>
<li>Capital - 2010</li>
<li>População estimada - 2021</li>
<li>População no último censo - 2010</li>
<li>Área urbanizada - 2019</li>
<li>Densidade demográfica - 2010</li>
<li>Área da unidade territorial - 2021</li>
<li>Matrículas no ensino médio - 2021</li>
<li>Docentes no ensino fundamental - 2021</li>
<li>Docentes no ensino médio - 2021</li>
<li>IDEB – Anos iniciais do ensino fundamental (Rede pública) - 2021</li>
<li>IDEB – Anos finais do ensino fundamental (Rede pública) - 2021</li>
<li>Número de estabelecimentos de ensino fundamental - 2021</li>
<li>Número de estabelecimentos de ensino médio - 2021</li>
<li>Depósitos a prazo - 2021</li>
<li>Depósitos à vista - 2021</li>
<li>Número de agências - 2021</li>
<li>Total de veículos - 2022</li>
<li>Receitas orçamentárias realizadas - 2017</li>
<li>Despesas orçamentárias empenhadas - 2017</li>
<li>Índice de Desenvolvimento Humano (IDH) - 2010</li>
<li>Pessoal ocupado na Administração pública, defesa e seguridade social - 2020</li>
<li>Pessoas de 16 anos ou mais ocupadas na semana de referência - 2016</li>
<li>Proporção de pessoas de 16 anos ou mais em trabalho formal, considerando apenas as ocupadas na semana de referência - 2016</li>
<li>Proporção de pessoas de 14 anos ou mais de idade, ocupadas na semana de referência em trabalhos formais - 2022</li>
<li>Rendimento médio real habitual do trabalho principal das pessoas de 14 anos ou mais de idade, ocupadas na semana de referência em trabalhos formais - 2022</li>
<li>Data de Extração</li>
<li>Hora de Extração</li>
</ul>
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


