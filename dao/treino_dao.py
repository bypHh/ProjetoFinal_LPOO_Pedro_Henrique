from config.database import DatabaseConnection
from model.treino import Treino

class TreinoDAO:
    def __init__(self):
        # Pega a conexão única compartilhada pelo Singleton
        self.conn = DatabaseConnection()

    def salvar_treino(self, treino: Treino):
        if not self.conn: return
        cursor = self.conn.cursor()
        query = """INSERT INTO treino (id_aluno, tipo_treino, descricao, frequencia_semanal) 
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (treino.id_aluno, treino.tipo_treino, treino.descricao, treino.frequencia))
        self.conn.commit()
        cursor.close()

    def listar_por_aluno(self, id_aluno):
        if not self.conn: return []
        cursor = self.conn.cursor()
        query = "SELECT id, tipo_treino, descricao, frequencia_semanal FROM treino WHERE id_aluno = %s ORDER BY id"
        cursor.execute(query, (id_aluno,))
        rows = cursor.fetchall()
        treinos = [Treino(r[0], id_aluno, r[1], r[2], r[3]) for r in rows]
        cursor.close()
        return treinos

    def deletar_treino(self, id_treino):
        if not self.conn: return
        cursor = self.conn.cursor()
        query = "DELETE FROM treino WHERE id = %s"
        cursor.execute(query, (id_treino,))
        self.conn.commit()
        cursor.close()