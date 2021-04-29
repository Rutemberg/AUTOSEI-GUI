eel.expose(timeline);
eel.expose(logvideos);
eel.expose(logsemana);
eel.expose(relatoriofinal);

var infodisciplinas = [];
var titulovideos = [];
var semana = [];
var dadosr = [];

function timeline(nome, disciplina, video, codigo) {
  //   console.log(nome, disciplina, video, codigo);
  infodisciplinas.push({
    nome,
    disciplina,
    video,
    codigo,
  });
}

function logvideos(titulo, codigo) {
  //   console.log(titulo, codigo);
  titulovideos.push({ titulo, codigo });
}

function logsemana(inserida, codigo) {
  // console.log("Inserida: " + inserida + " Codigo : " + codigo);
  semana.push({ inserida, codigo });
}

function relatoriofinal(
  tempo,
  totaldisciplinas,
  totalvideos,
  totalDinseridas,
  faltam,
  data
) {
  // console.log(tempo, totaldisciplinas, totalvideos, totalDinseridas, faltam);
  dadosr.push({
    tempo,
    totaldisciplinas,
    totalvideos,
    totalDinseridas,
    faltam,
    data,
    _id: ID(),
  });
  // console.log(dadosr);
}

function scrolltobottom() {
  let element = document.getElementById("app");
  element.scrollIntoView({ behavior: "instant", block: "end" });
}

var ID = function () {
  return Math.random().toString(26).substr(2, 9);
};

