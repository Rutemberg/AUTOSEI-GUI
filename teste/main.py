import pymongo


class ConteudoMDB:

    def __init__(self, banco):

        self.client = pymongo.MongoClient(
            "mongodb+srv://novousuario:ggwaE2eZPpPAGAEx@cluster0.2if2x.mongodb.net")
        self.banco = self.client[f"{banco}"]
        self.table = None

    def tabela(self, tabela):
        table = self.banco[f"{tabela}"]
        self.table = table

    def insert(self, document):
        try:
            q = self.table.insert_one(document)
            print("Registrado com sucesso")
            return True
        except pymongo.errors.DuplicateKeyError:
            print(f"Já existe um registro")
            return False

    def find_all(self):
        query = self.table
        count = query.estimated_document_count()
        if count > 0:
            result = query.find()
            return result
        else:
            print("Sem registros")
            return 0


# disciplina = {
#     "_id": 768,
#     "codigo_disciplina": 447,
#     "nome_disciplina": "Direito Processual Civil III",
#     "professor": "Thiago",
#     "codigo_conteudo": 768
# }

# conteudo_mdb = ConteudoMDB("AutoSEI")
# conteudo_mdb.tabela("Disciplinas")
# # conteudo_mdb.insert(disciplina)
# conteudo_mdb.find_all()
