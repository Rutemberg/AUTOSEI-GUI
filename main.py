import eel
import json
from modules.conteudo import iniciar_insercao
from modules.conteudoMDB import *
# from modules.prova import iniciar_insercao_prova
from util.funcoes import *
import os

eel.init('HTMLS', allowed_extensions=['.js', '.html'])

# path = os.getcwd() + "/"
# semana = path + "semanateste.json"

# disciplinas = abrir_arquivo_json(semana)


@eel.expose
def inserir_documento(banco, document, tabela, muitos=False):
    return inserir(banco, document, tabela, muitos)


@eel.expose
def listar_documentos(banco, tabela="Nenhuma"):
    return listartudo(banco, tabela)


@eel.expose
def listar_bancos_de_dados():
    return listar_dbs()


@eel.expose
def remover_documentos(banco, tabela, document):
    return remover(banco, tabela, document)


@eel.expose
def listar_tabelas(banco, nome):
    return listar_tbs(banco, nome)


@eel.expose
def criar_banco(nome):
    return criar_db(nome)

@eel.expose
def carregar_disciplinas_para_insercao(banco, grupo_disciplinas, semana_a_ser_inserida):
    return criar_semana_insercao(banco, grupo_disciplinas, semana_a_ser_inserida)


@eel.expose
def carregar_disciplinas():
    return disciplinas


@eel.expose
def carregar_configuracoes():
    return configuracoes


@eel.expose
def insercao(disciplinas, configuracoes, titulosemana, opcao):
    iniciar_insercao(disciplinas, configuracoes, titulosemana, opcao)

# inserir("Rutemberg", disciplinas, "Disciplinas teste", True)

eel.start('index.html')
