from config.database import Database
from model.aluno import Aluno

class AlunoDAO:
    def cadastrar(self, aluno: Aluno):
        conn = Database.get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO aluno (nome, cpf, telefone, id_instrutor) VALUES (%s, %s, %s, %s) RETURNING id"
        cursor.execute(query, (aluno.nome, aluno.cpf, aluno.telefone, aluno.id_instrutor))
        aluno.id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return aluno.id

    def listar_todos(self, busca=""):
        conn = Database.get_connection()
        cursor = conn.cursor()
        query = """SELECT a.id, a.nome, a.cpf, a.telefone, a.id_instrutor, i.nome 
                   FROM aluno a 
                   LEFT JOIN instrutor i ON a.id_instrutor = i.id"""
        if busca:
            query += " WHERE a.nome ILIKE %s ORDER BY a.id"
            cursor.execute(query, (f"%{busca}%",))
        else:
            query += " ORDER BY a.id"
            cursor.execute(query)
            
        rows = cursor.fetchall()
        alunos = [Aluno(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
        cursor.close()
        conn.close()
        return alunos

    def atualizar(self, aluno: Aluno):
        conn = Database.get_connection()
        cursor = conn.cursor()
        query = "UPDATE aluno SET nome=%s, cpf=%s, telefone=%s, id_instrutor=%s WHERE id=%s"
        cursor.execute(query, (aluno.nome, aluno.cpf, aluno.telefone, aluno.id_instrutor, aluno.id))
        conn.commit()
        cursor.close()
        conn.close()

    def deletar(self, id_aluno):
        conn = Database.get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM aluno WHERE id = %s"
        cursor.execute(query, (id_aluno,))
        conn.commit()
        cursor.close()
        conn.close()

    def listar_instrutores(self):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM instrutor ORDER BY nome")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows