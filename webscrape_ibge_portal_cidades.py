import requests
import json 
from datetime import datetime
import calendar
from time import sleep
from functools import reduce
from tqdm import tqdm
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

def get_url_estado():

    codigos_uf = open("codigo_uf.txt", "r", encoding="utf8")

    urls_api = []
    urls_api2 = []
    for cod_uf in codigos_uf:
        cod_uf = cod_uf.strip()
        url = f'https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/48981|62876|48985|25207|48982|28120|78187|78192|5908|5913|5929|5934|5950|5955|48986|62585|62590|95345|95379|59935|30255|28141|29749|21910|21906|21907|48980|95338/resultados/{cod_uf}'
        url2 = f'https://servicodados.ibge.gov.br/api/v1/biblioteca?aspas=3&coduf={cod_uf}'
       
        urls_api.append(url)
        urls_api2.append(url2)

    codigos_uf.close()

    return urls_api, urls_api2

def get_url_municipio():

    CODIGOS_MN = open("codigo_mun.txt", "r", encoding="utf8")

    urls_api = []
    urls_api2 = []
    urls_api3 = []
    for cod_mn in CODIGOS_MN:
        cod_mn = cod_mn.strip()
        cod_mn_6dig = cod_mn[0:6]
        url = f'http://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/29169|29170|29171|25207|29168|29765|29763|60036|60037|60045|78187|78192|5908|5913|5929|5934|5950|5955|47001|60048|30255|28141|29749|30279|60032|28242|95335|60030|60029|60031|93371|77861|82270|29167|87529|87530|91245|91247|91249|91251/resultados/{cod_mn_6dig}'
        #url para gentílico e outras informações
        url2 = f"http://servicodados.ibge.gov.br/api/v1/biblioteca?aspas=3&codmun={cod_mn_6dig}"

        url3 = f"http://servicodados.ibge.gov.br/api/v1/localidades/municipios/{cod_mn}"

        
        urls_api.append(url)
        urls_api2.append(url2)
        urls_api3.append(url3)


    CODIGOS_MN.close()

    return urls_api, urls_api2, urls_api3


def get_indicadores_uf(url, url2):
    req = requests.get(url, headers=headers).json()
    req2 = requests.get(url2, headers=headers).json()

    data_year = { 
            req[i]['id'] : list(req[i]['res'][0]['res'].keys())[-1]
            for i in range(0, len(req))
    }

    data_value = { 
            req[i]['id'] : list(req[i]['res'][0]['res'].values())[-1]
            for i in range(0, len(req))
    }

    data_value['Gentílico'] = list(req2[list(req2.keys())[0]].values())[0]
    data_value['Código do Estado'] = list(req[0]['res'][0].values())[0]
    data_value['Data de Extração'] = datetime.now().strftime("%Y/%m/%d")
    data_value['Hora de Extração'] = datetime.now().strftime("%H:%M:%S")

    return data_year, data_value

def get_indicadores_mun(url, url2, url3):

    req = requests.get(url, headers=headers).json()
    req2 = requests.get(url2, headers=headers).json()
    req3 = requests.get(url3, headers=headers).json()

    data_year = { 
            req[i]['id'] : list(req[i]['res'][0]['res'].keys())[-1]
            for i in range(0, len(req))
    }

    data_value = { 
            req[i]['id'] : list(req[i]['res'][0]['res'].values())[-1]
            for i in range(0, len(req))
    }

    data_value['Região'] = req3['microrregiao']['mesorregiao']['UF']['regiao']['nome']
    data_value['Sigla do Estado'] = req3['microrregiao']['mesorregiao']['UF']['sigla']
    data_value['Estado'] = req3['microrregiao']['mesorregiao']['UF']['nome']
    data_value['Código do Estado'] = req3['microrregiao']['mesorregiao']['UF']['id']
    data_value['Município'] = req3['nome']
    data_value['Código do Município'] = req3['id']
    data_value['Gentílico'] = req2[list(req2.keys())[0]]['GENTILICO']
    data_value['Histórico'] = req2[list(req2.keys())[0]]['HISTORICO']
    data_value['Data de Extração'] = datetime.now().strftime("%Y/%m/%d")
    data_value['Hora de Extração'] = datetime.now().strftime("%H:%M:%S")

    return data_year, data_value

