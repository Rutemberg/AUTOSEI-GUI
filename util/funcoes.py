import os
import pathlib
from util.log import log
from datetime import datetime
import json


def menu(*args):
    os.system("cls")
    print(f"\nAUTOSEI\n\n")
    for key, item in enumerate(args):
        print(f"{key+1}. {item}")
    print(f"\n{len(args)+1}. Sair\n\n\n")
    
    return len(args)+1


def criar_pasta(nome_da_pasta, pasta_atual):
    caminho_pasta = os.path.join(pasta_atual, nome_da_pasta)
    if pathlib.Path(caminho_pasta).is_dir():
        log("app", f"A pasta {nome_da_pasta} já existe", "info")
        return caminho_pasta
    else:
        try:
            os.mkdir(caminho_pasta)
            log("app", f"Pasta {nome_da_pasta} criada", "info")
            return caminho_pasta
        except OSError as error:
            print(error)

def tempo(hora_inicial, hora_final):
    hora_inicial= datetime.strptime(hora_inicial, "%d/%m/%Y %H:%M:%S")
    hora_final = datetime.strptime(hora_final, "%d/%m/%Y %H:%M:%S")

    dif = hora_final - hora_inicial

    return dif

def abrir_arquivo_json(caminho):
    with open(caminho, encoding="utf8") as file:
        dados = file.read()
        dados = json.loads(dados)
        return dados
    
def listar_disciplinas(disciplinas):
    os.system("cls")
    print("\nDISCIPLINAS\n\n")
    for disciplina in disciplinas:
        print(
            f"{disciplina['professor']} - {disciplina['nome_disciplina']}\n")
    
    print("-"*50)
    print(f"\nTotal de disciplinas encontradas: {len(disciplinas)}\n\n")

    confirmar = input("Tecle enter para continuar...")