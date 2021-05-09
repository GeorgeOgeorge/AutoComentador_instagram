from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

url_pagina = "https://www.amazon.com.br/s?k=box&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss"

conexao = urlopen(url_pagina)
pagina_final = soup(conexao.read(), "html.parser")
conexao.close()

arq_nome = "produtos.csv"
colunas = "nome,preço,avalição \n"
arq = open(arq_nome,"w")
arq.write(colunas)

produtos = pagina_final.findAll("div", {"data-component-type":"s-search-result"})

for produto in produtos:
    nome_produto = produto.h2.a.span.text
    try:
        avaliacao = produto.find("i", {"class":"a-icon-star-small"}).span.text.strip().replace(",",".")
    except:
        avaliacao = "Não possui"
    preco = produto.find("span", {"class":"a-offscreen"}).text.strip().replace(",",".")
    arq.write(str(nome_produto) + ", " + str(preco) + ", " + str(avaliacao) + "\n")

arq.close()