def data_frame_uf(lista):
    append_data = []
    for i in range(len(lista)):
        data =  globals()['df_' + str(i)] = pd.DataFrame(lista[i]).T
        append_data.append(data)
    
    final_df = reduce(lambda  left,right: 
                      pd.merge(left, right, left_index=True, right_index=True, how='outer'), 
                      append_data)
    
    final_df.columns = range(final_df.shape[1])

    NOME_INDICADORES = open("NOME_INDICADORES_ESTADOS.txt", "r", encoding="utf8")
    df_nome = pd.read_csv(NOME_INDICADORES, sep=';')

    merge = df_nome.merge(final_df,
                left_on='id',
                right_index=True,
                how='right'
                )
    merge['nomeIndicador'] = merge['nomeIndicador'] + ' - ' + merge[0]
    merge['nomeIndicador'] = merge['nomeIndicador'].fillna(merge['id'])

    merge_copy = merge.copy()
    concat = pd.concat([merge_copy.iloc[:,0], merge_copy.iloc[:,[ x for x in range(3, merge_copy.shape[1], 2)]]], axis=1)
    
    concat = concat.T
    concat.columns = concat.iloc[0].to_list()
    concat = concat.iloc[1:,1:]

    # concat = concat.rename(columns={concat.columns[-1]:'Código do Estado'}, level=0)
    # concat = concat.rename(columns={concat.columns[-2]:'Gentílico'}, level=0)

    
    return concat  

def data_frame_mn(lista):

    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/aniversarios/?diade=0&mesde=0&diaate=0&mesate=0'
    req = requests.get(url).json()
    aniversario = pd.DataFrame(req)
    aniversario['mes'] = aniversario['mes'].apply(lambda x: calendar.month_name[x])
    aniversario['Aniversário'] = aniversario['dia'].astype(str) + ' de ' + aniversario['mes']
    aniversario = aniversario[['codigo','Aniversário']]
    aniversario['codigo'] = aniversario['codigo'].astype('int64')

    append_data = []
    for i in range(len(lista)):
        data =  globals()['df_' + str(i)] = pd.DataFrame(lista[i]).T
        append_data.append(data)
    
    final_df = reduce(lambda  left,right: 
                      pd.merge(left, right, left_index=True, right_index=True, how='outer'), 
                      append_data)
    
    final_df.columns = range(final_df.shape[1])

    NOME_INDICADORES = open("NOME_INDICADORES_MUNICIPIOS.txt", "r", encoding="utf8")
    df_nome = pd.read_csv(NOME_INDICADORES, sep=';')

    merge = df_nome.merge(final_df,
                left_on='id',
                right_index=True,
                how='right'
                )

    merge['nomeIndicador'] = merge['nomeIndicador'] + ' - ' + merge[0]
    merge['nomeIndicador'] = merge['nomeIndicador'].fillna(merge['id'])

    merge_copy = merge.copy()
    concat = pd.concat([merge_copy.iloc[:,0], merge_copy.iloc[:,[ x for x in range(3, merge_copy.shape[1], 2)]]], axis=1)
    
    concat = concat.T
    concat.columns = concat.iloc[0].to_list()
    concat = concat.iloc[1:,1:]

    concat['Código do Município - 2016_2'] = [x[0:6] for x in concat['Código do Município - 2016']]
    concat['Código do Município - 2016_2'] = concat['Código do Município - 2016_2'].astype('int64')

    concat2 = concat.merge(aniversario,
                left_on = 'Código do Município - 2016_2',
                right_on = 'codigo',
                how='left'
                )
    
    concat2 = concat2.drop(['codigo','Código do Município - 2016_2'], axis=1)

    # concat = concat.rename(columns={concat.columns[-1]:'Código do Estado'}, level=0)
    # concat = concat.rename(columns={concat.columns[-2]:'Gentílico'}, level=0)

    
    return concat2  

