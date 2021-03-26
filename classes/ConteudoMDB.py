import pymongo

class ConteudoMDB:

    def __init__(self, banco):

        self.client = pymongo.MongoClient(
            "mongodb+srv://novousuario:ggwaE2eZPpPAGAEx@cluster0.2if2x.mongodb.net")
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

    def insert(self, document):
        try:
            q = self.table.insert_one(document)
            # print("Registrado com sucesso")
            return True
        except pymongo.errors.DuplicateKeyError:
            # print("Já existe um registro")
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

# videos = {  
#             "_id": 447,
#             "codigo_disciplina": 447,
#             "nome_disciplina": "Direito Processual Civil III",
#             "professor": "Thiago",
#             "videos":
#                     [
#                         {
#                         "titulo": "teste",
#                         "frame": 123456789
#                         },
#                         {
#                         "titulo": "teste",
#                         "frame": 123456789
#                         }
#                     ]
# }



# conteudo_mdb = ConteudoMDB("AutoSEI")
# conteudo_mdb.tabela("SEMANA 01")
# conteudo_mdb.insert(videos)
# # conteudo_mdb.find_all()
# lista = conteudo_mdb.list_tables()
# print(lista)
# print(conteudo_mdb.find_one(1))
