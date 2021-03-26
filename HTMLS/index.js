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
    titulo: "",
    frame: "",
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
    async inserirdisciplinas() {
      this.camposDisciplina._id = this.camposDisciplina.codigo_conteudo;
      let result = await eel.inserir_documento(
        this.camposDisciplina,
        "Disciplinas"
      )();
      if (result == true) {
        this.formularioinsercao = false;
        await this.listardisciplinas();
      }
    },
    async listardisciplinas() {
      let disciplinas = await eel.listar_documentos("Disciplinas")();
      this.listadisciplinas = disciplinas.reverse();
      this.dialoglistadisciplinas = true;
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
        if (element.cd == codigo) {
          qtd++;
        }
      });
      return qtd;
    },
    montarvideos: function (codigo) {
      this.videos.push({ cd: codigo, titulo: this.titulo, frame: this.frame });
      console.log(this.videos);
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