new Vue({
  el: "#app",
  vuetify: new Vuetify(),
  data: {
    progressocountdisciplinas: 0,
    indexcarousel: 0,
    botaofecharrelatorio: true,
    e6: 0,
    disabled: false,
    listaconfiguracoescadastradas: [],
    bancos: [],
    bancoselecionado: "",
    nomebanco: "",
    nometabela: "",
    tabelas: [],
    semanas: [],
    nomesemana: "",
    disciplinasselecionadas: "",
    windowHeight: window.innerHeight,
    alert: {
      on: false,
      message: "",
      type: "",
      color: "",
    },
    titulosemana: "",
    video: {
      _id: "",
      titulo: "",
      frame: "",
    },
    videos: [],
    videoparacadastrar: {},
    vervideos: false,
    listadevideos: [],
    semana: false,
    disciplinassemana: [],
    disciplinaselecionada: [],
    disciplinassemanaparacadastrar: [],
    listadisciplinas: [],
    formularioinsercao: false,
    formulariobanco: false,
    tabeladisciplina: "",
    camposDisciplina: {
      _id: "",
      nome_disciplina: "",
      codigo_disciplina: "",
      codigo_conteudo: "",
      professor: "",
    },
    camposconfiguracao: {
      _id: ID(),
      site: "https://sei.institutoprocessus.com.br/",
      url_conteudo:
        "https://sei.institutoprocessus.com.br/visaoAdministrativo/ead/conteudoCons.xhtml",
      usuario: "",
      senha: "",
    },
    dialogconfirmarinsercao: false,
    dialoglistadisciplinas: false,
    dialoginsercao: false,
    dialogbanco: false,
    dialog: false,
    dialogRelatorio: false,
    dialogconfiguracoes: false,
    dialogvervideos: false,
    fab: false,
    fab2: false,
    titulo: false,
    power: 0,
    appbar: false,
    menu: true,
    timeline: false,
    progresso: false,
    colorbar: "#762051",
    disciplinas: [],
    qtddisciplinas: 0,
    configuracoes: [],
    items: [],
    logDisciplinas: infodisciplinas,
    logVideos: titulovideos,
    semanainserida: semana,
    dadosrelatorio: dadosr,
  },
  async mounted() {
    let bancos = await eel.listar_bancos_de_dados()();
    this.bancos = bancos;
    var main = document.getElementById("app");
    main.style.display = "block";
    this.titulo = true;
    this.appbar = true;
    window.addEventListener("resize", this.onResize);
    setTimeout(() => {
      this.dialogbanco = true;
    }, 500);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    verlistadevideos(lista, disciplinaselecionada) {
      this.listadevideos = lista;
      this.dialogvervideos = true;
      this.disciplinaselecionada = disciplinaselecionada;
      this.e6 = 0;
    },
    async removerconfiguracoes() {
      let d = await eel.remover_documentos(
        this.bancoselecionado,
        "Configuracoes",
        this.camposconfiguracao
      )();

      if (d > 0) {
        this.camposconfiguracao.usuario = "";
        this.camposconfiguracao.senha = "";

        this.alertar(
          true,
          "Configuração removida com sucesso",
          "mdi-check-bold",
          "success"
        );
        await this.carregarconfiguracoes();
      }
    },
    async inserirconfiguracoes() {
      if (this.validarcampos(this.camposconfiguracao) == true) {
        this.camposconfiguracao._id = ID();
        let result = await eel.inserir_documento(
          this.bancoselecionado,
          this.camposconfiguracao,
          "Configuracoes"
        )();
        if (result == true) {
          this.alertar(
            true,
            "Configuracão adicionada!",
            "mdi-check-bold",
            "success"
          );
          this.dialogconfiguracoes = false;
          await this.carregarconfiguracoes();
        } else {
          this.alertar(true, "Configuracão adicionada!", "alert", "error");
        }
      } else {
        this.alertar(true, "Existem campos em branco!", "mdi-alert", "warning");
      }
    },
    fechardialoginsercao() {
      this.dialoginsercao = false;
      this.disciplinas = [];
    },
    async carregarbanco(banco) {
      this.bancoselecionado = banco;
      await this.carregarconfiguracoes();
      let semanas = await eel.listar_tabelas(this.bancoselecionado, "semana")();
      this.semanas = semanas.reverse();

      await this.listartabelas();
      this.dialogbanco = false;
    },
    async carregarconfiguracoes() {
      this.camposconfiguracao.usuario = "";
      this.camposconfiguracao.senha = "";
      let configuracoes = await eel.listar_documentos(
        this.bancoselecionado,
        "Configuracoes"
      )();
      this.listaconfiguracoescadastradas = configuracoes;
      this.configuracoes = configuracoes[0];
      if (configuracoes.length > 0) {
        this.camposconfiguracao = configuracoes[0];
        this.disabled = true;
      } else {
        this.disabled = false;
      }
    },
    async listartabelas() {
      let tabelas = await eel.listar_tabelas(this.bancoselecionado, "disci")();
      this.tabelas = tabelas;
    },
    async salvarbanco() {
      if (this.nomebanco != "") {
        let banco = await eel.criar_banco(this.nomebanco)();

        if (banco == true) {
          let bancos = await eel.listar_bancos_de_dados()();
          this.bancos = bancos;
          this.alertar(
            true,
            "Banco inserido com sucesso!",
            "mdi-database-check",
            "success"
          );
          this.formulariobanco = false;
          this.nomebanco = "";
          this.dialogbanco = true;
        }
      } else {
        this.alertar(
          true,
          "Nome do banco vazio",
          "mdi-database-remove",
          "error"
        );
      }
    },
    onResize() {
      this.windowHeight = window.innerHeight;
    },
    async carregardisciplinas() {
      try {
        let disciplinas = await eel.carregar_disciplinas()();
        this.disciplinas = disciplinas;
      } catch (e) {
        console.error(e);
      }
      this.dialog = true;
    },
    async carregarsemana(tabela) {
      try {
        disciplinas = await eel.listar_documentos(
          this.bancoselecionado,
          tabela
        )();
        this.disciplinassemana = disciplinas;
        this.semana = true;
        this.nometabela = tabela;
        await this.listartabelas();
        this.alertar(
          true,
          `Encontradas ${disciplinas.length} disciplinas`,
          "mdi-check-bold",
          "info"
        );
      } catch (e) {
        console.error(e);
      }
    },
    validarcampos: function (arr) {
      valida = true;
      for (var item in arr) {
        if (arr[item] == "") {
          valida = false;
        }
      }
      return valida;
    },
    contar: function (array) {
      return array.length;
    },
    contarvideos: function (arr, faltam) {
      qnt = 0;
      arr.forEach((a) => {
        if (a.videos.length > "" && faltam == false) {
          qnt += a.videos.length;
        } else if (a.videos.length == 0 && faltam == true) {
          qnt += 1;
        }
      });
      return qnt;
    },
    iniciar: function (codigo = null) {
      let disciplinas = [];

      if (codigo != null) {
        let resultado = this.disciplinas.filter((obj) => {
          return obj.codigo_conteudo === codigo;
        });
        disciplinas = resultado;
      } else {
        disciplinas = this.disciplinas;
      }

      this.progressocountdisciplinas = this.contar(disciplinas);

      eel.insercao(disciplinas, this.configuracoes, this.nomesemana, "Sim")();
      this.dialoginsercao = false;
      this.dialogvervideos = false;
      this.timeline = true;
      this.menu = false;
      this.colorbar = "transparent";
      this.progresso = true;
      this.dialogconfirmarinsercao = false;

      // console.log(this.disciplinas);
      // console.log(this.nomesemana);
      // console.log(this.configuracoes);
    },
    deletarvideosemana: function (item) {
      var filtered = this.videos.filter(function (el) {
        return el.frame != item;
      });
      this.videos = filtered;
      // console.log(this.videos);
    },
    async inserirdisciplinas() {
      this.camposDisciplina._id = this.camposDisciplina.codigo_conteudo;

      if (
        this.validarcampos(this.camposDisciplina) == true &&
        this.tabeladisciplina != ""
      ) {
        let result = await eel.inserir_documento(
          this.bancoselecionado,
          this.camposDisciplina,
          this.tabeladisciplina.toUpperCase()
        )();
        if (result == true) {
          this.formularioinsercao = false;
          await this.listardisciplinas(this.tabeladisciplina.toUpperCase());
          this.alertar(
            true,
            "Disciplina inserida com sucesso",
            "mdi-check-bold",
            "success"
          );
          await this.listartabelas();
        } else {
          this.alertar(
            true,
            "Já existe uma disciplina cadastrada!",
            "mdi-alert",
            "warning"
          );
        }
      } else {
        this.alertar(
          true,
          "Nenhum campo devera ficar em branco",
          "mdi-alert",
          "error"
        );
      }
    },
    async listardisciplinas(tabela = "disci") {
      let disciplinas = await eel.listar_documentos(
        this.bancoselecionado,
        tabela
      )();
      this.listadisciplinas = disciplinas;
      this.dialoglistadisciplinas = true;
    },
    async deletar(codigoconteudo, frame) {
      let documento = { _id: `${codigoconteudo}_` + frame };
      let d = await eel.remover_documentos(
        this.bancoselecionado,
        this.titulosemana,
        documento
      )();

      if (d > 0) {
        this.alertar(
          true,
          "Frame removido com sucesso",
          "mdi-code-tags",
          "success"
        );
        let v = await eel.listar_documentos(
          this.bancoselecionado,
          this.titulosemana
        )();
        if (v.length > 0) {
          this.videos = v;
        } else {
          this.videos = [];
        }
      } else {
        this.alertar(true, "Frame nao encontrado", "mdi-code-tags", "error");
      }
    },
    alertar: function (on, message, type, color) {
      this.alert.on = on;
      this.alert.message = message;
      this.alert.type = type;
      this.alert.color = color;
    },
    limparlistadisciplinas: function () {
      this.dialoglistadisciplinas = false;
    },
    async fecharRelatorio(salvar = true) {
      this.botaofecharrelatorio = false;
      if (salvar == true) {
        await eel.inserir_documento(
          this.bancoselecionado,
          this.dadosrelatorio,
          "Relatorios",
          true
        )();
      }
      // this.dialogRelatorio = false;
      // this.menu = true;
      // this.colorbar = "#762051";
      // this.progresso = false;
      // this.timeline = false;
      // this.power = 0;
      document.location.reload();
    },
    contvideos: function (arr, codigo) {
      let qtd = 0;
      arr.forEach((element) => {
        if (element.codigo_conteudo == codigo) {
          qtd++;
        }
      });
      return qtd;
    },
    async montarvideos(codigo) {
      this.video._id = `${codigo}_` + this.video.frame;

      if (this.video.frame != "" && this.titulosemana != "") {
        this.videoparacadastrar._id = this.video._id;
        this.videoparacadastrar.codigo_conteudo = codigo;
        this.videoparacadastrar.titulo = this.video.titulo;
        this.videoparacadastrar.frame = this.video.frame;
        this.videoparacadastrar.info = "DISPONIVEL PARA INSERCAO";

        let result = await eel.inserir_documento(
          this.bancoselecionado,
          this.videoparacadastrar,
          this.titulosemana.toUpperCase()
        )();
        if (result == true) {
          this.alertar(
            true,
            "Frame cadastrado com sucesso!",
            "mdi-check-bold",
            "success"
          );
          let v = await eel.listar_documentos(
            this.bancoselecionado,
            this.titulosemana
          )();
          if (v.length > 0) {
            this.videos = v;
          }
          let semana = await eel.listar_tabelas(
            this.bancoselecionado,
            "semana"
          )();
          this.semanas = semana.reverse();
        } else {
          this.alertar(true, "Frame já cadastrado", "mdi-alert", "error");
        }
        // console.log(this.videos);
        this.video.frame = "";
        this.video.titulo = "";
      } else {
        this.alertar(
          true,
          "Campos frame ou semana em branco",
          "mdi-code-tags",
          "error"
        );
      }
    },
    async montarsemanaparainsercao(semana) {
      this.nomesemana = semana;
      if (this.disciplinasselecionadas != "" && this.nomesemana != "") {
        let disciplinas = await eel.carregar_disciplinas_para_insercao(
          this.bancoselecionado,
          this.disciplinasselecionadas,
          this.nomesemana
        )();
        this.disciplinas = disciplinas;
        // console.log(this.disciplinas);
      } else {
        this.alertar(
          true,
          "Escolha o grupo de disciplinas e clique na semana desejada",
          "mdi-alert",
          "info"
        );
      }
    },
    async selecionartabela() {
      await this.carregarsemana(this.nometabela)();
    },
  },
  watch: {
    logVideos: function () {
      scrolltobottom();
    },
    logDisciplinas: function () {
      scrolltobottom();
      let pctgatual = this.logDisciplinas.length;
      let totalD = this.progressocountdisciplinas;
      this.power = (pctgatual / totalD) * 100;
    },
    dadosrelatorio: function () {
      scrolltobottom();
      this.dialogRelatorio = true;
    },
    async titulosemana() {
      this.videos = [];
      if (this.titulosemana != "") {
        let titulosem = this.titulosemana.toUpperCase();
        // console.log(titulosem);
        let v = await eel.listar_documentos(this.bancoselecionado, titulosem)();
        if (v.length > 0) {
          this.videos = v;
          this.vervideos = true;
          this.alertar(
            true,
            `Foram encontrados ${v.length} frames cadastrados em ${titulosem}`,
            "mdi-code-tags",
            "info"
          );
        }
      }
    },
  },
});