def organizar_colunas_estado(df):
    df_copy = df.copy()

    df_copy = df_copy[['Código do Estado', 'Governador - 2023', 'Gentílico', 'Capital - 2010',
                        'População estimada - 2021', 'População no último censo - 2010', 'Área urbanizada - 2019',
                        'Densidade demográfica - 2010', 'Área da unidade territorial - 2021', 'Matrículas no ensino médio - 2021',
                        'Docentes no ensino fundamental - 2021', 'Docentes no ensino médio - 2021', 'IDEB – Anos iniciais do ensino fundamental (Rede pública) - 2021',
                        'IDEB – Anos finais do ensino fundamental (Rede pública) - 2021', 'Número de estabelecimentos de ensino fundamental - 2021',
                        'Número de estabelecimentos de ensino médio - 2021', 'Depósitos a prazo - 2021', 'Depósitos à vista - 2021',
                        'Número de agências - 2021', 'Total de veículos - 2022', 'Receitas orçamentárias realizadas - 2017',
                        'Despesas orçamentárias empenhadas - 2017', 'Índice de Desenvolvimento Humano (IDH) - 2010',
                        'Rendimento nominal mensal domiciliar per capita - 2021', 'Pessoal ocupado na Administração pública, defesa e seguridade social - 2020',
                        'Pessoas de 16 anos ou mais ocupadas na semana de referência - 2016',
                        'Proporção de pessoas de 16 anos ou mais em trabalho formal, considerando apenas as ocupadas na semana de referência - 2016',
                        'Proporção de pessoas de 14 anos ou mais de idade, ocupadas na semana de referência em trabalhos formais - 2022',
                        'Rendimento médio real habitual do trabalho principal das pessoas de 14 anos ou mais de idade, ocupadas na semana de referência em trabalhos formais - 2022',
                        'Data de Extração', 'Hora de Extração']].sort_values(by=['Código do Estado'])


    num_col = ['Código do Estado', 'População estimada - 2021', 'População no último censo - 2010', 'Área urbanizada - 2019', 'Densidade demográfica - 2010',
                'Área da unidade territorial - 2021', 'Matrículas no ensino médio - 2021', 'Docentes no ensino fundamental - 2021', 'Docentes no ensino médio - 2021',
                'IDEB – Anos iniciais do ensino fundamental (Rede pública) - 2021', 'IDEB – Anos finais do ensino fundamental (Rede pública) - 2021',
                'Número de estabelecimentos de ensino fundamental - 2021', 'Número de estabelecimentos de ensino médio - 2021', 'Depósitos a prazo - 2021',
                'Depósitos à vista - 2021', 'Número de agências - 2021', 'Total de veículos - 2022', 'Receitas orçamentárias realizadas - 2017',
                'Despesas orçamentárias empenhadas - 2017', 'Índice de Desenvolvimento Humano (IDH) - 2010', 'Rendimento nominal mensal domiciliar per capita - 2021',
                'Pessoal ocupado na Administração pública, defesa e seguridade social - 2020', 'Pessoas de 16 anos ou mais ocupadas na semana de referência - 2016',
                'Proporção de pessoas de 16 anos ou mais em trabalho formal, considerando apenas as ocupadas na semana de referência - 2016',
                'Proporção de pessoas de 14 anos ou mais de idade, ocupadas na semana de referência em trabalhos formais - 2022']

    df_copy[num_col] = df_copy[num_col].replace('-','')
    df_copy[num_col] = df_copy[num_col].apply(pd.to_numeric)
    df_copy[num_col] = df_copy[num_col].replace('','-')

    df_copy[num_col] = df_copy[num_col].replace({99999999999991:0, 99999999999992:0,
                                                 99999999999993:0, 99999999999994:0,
                                                 99999999999995:0, 99999999999996:0,
                                                 99999999999997:0, 99999999999998:0,
                                                 99999999999999:0}) 
    

    return df_copy
    
