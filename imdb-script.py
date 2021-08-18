from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd

site = requests.get('https://m.imdb.com/feature/genre/?ref_=nv_ch_gr')


def pegar_link(reqs):
    all_links = []
    site = reqs.content
    html_categoria = BeautifulSoup(site, 'html.parser')
    div_images = html_categoria.findAll('div', attrs={'class': 'image'})
    for div_image in div_images:
        link1 = div_image.find('a')
        link1 = link1['href']
        site2 = requests.get(f'{link1}')
        site2 = site2.content
        html_next = BeautifulSoup(site2,'html.parser')
        selector_link = html_next.find('a',  attrs={'class': 'lister-page-next next-page'})
        link2 = 'https://www.imdb.com/' + selector_link['href']
        all_links.append([link1, link2])
    return all_links



def pegar_dados(info):
    dados = []
    for lista_links in info:
        for x in range(0, 2):
            link = requests.get(f'{lista_links[x]}')
            link = link.content
            site = BeautifulSoup(link, 'html.parser')
            filmes = site.findAll('div', attrs={'class': 'lister-item mode-advanced'})
            
            for filme in filmes:
                #Obtendo as tag dos valores
                cabecalho_filme = filme.find('h3', attrs={'class': 'lister-item-header'})
                ano_lancamento = cabecalho_filme.find('span', attrs={'class': 'lister-item-year text-muted unbold'})
                titulo = cabecalho_filme.find('a')
                descricao = filme.findAll('p', attrs={'class': 'text-muted'})[1]
                diretor = filme.find('p', attrs={'class': ''})
                genero = filme.find('span', attrs={'class': 'genre'})

                #tratando os erros antes de inserir na list
                if 'I' in ano_lancamento.text:
                    ano_lancamento = ano_lancamento.text[5:9]
                else:
                    ano_lancamento = ano_lancamento.text[1:5]

                if (filme.find('span', attrs={'name': 'nv'})):
                    votos = filme.find('span', attrs={'name': 'nv'})
                    votos = votos.text
                else:
                    votos = ''

                if (filme.find('strong')):
                    nota = filme.find('strong')
                    nota = nota.text
                else:
                    nota = ''
                

                if ('Director' in diretor.text):
                    new_diretor = ''
                    lista_diretor = diretor.text.split()
                    for x in range (1, len(lista_diretor)):
                        if lista_diretor[x] == '|':
                            break
                        else:
                            new_diretor += lista_diretor[x] + ' '
                    new_diretor.strip()
                else:
                    new_diretor = ''

                dados.append([titulo.text, ano_lancamento, descricao.text, nota, new_diretor, votos, genero.text ])
    return dados

link = pegar_link(site)
dados1 = pegar_dados(link)
df = pd.DataFrame(dados1, columns=['titulo', 'Ano lançamento', 'Descrição', 'Nota', 'Diretor', 'Votos', 'Genero'])
print(df)