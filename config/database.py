import psycopg2

class Database:
    @staticmethod
    def get_connection():
        try:
            return psycopg2.connect(
                host="localhost",
                database="lpoo_projeto_pedro_henrique_carniel",
                user="postgres",       
                password="postgres",
                client_encoding="latin1",      
                options="-c search_path=public" 
            )
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None