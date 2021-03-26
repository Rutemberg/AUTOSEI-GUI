from classes.ConteudoMDB import ConteudoMDB
import eel

def inserir(document, tabela):
    
    inserirD = ConteudoMDB("AutoSEI")
    inserirD.tabela(tabela)
    result = inserirD.insert(document)

    if result == True:
        print("Inserido com sucesso!")
    else:
        print("Registro já existe!")
    
    eel.loginserirdisciplina(result)

    return result
    
def listartudo(tabela):
    
    listarD = ConteudoMDB("AutoSEI")
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
    

    