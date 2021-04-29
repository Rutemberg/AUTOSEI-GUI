from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import sys


class Inserir_Conteudo:

    # Inicia o driver caso a resposta seja sim ou s
    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        # self.options.add_argument("headless")
        self.driver = Chrome(options=self.options)

    # abre o site pela url

    def abrir(self, url):
        self.driver.get(url)

    # Aguardar ate que a mensagem de loading suma
    def aguardar_processo(self):
        wait = WebDriverWait(self.driver, 300)
        # Aguarda até que o elemento(loading do sistema) suma da tela
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'rf-st-start')))

    # Loga no site usando o usuario e senha
    def logar(self, usuario, senha):
        # procura os elementos
        usuario_campo = self.driver.find_element_by_id("formLogin:username")
        senha_campo = self.driver.find_element_by_id("formLogin:senha")
        # Insere os valores nos campos
        usuario_campo.send_keys(usuario)
        senha_campo.send_keys(senha)
        # Procura o botao e clica
        logar = self.driver.find_element_by_id("formLogin:btLogin")
        logar.click()

    # Pesquisa o conteudo
    def pesquisar_conteudo(self, url_conteudo, codigo_conteudo):
        self.driver.get(url_conteudo)  # navegue ate a url
        # Usando o select encontra o elemento select do html
        consultar_por = Select(self.driver.find_element_by_id("form:consulta"))
        # Seleciona o valor
        consultar_por.select_by_value("codigoConteudo")

        self.aguardar_processo()

        # Consulta pelo codigo do conteudo
        valor_consulta = self.driver.find_element_by_id("form:valorConsulta")
        valor_consulta.clear()  # limpa o campo
        valor_consulta.send_keys(codigo_conteudo)  # Escreve o codigo
        # Clica no botao consultar
        consultar = self.driver.find_element_by_id("form:consultar")
        consultar.click()

    # Seleciona e clica na disciplina encontrada, somente a primeira e unica encontrada
    def selecionar_disciplina(self):
        click_disciplina = self.driver.find_element_by_id(
            "form:items:0:descricao")
        click_disciplina.click()

    # Verifica pelo texto se o conteudo existe
    def verificar_conteudo(self, elem):
        conteudo_existe = self.driver.find_elements_by_link_text(f"{elem}")
        return len(conteudo_existe)

    # Insere o titulo da semana
    def inserir_semana(self, semana):
        titulo_unidade = self.driver.find_element_by_id(
            "form:unidadeConteudoTitulo")  # Pega o input pelo id
        titulo_unidade.send_keys(semana)  # Digita o valor
        adicionar = self.driver.find_element_by_xpath(
            "//*[@id='form:j_idt595']")  # pega o botao
        adicionar.click()  # clica para salvar

    # Adiciona pegando a ultima semana inserida
    def adicionar_video(self):
        video = self.driver.find_elements_by_xpath(
            "//*[@title='Adicionar Página']")[-1].get_attribute("id")
        self.driver.execute_script(
            f'document.getElementById("{video}").click()')

    # Insere os videos por titulo e frame
    def inserir_video(self, titulo, frame):

        # Script para inserir o valor em um documento por innerHTML
        self.driver.execute_script(
            'document.getElementsByClassName("cke_wysiwyg_frame cke_reset")[0].contentDocument.body.innerHTML = ' + f'`<iframe src="https://player.vimeo.com/video/{frame}" width="640" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>`')

        # Escreve o titulo no input encontrado
        titulo_video = self.driver.find_element_by_id("formNovaPagina:titulo")
        titulo_video.send_keys(titulo)

        self.driver.execute_script(
            'document.getElementById("formNovaPagina:salvar").click()')


