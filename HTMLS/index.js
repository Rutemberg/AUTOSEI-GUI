eel.expose(timeline);
eel.expose(logvideos);
eel.expose(logsemana);
eel.expose(relatoriofinal);
eel.expose(loginserirdisciplina);

var infodisciplinas = [];
var titulovideos = [];
var semana = [];
var dadosr = [];
var mensagemDisciplina = [];

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
  console.log("Inserida: " + inserida + " Codigo : " + codigo);
  semana.push({ inserida, codigo });
}

function relatoriofinal(
  tempo,
  totaldisciplinas,
  totalvideos,
  totalDinseridas,
  faltam
) {
  // console.log(tempo, totaldisciplinas, totalvideos, totalDinseridas, faltam);
  dadosr.push({
    tempo,
    totaldisciplinas,
    totalvideos,
    totalDinseridas,
    faltam,
  });
  console.log(dadosr);
}

function scrolltobottom() {
  let element = document.getElementById("app");
  element.scrollIntoView({ behavior: "instant", block: "end" });
}

function loginserirdisciplina(resultado) {
  if (resultado == true) {
    msg = "Inserida com sucesso";
  } else {
    msg = "Disciplina já inserida";
  }
  mensagemDisciplina.push({ resultado, msg });
}

new Vue({
  el: "#app",
  vuetify: new Vuetify(),
  data: {
    bancos: [],
    bancoselecionado: "",
    nomebanco: "",
    nometabela: "",
    tabelas: [],
    semanas: [],
    nomesemana: "",
    nomedisciplina: "",
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
    semana: false,
    disciplinassemana: [],
    disciplinassemanaparacadastrar: [],
    listadisciplinas: [],
    mensagemDisciplina,
    formularioinsercao: false,
    formulariobanco: false,
    dialoglistadisciplinas: false,
    tabeladisciplina: "",
    camposDisciplina: {
      _id: "",
      nome_disciplina: "Ciência Política",
      codigo_disciplina: 94,
      codigo_conteudo: 6,
      professor: "Joao",
    },
    dialoginsercao: false,
    dialogbanco: false,
    dialog: false,
    dialogRelatorio: false,
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
    fechardialoginsercao() {
      this.dialoginsercao = false;
      this.disciplinas = [];
    },
    async carregarbanco(banco) {
      this.bancoselecionado = banco;
      let configuracoes = await eel.carregar_configuracoes()();
      let semanas = await eel.listar_tabelas(this.bancoselecionado, "semana")();
      await this.listartabelas();
      this.semanas = semanas.reverse();
      this.configuracoes = configuracoes;
      this.dialogbanco = false;
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
      for (var item in arr) {
        if (arr[item] == "") {
          return false;
        } else {
          return true;
        }
      }
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
    iniciar: function (value) {
      eel.insercao(value)();
      this.dialog = false;
      this.timeline = true;
      this.menu = false;
      this.colorbar = "transparent";
      this.progresso = true;
    },
    deletarvideosemana: function (item) {
      var filtered = this.videos.filter(function (el) {
        return el.frame != item;
      });
      this.videos = filtered;
      console.log(this.videos);
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
      this.listadisciplinas = disciplinas.reverse();
      this.dialoglistadisciplinas = true;
    },
    async deletar(document) {
      let d = await eel.remover_documentos(
        this.bancoselecionado,
        this.titulosemana,
        document
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
    fecharRelatorio: function () {
      this.dialogRelatorio = false;
      this.menu = true;
      this.colorbar = "#762051";
      this.progresso = false;
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
      this.video._id = this.video.frame;

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
      if (this.nomedisciplina != "") {
        this.nomesemana = semana;

        let disciplinas = await eel.carregar_disciplinas_para_insercao(
          this.bancoselecionado,
          this.nomedisciplina,
          this.nomesemana
        )();
        this.disciplinas = disciplinas;
        console.log(this.disciplinas);
      } else {
        this.alertar(
          true,
          "Escolha o grupo de disciplinas a serem inseridas",
          "mdi-alert",
          "warning"
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
    // nomesemana: function () {
    //   console.log(this.nomesemana);
    // },
    // nomedisciplina: function () {
    //   console.log(this.nomedisciplina);
    // },
    logDisciplinas: function () {
      scrolltobottom();
      let pctgatual = this.logDisciplinas.length;
      let totalD = this.disciplinas.length;
      this.power = (pctgatual / totalD) * 100;
    },
    dadosrelatorio: function () {
      scrolltobottom();
      this.dialogRelatorio = true;
    },
    async titulosemana() {
      this.videos = [];
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
    },
  },
});
