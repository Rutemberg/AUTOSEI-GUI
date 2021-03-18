# importando a classe Inserir_Conteudo
from classes.Conteudo import Inserir_Conteudo
from util.funcoes import *  # funcao de criacao de menu e pasta
from util.log import log  # funcao de criacao de logs.
from locale import LC_ALL, setlocale
import os
import sys
import eel
from datetime import datetime, timedelta

# funcao de insercao dos conteudos das disciplinas

def iniciar_insercao(disciplinas, configuracoes, opcao):
    agora = datetime.now()
    hora_inicial = agora.strftime("%d/%m/%Y %H:%M:%S")

    setlocale(LC_ALL, 'pt_BR.utf-8')

    # Se a opcao do menu for == 2 aramazenara o codigo em uma variavel
    # if opcao == 2:
    #     key = None
    #     while key == None:
    #         disciplina_codigo = int(input("Digite o código do conteúdo: "))
    #         # Pega a chave de um elemento da lista se o codigo digitado for encontrado
    #         key = next((index for (index, d) in enumerate(disciplinas)
    #                     if d["codigo_conteudo"] == disciplina_codigo), None)
    #         # Substitui a lista de disciplinas pela disciplina encontrada com a chave
    #         if key != None:
    #             log("app",
    #                 f"Disciplina: {disciplinas[key]['professor']} - {disciplinas[key]['nome_disciplina']} encontrada", "info")
    #             disciplinas = [disciplinas[key]]
    #         else:
    #             log("app",
    #                 f"Código de conteudo {disciplina_codigo} não encontrado", "warn")

    titulo_semana = configuracoes["semana"]
    pasta_atual = os.getcwd()  # Pega a localizacao da pasta atual

    if "S" in opcao:
        agora = datetime.now()
        hora_inicial = agora.strftime("%d/%m/%Y %H:%M:%S")
        # Funcao criar_pasta(nome, path) para criar pasta com o nome e a localizacao atual
        pasta_log = criar_pasta("logs", pasta_atual)
        pasta_semanas = criar_pasta(titulo_semana, pasta_log)

        arquivo = f"{pasta_semanas}\{titulo_semana}"
        Disciplinas_que_faltam = f"{pasta_semanas}\Disciplinas_que_faltam"
        arquivo_videos_sem_titulos = f"{pasta_semanas}\Videos_sem_temas"

        # Iniciar caso a resposta seja sim
        Processar = Inserir_Conteudo()
        Processar.abrir(configuracoes["site"])  # Abre o site
        # Loga com usuario e senha
        Processar.logar(configuracoes["usuario"], configuracoes["senha"])

        for disciplina in disciplinas:  # For para percorrer as disciplinas


            # Se nao houver videos e a opcao for 3 fara um log com as disciplinas que faltam
            # if [x for x in disciplina["videos"] if x['frame'] == ''] and opcao == 3:
            #     log(Disciplinas_que_faltam,
            #         f"*{disciplina['professor']}* - {disciplina['nome_disciplina']}", "warn", True)

            # Abre um arquivo de log e insere o titulo da disciplina
            log(arquivo,
                f"\n\n{disciplina['professor']} - {disciplina['nome_disciplina']}", "info", True)

            videos = True if [x for x in disciplina["videos"] if x['frame'] != ''] else False
            eel.timeline(disciplina['professor'], disciplina['nome_disciplina'], videos, disciplina['codigo_conteudo'])
            # Se existir videos para serem lançados prossiga com a inserção
            if [x for x in disciplina["videos"] if x['frame'] != '']:

                # Pesquisa a disciplina pela url e codigo
                Processar.pesquisar_conteudo(
                    configuracoes["url_conteudo"], disciplina["codigo_conteudo"])
                # Aguarda o carregamento do sistema
                Processar.aguardar_processo()
                # Seleciona a disciplina listada
                Processar.selecionar_disciplina()
                # Verifica se a semana em questão existe
                semana_existe = Processar.verificar_conteudo(
                    configuracoes["semana"])

                # Se a semana nao existir prossiga com a inserção
                if semana_existe == 0:
                    eel.logsemana(False, disciplina['codigo_conteudo'])
                    cont_titulo_video = 0
                    # Insere a semana
                    Processar.inserir_semana(configuracoes["semana"])
                    Processar.aguardar_processo()

                    for video in disciplina["videos"]:
                        cont_titulo_video += 1
                        numero_video = f"{cont_titulo_video:02d}"

                        if video["titulo"] != '':
                            titulo = video["titulo"]
                        else:
                            titulo = f'VIDEO {numero_video}'
                            log(arquivo_videos_sem_titulos,
                                f"*{disciplina['professor']}* - {disciplina['nome_disciplina']} - {titulo} sem tema", "warn", True, False)
                            log(arquivo,
                                f"{disciplina['professor']} - {disciplina['nome_disciplina']} - {titulo} sem tema", "warn")

                        # Adiciona o video
                        Processar.adicionar_video()
                        Processar.aguardar_processo()
                        # insere o video com titulo e frame
                        Processar.inserir_video(titulo, video["frame"])
                        Processar.aguardar_processo()

                        # Cria ou abre o log informando
                        log(arquivo, f"Video: {titulo} inserido", "info")
                        eel.logvideos(titulo, disciplina['codigo_conteudo'])
                        # Se a semana já existir
                else:
                    log(arquivo, f"{titulo_semana} já inserida !", "info")
                    eel.logsemana(True, disciplina['codigo_conteudo'])
            # Se não existir videos para serem lançados
            else:
                # Cria ou abre o log informando em dois arquivos
                log(Disciplinas_que_faltam,
                    f"*{disciplina['professor']}* - {disciplina['nome_disciplina']}", "warn", True, False, modo="w")
                log(arquivo, "Videos indisponiveis !", "warn")
    else:
        # sys.exit()
        pass

    agora = datetime.now()
    hora_final = agora.strftime("%d/%m/%Y %H:%M:%S")
    diferenca = tempo(hora_inicial, hora_final)
    print("\n")
    print("-"*50)
    log("app",f"\nTempo de execução - {diferenca}", "info", True)
    print("-"*50)
