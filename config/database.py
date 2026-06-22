import psycopg2

class DatabaseConnection:
    _instance = None  # Guarda a única instância da conexão

    def __new__(cls):
        # Se a instância ainda não existir, cria uma nova
        if cls._instance is None:
            try:
                usuario = "postgres"
                senha = "postgres"  
                banco = "lpoo_projeto_pedro_henrique_carniel"  
                
                conn_uri = f"postgresql://{usuario}:{senha}@localhost:5432/{banco}"
                cls._instance = psycopg2.connect(conn_uri, client_encoding="latin1")
                print("Conexão com o PostgreSQL criada com sucesso via Singleton!")
            except Exception as e:
                print(f"Erro ao conectar ao banco de dados: {str(e).encode('utf-8', 'ignore').decode('utf-8')}")
                cls._instance = None
        
        # Se já existir, apenas devolve a mesma que foi criada antes
        return cls._instance