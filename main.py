import eel
import json
from modules.conteudo import iniciar_insercao
# from modules.prova import iniciar_insercao_prova
from util.funcoes import *
import os

eel.init('HTMLS', allowed_extensions=['.js', '.html'])

path = os.getcwd() + "/config/"
config = path + "config.json"
semana = path + "semana.json"

configuracoes = abrir_arquivo_json(config)
disciplinas = abrir_arquivo_json(semana)


@eel.expose
def carregar_disciplinas():
    return disciplinas

@eel.expose
def carregar_configuracoes():
    return configuracoes

@eel.expose
def insercao(opcao):
    iniciar_insercao(disciplinas, configuracoes, opcao)


eel.start('index.html')  