class Inserir_Prova(Inserir_Conteudo):

    def __init__(self):
        super().__init__()

    def adicionar_prova(self):
        self.driver.find_elements_by_xpath(
            "//*[@title='Adicionar Página']")[-1].click()

    def inserir_informaçoes(self, titulo, informacao):

        # Script para inserir o valor em um documento por innerHTML
        self.driver.execute_script(
            'document.getElementsByClassName("cke_wysiwyg_frame cke_reset")[0].contentDocument.body.innerHTML = ' + f"`{informacao}`")

        # Escreve o titulo no input encontrado
        titulo_prova = self.driver.find_element_by_id("formNovaPagina:titulo")
        titulo_prova.send_keys(titulo)

        self.driver.execute_script(
            'document.getElementById("formNovaPagina:salvar").click()')

    def editar_conteudo(self):
        self.driver.find_elements_by_xpath(
            "//*[@title='Editar']")[-1].click()

    def adicionar_avaliacao_online(self):
        self.driver.find_element_by_id("form:addPosterior").click()
        id_elemento = self.driver.find_elements_by_xpath(
            "//*[@title='Avalição Online']")[-1].get_attribute("id")
        self.driver.execute_script(
            f'document.getElementById("{id_elemento}").click()')

    def adicionar_valor_por_id(self, id_elemento, valor):
        input_valor = self.driver.find_element_by_id(id_elemento)
        input_valor.send_keys(valor)

    def adicionar_valor_por_path(self, path, valor):
        input_valor = self.driver.find_element_by_xpath(path)
        input_valor.send_keys(valor)

    def selecionar_opcao(self, id_elemento, valor):
        selecionar_por = Select(self.driver.find_element_by_id(id_elemento))
        selecionar_por.select_by_value(valor)

    def selecionar_assunto(self):
        assunto = self.driver.find_elements_by_tag_name("select")[-2].get_attribute("name")
        selecionar_por = Select(self.driver.find_element_by_name(assunto))
        selecionar_por.select_by_value("75")


    def selecionar_opcao_por_nome(self, nome_elemento, valor):
        selecionar_por = Select(
            self.driver.find_element_by_name(nome_elemento))
        selecionar_por.select_by_value(valor)

    def click_opcao_id(self, id_elemento):
        selecionar = self.driver.find_element_by_id(id_elemento)
        selecionar.click()

    def inserir_descricao(self, descricao):
        self.driver.execute_script(
            f'document.getElementById("formAddRecursoEducacional:textoAvaliacaoOnline").innerHTML = `{descricao}`')

    def limpar_campo(self, id_elemento):
        limpar = self.driver.find_element_by_id(id_elemento)
        limpar.clear()

    def questoes(self, nivel, qtd, valor):
        if nivel == "facil":
            dificuldade = "formAddRecursoEducacional:quantidadeNivelQuestaoFacil"
            valor_por_q = "formAddRecursoEducacional:notaPorQuestaoNivelFacil"
        elif nivel == "medio":
            dificuldade = "formAddRecursoEducacional:quantidadeNivelQuestaoMedio"
            valor_por_q = "formAddRecursoEducacional:notaPorQuestaoNivelMedio"

        elif nivel == "dificil":
            id_elemento = self.driver.find_element_by_xpath(
                "/html/body/div[1]/div[2]/table/tbody/tr/td/table/tbody/tr[17]/td/div/div[2]/div[4]/div/form/div[2]/div[1]/div/div[2]/table[1]/tbody/tr[1]/td[2]/span/input").get_attribute("id")
            dificuldade = id_elemento
            valor_por_q = "formAddRecursoEducacional:notaPorQuestaoNivelDificil"

        self.driver.execute_script(f'''document.getElementById("{dificuldade}").value = {qtd};
  document.getElementById("{valor_por_q}").value = "{valor}";
  document.getElementById("{dificuldade}").onchange();''')

    def xpath_click_script(self, path):
        elemetoid = self.driver.find_element_by_xpath(
            f"{path}").get_attribute("id")
        self.driver.execute_script(
            f'document.getElementById("{elemetoid}").click()')

    def verificar_questoes(self):
        try:
            questoes = self.driver.find_element_by_xpath(
                "/html/body/div[6]/div[4]/div/form/div/div/table/tbody/tr[1]/td/div/span").text
            self.xpath_click_script("/html/body/div[6]/div[3]/input")
            self.aguardar_processo()
            self.xpath_click_script("/html/body/div[6]/div[3]/input")
            self.aguardar_processo()

            return {"texto": questoes, "tipo": "info"}

        except exceptions.NoSuchElementException:
            questoes = self.driver.find_element_by_xpath(
                "/html/body/div[6]/div[4]/div/form/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td").text
            self.xpath_click_script("/html/body/div[6]/div[3]/input")
            self.aguardar_processo()
            return {"texto": questoes, "tipo": "warn"}
    
    def salvar_prova(self):
        id_elemento = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/table/tbody/tr/td/table/tbody/tr[17]/td/div/div[2]/div[4]/div/form/table[2]/tbody/tr[3]/td/table/tbody/tr/td/input[1]").get_attribute("id")
        self.driver.execute_script(
            f'document.getElementById("{id_elemento}").click()')
    def salvar(self):
        id_elemento = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/table/tbody/tr/td/table/tbody/tr[29]/td/form/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr/td/input[2]").get_attribute("id")
        self.driver.execute_script(
            f'document.getElementById("{id_elemento}").click()')
