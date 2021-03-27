import pymongo


class ConteudoMDB:

    def __init__(self, banco):

        self.client = pymongo.MongoClient(
            f"mongodb://novousuario:ggwaE2eZPpPAGAEx@cluster0-shard-00-00.2if2x.mongodb.net:27017,cluster0-shard-00-01.2if2x.mongodb.net:27017,cluster0-shard-00-02.2if2x.mongodb.net:27017/{banco}?ssl=true&replicaSet=atlas-sara4b-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.banco = self.client[f"{banco}"]
        self.table = None
    # Retorna um array
    def list_tables(self):
        tabelas = []
        lista = self.banco.list_collections()
        for l in lista:
            nome = l["name"].replace("_", " ")
            tabelas.append(nome)
        return tabelas

    def tabela(self, tabela):
        tabela = tabela.replace(" ", "_")
        table = self.banco[f"{tabela}"]
        self.table = table

    def insert(self, document, muitos=False):
        try:
            if muitos == False:
                q = self.table.insert_one(document)
            else:
                q = self.table.insert_many(document)

            print("Registrado com sucesso")
            return True
        except pymongo.errors.DuplicateKeyError:
            print("Já existe um registro")
            return False
        except pymongo.errors.BulkWriteError:
            print("Já existe um registro")
            return False

    def find_all(self):
        query = self.table
        count = query.estimated_document_count()
        if count > 0:
            result = query.find()
            return result
        else:
            # print("Sem registros")
            return 0

    def find_one(self, codigo):
        query = self.table
        count = query.find_one({"codigo_disciplina": codigo})
        return count


# disciplina = {
#     "_id": 768,
#     "codigo_disciplina": 447,
#     "nome_disciplina": "Direito Processual Civil III",
#     "professor": "Thiago",
#     "codigo_conteudo": 768
# }

videos = [{
    "codigo_conteudo": 6,
    "titulo": "teste",
    "frame": 123456789,
    "info": "DISNPONIVEL PARA INSERCAO"
},
    {
    "codigo_conteudo": 6,
    "titulo": "teste II",
    "frame": 654655658,
    "info": "DISNPONIVEL PARA INSERCAO"

}
]


# conteudo_mdb = ConteudoMDB("AutoSEI")
# conteudo_mdb.tabela("SEMANA 01")
# conteudo_mdb.insert(videos, True)
# # conteudo_mdb.find_all()
# lista = conteudo_mdb.list_tables()
# print(lista)
# print(conteudo_mdb.find_one(1))
