import pymongo


class ConteudoMDB:

    def __init__(self, banco="Default"):

        self.client = pymongo.MongoClient(
            f"mongodb://novousuario:ggwaE2eZPpPAGAEx@cluster0-shard-00-00.2if2x.mongodb.net:27017,cluster0-shard-00-01.2if2x.mongodb.net:27017,cluster0-shard-00-02.2if2x.mongodb.net:27017/{banco}?ssl=true&replicaSet=atlas-sara4b-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.banco = self.client[f"{banco}"]
        self.table = None
    # Retorna um array

    def list_tables(self, nome=""):
        filter = {"name": {"$regex": f".*{nome}", "$options": 'i'}}
        lista = self.banco.list_collection_names(filter=filter)
        return [l.replace("_", " ") for l in lista]

    def list_dbs(self):
        lista = self.client.list_database_names()
        lista = [l for l in lista if not("admin" in l) and not("local" in l)]
        return lista

    def tabela(self, tabela):
        tabela = tabela.replace(" ", "_")
        table = self.banco[f"{tabela}"]
        self.table = table

    # def deletar_tabela_criada(self):
    #     self.table.drop()

    def insert(self, document, muitos=False):
        try:
            if muitos == False:
                q = self.table.insert_one(document)
            else:
                q = self.table.insert_many(document)

            # print("Registrado com sucesso")
            return True
        except pymongo.errors.DuplicateKeyError:
            # print("Já existe um registro")
            return False
        except pymongo.errors.BulkWriteError:
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

    def find_in_week(self, semana, query):
        tabela = self.banco[f"{semana}"]
        count = tabela.estimated_document_count()
        if count > 0:
            result = tabela.find(query)
            return result
        else:
            # print("Sem registros")
            return 0

    def remove(self, document):
        q = self.table.delete_one(document)
        result = q.deleted_count
        return result

    def montar_videos_da_semana(self, semana):
        semana = semana.replace(" ", "_")
        disciplinas = []
        resultD = self.find_all()
        if resultD != 0:
            for r in resultD:
                disciplina = {"codigo_disciplina": r["codigo_disciplina"],
                              "nome_disciplina": r["nome_disciplina"],
                              "professor": r["professor"],
                              "codigo_conteudo": r["codigo_conteudo"],
                              "videos": []}

                resultV = self.find_in_week(
                    semana, {"codigo_conteudo": r["codigo_conteudo"]})
                if resultV != 0:
                    for v in resultV:
                        frames = {
                            "titulo": v["titulo"],
                            "frame": v["frame"]
                        }
                        disciplina["videos"].append(frames)

                disciplinas.append(disciplina)

        return disciplinas


disciplinas = [
    {
        "_id": 6,
        "codigo_disciplina": 94,
        "nome_disciplina": "Ciência Política",
        "professor": "Joao",
        "codigo_conteudo": 6
    },
    {
        "_id": 7,
        "codigo_disciplina": 94,
        "nome_disciplina": "Ciência Política II",
        "professor": "Paula",
        "codigo_conteudo": 7
    },
    {
        "_id": 8,
        "codigo_disciplina": 1286,
        "nome_disciplina": "Filosofia Geral e Jurídica",
        "professor": "Mauricio",
        "codigo_conteudo": 8
    }
]

# nome = "Rutemberg"
# conteudo_mdb = ConteudoMDB()
# conteudo_mdb.tabela("bancocriado")
# conteudo_mdb.insert({"nome": nome})
# print(conteudo_mdb.list_dbs())
# conteudo_mdb.deletar_tabela_criada()
# conteudo_mdb.tabela("DISCIPLINAS TESTE")
# print(conteudo_mdb.montar_videos_da_semana("SEMANA TESTE"))
# conteudo_mdb.insert(disciplinas, True)
# frame = {"frame": "123"}
# print(conteudo_mdb.remove(frame))
# conteudo_mdb.insert(videos, True)
# conteudo_mdb.find_all()
# lista = conteudo_mdb.list_tables("disci")
# print(lista)
# print(conteudo_mdb.find_one(1))
