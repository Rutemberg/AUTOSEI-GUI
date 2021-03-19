eel.expose(timeline);
eel.expose(logvideos);
eel.expose(logsemana);
eel.expose(relatoriofinal);

var infodisciplinas = [];
var titulovideos = [];
var semana = [];
var dadosr = {};

function timeline(nome, disciplina, video, codigo) {
  //   console.log(nome, disciplina, video, codigo);
  infodisciplinas.push({
    nome: nome,
    disciplina: disciplina,
    video: video,
    codigo: codigo,
  });
}

function logvideos(titulo, codigo) {
  //   console.log(titulo, codigo);
  titulovideos.push({ titulo: titulo, codigo: codigo});
}

function logsemana(inserida, codigo) {
  console.log("Inserida: " + inserida + " Codigo : " + codigo);
  semana.push({ inserida: inserida, codigo:  codigo});
}

function relatoriofinal(tempo, totaldisciplinas, totalvideos, totalDinseridas, faltam) {
  console.log(tempo, totaldisciplinas, totalvideos, totalDinseridas, faltam);
  dadosr.push({ tempo: tempo, totaldisciplinas: totaldisciplinas, totalvideos: totalvideos, totalDinseridas: totalDinseridas, faltam: faltam});
}

function scrolltobottom() {
  let element = document.getElementById("app");
  element.scrollIntoView({ behavior: "instant", block: "end" });
}

new Vue({
  el: "#app",
  vuetify: new Vuetify(),
  data: {
    dialog: false,
    dialogRelatorio: false,
    fab: false,
    disciplinas: [],
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
    contar: function (array) {
      return array.length;
    },
    iniciar: function (value) {
      eel.insercao(value)();
      this.dialog = false;
    },
  },
  watch: {
    logVideos: function () {
      scrolltobottom();
    },
    logDisciplinas: function () {
      scrolltobottom();
    },
    dadosrelatorio: function () {
      this.dialogRelatorio = true;
    },
  },
});
