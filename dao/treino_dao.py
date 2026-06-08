from config.database import Database
from model.treino import Treino

class TreinoDAO:
    def salvar_treino(self, treino: Treino):
        conn = Database.get_connection()
        cursor = conn.cursor()
        query = """INSERT INTO treino (id_aluno, tipo_treino, descricao, frequencia_semanal) 
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (treino.id_aluno, treino.tipo_treino, treino.descricao, treino.frequencia))
        conn.commit()
        cursor.close()
        conn.close()

    def listar_por_aluno(self, id_aluno):
        conn = Database.get_connection()
        cursor = conn.cursor()
        query = "SELECT id, tipo_treino, descricao, frequencia_semanal FROM treino WHERE id_aluno = %s ORDER BY id"
        cursor.execute(query, (id_aluno,))
        rows = cursor.fetchall()
        treinos = [Treino(r[0], id_aluno, r[1], r[2], r[3]) for r in rows]
        cursor.close()
        conn.close()
        return treinos

    def deletar_treino(self, id_treino):
        conn = Database.get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM treino WHERE id = %s"
        cursor.execute(query, (id_treino,))
        conn.commit()
        cursor.close()
        conn.close()