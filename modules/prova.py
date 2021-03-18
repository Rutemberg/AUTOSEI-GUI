from classes.Conteudo import Inserir_Prova
from util.funcoes import menu, criar_pasta
import os

def iniciar_insercao_prova(disciplinas, configuracoes, configuracao_prova):

    menu("Inserir Prova em todas as disciplinas", "Inserir prova em uma disciplina")
    opcao = int(input("Digite a opção: "))
    os.system("cls")

    if opcao == 2:
        key = None
        while key == None:
            disciplina_codigo = int(input("Digite o código do conteúdo: "))
            # Pega a chave de um elemento da lista se o codigo digitado for encontrado
            key = next((index for (index, d) in enumerate(disciplinas)
                        if d["codigo_conteudo"] == disciplina_codigo), None)
            # Substitui a lista de disciplinas pela disciplina encontrada com a chave
            if key != None:
                log("app",
                    f"Disciplina {disciplinas[key]['nome_disciplina']} encontrada", "info")
                disciplinas = [disciplinas[key]]
            else:
                log("app",
                    f"Código de conteudo {disciplina_codigo} não encontrado", "warn")

    iniciar = input("Iniciar (Sim/Nao): ")
    iniciar = iniciar.upper()

    titulo_semana = configuracao_prova["titulo_semana"]
    pasta_atual = os.getcwd()  # Pega a localizacao da pasta atual


    if "S" in iniciar:
        Prova = Inserir_Prova()
        Prova.abrir(configuracoes["site"])
        Prova.logar(configuracoes["usuario"], configuracoes["senha"])

        
        Prova.pesquisar_conteudo(configuracoes["url_conteudo"], 6)
        Prova.aguardar_processo()
        Prova.selecionar_disciplina()
        semana_existe = Prova.verificar_conteudo(configuracao_prova["titulo_semana"])

        if semana_existe == 0:
            Prova.inserir_semana(configuracao_prova["titulo_semana"])
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
            Prova.salvar_prova()