def organizar_colunas_municipio(df):
    df_copy = df.copy()

    df_copy = df_copy[['Estado', 'Sigla do Estado', 'Código do Estado', 'Município',
                        'Código do Município - 2016', 'Aniversário', 'Prefeito - 2021', 'Gentílico',
                         'Região', 'Hierarquia urbana - 2018', 'Região de Influência - 2018',
                        'Região intermediária - 2021', 'Região imediata - 2021', 'Mesorregião - 2021',
                        'Microrregião - 2021', 'População estimada - 2021', 'População no último censo - 2010',
                        'População exposta ao risco - 2010', 'Densidade demográfica - 2010', 'Área urbanizada - 2019',
                        'Área da unidade territorial - 2021',  'IDEB – Anos iniciais do ensino fundamental (Rede pública) - 2021',
                        'IDEB – Anos finais do ensino fundamental (Rede pública) - 2021', 'Matrículas no ensino médio - 2021',
                        'Docentes no ensino fundamental - 2021', 'Docentes no ensino médio - 2021', 'Número de estabelecimentos de ensino fundamental - 2021',
                        'Número de estabelecimentos de ensino médio - 2021', 'Taxa de escolarização de 6 a 14 anos de idade - 2010',
                        'Estabelecimentos de Saúde SUS - 2009', 'Mortalidade Infantil - 2020', 'Internações por diarreia - 2016',
                        'PIB per capita - 2020', 'Pessoal ocupado - 2020', 'População ocupada - 2020', 'Total de receitas realizadas - 2017',
                        'Total de despesas empenhadas - 2017', 'Percentual da população com rendimento nominal mensal per capita de até 1/2 salário mínimo - 2010',
                        'Percentual das receitas oriundas de fontes externas - 2015', 'Salário médio mensal dos trabalhadores formais - 2020',
                        'Índice de Desenvolvimento Humano Municipal (IDHM) - 2010', 'Arborização de vias públicas - 2010',
                        'Esgotamento sanitário adequado - 2010', 'Urbanização de vias públicas - 2010', 'Bioma - 2019',
                        'Sistema Costeiro-Marinho - 2019','Histórico', 'Data de Extração', 'Hora de Extração']].sort_values(by=['Código do Município - 2016'])

    
    num_col = ['Código do Estado', 'Código do Município - 2016', 'População estimada - 2021',
                'População no último censo - 2010', 'População exposta ao risco - 2010', 'Densidade demográfica - 2010',
                'Área urbanizada - 2019', 'Área da unidade territorial - 2021',  'IDEB – Anos iniciais do ensino fundamental (Rede pública) - 2021',
                'IDEB – Anos finais do ensino fundamental (Rede pública) - 2021', 'Matrículas no ensino médio - 2021',
                'Docentes no ensino fundamental - 2021', 'Docentes no ensino médio - 2021', 'Número de estabelecimentos de ensino fundamental - 2021',
                'Número de estabelecimentos de ensino médio - 2021', 'Taxa de escolarização de 6 a 14 anos de idade - 2010', 'Estabelecimentos de Saúde SUS - 2009',
                'Mortalidade Infantil - 2020', 'Internações por diarreia - 2016', 'PIB per capita - 2020', 'Pessoal ocupado - 2020',
                'População ocupada - 2020', 'Total de receitas realizadas - 2017', 'Total de despesas empenhadas - 2017',
                'Percentual da população com rendimento nominal mensal per capita de até 1/2 salário mínimo - 2010',
                'Percentual das receitas oriundas de fontes externas - 2015', 'Salário médio mensal dos trabalhadores formais - 2020',
                'Índice de Desenvolvimento Humano Municipal (IDHM) - 2010', 'Arborização de vias públicas - 2010',
                'Esgotamento sanitário adequado - 2010', 'Urbanização de vias públicas - 2010']

    df_copy[num_col] = df_copy[num_col].replace('-','')
    df_copy[num_col] = df_copy[num_col].apply(pd.to_numeric)
    df_copy[num_col] = df_copy[num_col].replace('','-')

    df_copy[num_col] = df_copy[num_col].replace({99999999999991:0, 99999999999992:0,
                                                 99999999999993:0, 99999999999994:0,
                                                 99999999999995:0, 99999999999996:0,
                                                 99999999999997:0, 99999999999998:0,
                                                 99999999999999:0}) 
    
    return df_copy

def save_to_excel(df_uf, df_mun):

    """
        Função para salvar o data frame em tabela excel
    """
    date = datetime.now().strftime("%Y%m%d-%H-%M-%S")
    with pd.ExcelWriter('Extração-Informações-cidades-e-estados-IBGE-'+ date + '.xlsx') as writer:
        df_uf.to_excel(writer, sheet_name="UF", index=False )
        df_mun.to_excel(writer, sheet_name="MUN", index=False )

    print('\nParabéns, pesquisa salva!')

if __name__ == '__main__':
    urls_estado, url_estado2 = get_url_estado()
    urls_municipio, url_municipio2, url_municipio3 = get_url_municipio()


    dados_estados = []
    dados_municipios = []

    for i in tqdm(range(0, len(urls_estado))):
        url = urls_estado[i]
        url2 = url_estado2[i]

        ind_uf = get_indicadores_uf(url, url2)

        dados_estados.append(ind_uf)

    for i in tqdm(range(0, len(urls_municipio))):
        url = urls_municipio[i]
        url2 = url_municipio2[i]
        url3 = url_municipio3[i]

        ind_mun = get_indicadores_mun(url, url2, url3)


        dados_municipios.append(ind_mun)

    df_uf = data_frame_uf(dados_estados)
    df_mun = data_frame_mn(dados_municipios)

    df_uf_org = organizar_colunas_estado(df_uf)
    df_mun_org = organizar_colunas_municipio(df_mun)

    save_to_excel(df_uf_org, df_mun_org)