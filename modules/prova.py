from classes.Conteudo import Inserir_Prova
from util.funcoes import *
from config.prova import configuracao_prova
import os
from util.log import log
from locale import LC_ALL, setlocale
from datetime import datetime, timedelta


def iniciar_insercao_prova(disciplinas, configuracoes, iniciar, configuracao_prova=configuracao_prova):

    setlocale(LC_ALL, 'pt_BR.utf-8')

    agora = datetime.now()
    hora_inicial = agora.strftime("%d/%m/%Y %H:%M:%S")

    titulo_semana = configuracao_prova["titulo_semana"]
    pasta_atual = os.getcwd()  # Pega a localizacao da pasta atual

    pasta_log = criar_pasta("logs", pasta_atual)
    pasta_semanas = criar_pasta(titulo_semana, pasta_log)
    arquivo = f"{pasta_semanas}\{titulo_semana}"

    if "S" in iniciar:
        Prova = Inserir_Prova()
        Prova.abrir(configuracoes["site"])
        Prova.logar(configuracoes["usuario"], configuracoes["senha"])


        for disciplina in disciplinas:
            
            log(arquivo,f"\n\n{disciplina['professor']} - {disciplina['nome_disciplina']}", "info", True)
            Prova.pesquisar_conteudo(configuracoes["url_conteudo"], disciplina['codigo_conteudo'])
            Prova.aguardar_processo()
            Prova.selecionar_disciplina()
            semana_existe = Prova.verificar_conteudo(configuracao_prova["titulo_semana"])

            if semana_existe == 0:
                Prova.inserir_semana(configuracao_prova["titulo_semana"])
                Prova.aguardar_processo()
                Prova.selecionar_assunto()
                Prova.salvar()
                Prova.aguardar_processo()
                Prova.adicionar_prova()
                Prova.aguardar_processo()
                Prova.inserir_informaçoes(configuracao_prova["titulo_da_prova"], configuracao_prova["conteudo_apresentacao"])
                Prova.aguardar_processo()
                Prova.editar_conteudo()
                Prova.adicionar_avaliacao_online()
                Prova.aguardar_processo()
                Prova.adicionar_valor_por_id("formAddRecursoEducacional:tituloRE", configuracao_prova["titulo_da_prova"])

                # Tipo Geração	
                Prova.selecionar_opcao("formAddRecursoEducacional:politicaSelecaoQuestao", "QUESTOES_ASSUNTO_UNIDADE")
                Prova.aguardar_processo()

                # Política de Seleção de Questão	

                # Regra de Distribuição de Questão	

                # Parâmetros de Monitoramento das Avaliações	
                Prova.selecionar_opcao_por_nome("formAddRecursoEducacional:j_idt1102", "1")
                Prova.aguardar_processo()

                # Acertos Considerar Aprovado	
                Prova.adicionar_valor_por_path('//*[@id="formAddRecursoEducacional:panelAvaliacaoOnline"]/table/tbody/tr[5]/td[2]/input', configuracao_prova["acertos"])

                # Tempo Limite Realização Avaliação On-line (Em Minutos)
                Prova.adicionar_valor_por_id("formAddRecursoEducacional:tempoLimiteRealizacaoAvaliacaoOnline", configuracao_prova["tempo"])

                # Regra Definição Período Liberação Avaliação On-line	
                Prova.selecionar_opcao("formAddRecursoEducacional:regraDefinicaoPeriodoAvaliacaoOnline", "CALENDARIO_LANCAMENTO_NOTA")
                Prova.aguardar_processo()
                
                # Nº Dias Entre Avaliação On-line (Dias)		

                # Nº Vezes Pode Repetir Avaliação On-line	

                # Variável Nota Padrão Avaliação On-line	
                Prova.selecionar_opcao("formAddRecursoEducacional:variavelNotaPadraoAvaliacaoOnline", "A1")

                # Permitir Repetições De Questões A Partir Da Segunda Avaliação On-line Do Aluno	
                Prova.click_opcao_id("formAddRecursoEducacional:permiteRepeticoesDeQuestoesAPartirSegundaAvaliacaoOnlineAluno")

                # Apresentar a Nota da Questão Na Visão do Aluno	

                # Permite Aluno Avançar Conteúdo Sem o REA esta Realizado.	
                Prova.click_opcao_id("formAddRecursoEducacional:permiteAlunoAvancarConteudoSemLancarNotaReaAvaliacaoOnline")
                # Limitar o Tempo da Prova Dentro do Período de Realização	

                # Apresentar Gabarito da Prova do Aluno Após a Data do Período de Realização	

                # Descrição / Orientação
                Prova.inserir_descricao(configuracao_prova["descricao"])

                # Randômico Por Complexidade Da Questão
                # Qtde. Questões Medianas
                Prova.questoes(configuracao_prova["dificuldade"], configuracao_prova["qnt_de_questoes"], configuracao_prova["valor_por_questao"])
                Prova.aguardar_processo()

                #Simular prova e obter resposta
                #Clica em simular avaliacao
                Prova.xpath_click_script("/html/body/div[1]/div[2]/table/tbody/tr/td/table/tbody/tr[17]/td/div/div[2]/div[4]/div/form/table[2]/tbody/tr[3]/td/table/tbody/tr/td/input[2]")
                Prova.aguardar_processo()

                #Clica na segunda tela de simular avaliacao
                Prova.xpath_click_script("/html/body/div[6]/div[4]/div/form/div/input")
                Prova.aguardar_processo()

                #Verificar as questoes
                questoes = Prova.verificar_questoes()
                log(arquivo, f"{questoes['texto']}", "info")   


                if questoes["tipo"] == "info":
                    Prova.salvar_prova()
                    log(arquivo, f"Prova inserida com sucesso!", "info")
                else:
                    log(arquivo, f"Prova não inserida!", "warn")
                
            else:
                log(arquivo, f"{titulo_semana} já inserida !", "info")

    agora = datetime.now()
    hora_final = agora.strftime("%d/%m/%Y %H:%M:%S")
    diferenca = tempo(hora_inicial, hora_final)
    print("\n")
    print("-"*50)
    log(arquivo,f"\nTempo de execução - {diferenca}", "info", True)
    log("app",f"\nTempo de execução - {diferenca}", "info", True, False)
    print("-"*50)