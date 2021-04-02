from classes.ConteudoMDB import ConteudoMDB
import eel

def criar_db(nome):
    criar = ConteudoMDB(nome)
    criar.tabela("tabela de teste")
    result = criar.insert({"criado": True})
    return result

def listar_dbs():
    listar = ConteudoMDB()
    result = listar.list_dbs()
    return result

def inserir(banco, document, tabela, muitos=False):

    inserirD = ConteudoMDB(banco)
    inserirD.tabela(tabela)
    result = inserirD.insert(document, muitos)

    if result == True:
        print("Inserido com sucesso!")
    else:
        print("Registro já existe!")

    eel.loginserirdisciplina(result)

    return result


def listartudo(banco, tabela):

    listarD = ConteudoMDB(banco)
    listarD.tabela(tabela)
    result = listarD.find_all()
    disciplinas = []

    if result == 0:
        return disciplinas
        print("Nenhuma disciplina encontrada")
    else:
        for r in result:
            disciplinas.append(r)
        print(disciplinas)
        return disciplinas


def remover(banco, tabela, documento):
    removerD = ConteudoMDB(banco)
    removerD.tabela(tabela)
    result = removerD.remove(documento)
    return result


def listar_tbs(banco, nome):
    listar = ConteudoMDB(banco)
    result = listar.list_tables(nome)
    return result

def criar_semana_insercao(banco, grupo_disciplinas, semana_a_ser_inserida):
    criar = ConteudoMDB(banco)
    criar.tabela(grupo_disciplinas)
    result = criar.montar_videos_da_semana(semana_a_ser_inserida)
    return result