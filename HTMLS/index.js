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
    vervideos: false,
    semana: false,
    disciplinassemana: [],
    disciplinassemanaparacadastrar: [],
    listadisciplinas: [],
    mensagemDisciplina,
    formularioinsercao: false,
    dialoglistadisciplinas: false,
    camposDisciplina: {
      _id: "",
      nome_disciplina: "Ciência Política",
      codigo_disciplina: 94,
      codigo_conteudo: 6,
      professor: "Joao",
    },
    dialog: false,
    dialogRelatorio: false,
    fab: false,
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
    try {
      let configuracoes = await eel.carregar_configuracoes()();
      this.configuracoes = configuracoes;
    } catch (e) {
      console.error(e);
    }
    var main = document.getElementById("app");
    main.style.display = "block";
    this.titulo = true;
    this.appbar = true;
  },
  methods: {
    async carregardisciplinas() {
      try {
        let disciplinas = await eel.carregar_disciplinas()();
        this.disciplinas = disciplinas;
      } catch (e) {
        console.error(e);
      }
      this.dialog = true;
    },
    async carregarsemana() {
      try {
        disciplinas = await eel.listar_documentos("Disciplinas")();
        this.disciplinassemana = disciplinas;
        this.semana = true;
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
        if (a.videos[0].frame != "" && faltam == false) {
          qnt += a.videos.length;
        } else if (a.videos[0].frame == "" && faltam == true) {
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
    async inserirvideossemana() {
      let videos = this.videos;
      let titulosemana = this.titulosemana;
      if (videos.length > 0 && titulosemana != "") {
        let result = await eel.inserir_documento(videos, titulosemana, true)();
        if (result == true) {
          this.alertar(
            true,
            "Semana cadastrada com sucesso!",
            "mdi-check-bold",
            "success"
          );
        } else {
          this.alertar(
            true,
            "Já existe um ou mais frames inseridos no banco",
            "mdi-alert",
            "error"
          );
        }
      } else {
        this.alertar(
          true,
          "Insira o nome da semana e algum video para poder inserir",
          "mdi-alert",
          "error"
        );
      }
    },
    async inserirdisciplinas() {
      this.camposDisciplina._id = this.camposDisciplina.codigo_conteudo;

      if (this.validarcampos(this.camposDisciplina) == true) {
        let result = await eel.inserir_documento(
          this.camposDisciplina,
          "Disciplinas"
        )();
        if (result == true) {
          this.formularioinsercao = false;
          await this.listardisciplinas();
          this.alertar(
            true,
            "Disciplina inserida com sucesso",
            "mdi-check-bold",
            "success"
          );
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
    async listardisciplinas() {
      let disciplinas = await eel.listar_documentos("Disciplinas")();
      this.listadisciplinas = disciplinas.reverse();
      this.dialoglistadisciplinas = true;
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
    montarvideos: function (codigo) {
      this.video._id = this.video.frame;

      if (this.video.frame != "") {
        this.videos.push({
          _id: this.video._id,
          codigo_conteudo: codigo,
          titulo: this.video.titulo,
          frame: this.video.frame,
          info: "DISPONIVEL PARA INSERCAO",
        });
        this.alertar(
          true,
          "Frame adicionado com sucesso",
          "mdi-code-tags-check",
          "success"
        );
        // console.log(this.videos);
        this.video.frame = "";
        this.video.titulo = "";
      } else {
        this.alertar(true, "Campo frame em branco", "mdi-code-tags", "error");
      }
    },
  },
  watch: {
    logVideos: function () {
      scrolltobottom();
    },
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
  },
});
