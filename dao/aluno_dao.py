from config.database import DatabaseConnection
from model.aluno import Aluno

class AlunoDAO:
    def __init__(self):
        # Pega a conexão única compartilhada pelo Singleton
        self.conn = DatabaseConnection()

    def cadastrar(self, aluno: Aluno):
        if not self.conn: return None
        cursor = self.conn.cursor()
        query = "INSERT INTO aluno (nome, cpf, telefone, id_instrutor) VALUES (%s, %s, %s, %s) RETURNING id"
        cursor.execute(query, (aluno.nome, aluno.cpf, aluno.telefone, aluno.id_instrutor))
        aluno.id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return aluno.id

    def listar_todos(self, busca=""):
        if not self.conn: return []
        cursor = self.conn.cursor()
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
        return alunos

    def atualizar(self, aluno: Aluno):
        if not self.conn: return
        cursor = self.conn.cursor()
        query = "UPDATE aluno SET nome=%s, cpf=%s, telefone=%s, id_instrutor=%s WHERE id=%s"
        cursor.execute(query, (aluno.nome, aluno.cpf, aluno.telefone, aluno.id_instrutor, aluno.id))
        self.conn.commit()
        cursor.close()

    def deletar(self, id_aluno):
        if not self.conn: return
        cursor = self.conn.cursor()
        query = "DELETE FROM aluno WHERE id = %s"
        cursor.execute(query, (id_aluno,))
        self.conn.commit()
        cursor.close()

    def listar_instrutores(self):
        if not self.conn: return []
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome FROM instrutor ORDER BY nome")
        rows = cursor.fetchall()
        cursor.close()
        return rows