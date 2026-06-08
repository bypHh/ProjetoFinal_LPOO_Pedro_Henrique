class Treino:
    def __init__(self, id_treino=None, id_aluno=None, tipo_treino=None, descricao=None, frequencia=None):
        self.id = id_treino
        self.id_aluno = id_aluno
        self.tipo_treino = tipo_treino
        self.descricao = descricao
        self.frequencia = frequencia

# PADRÃO DE PROJETO: Factory Method (Fábrica de Treinos)
class TreinoFactory:
    @staticmethod
    def criar_treino(tipo, id_aluno, frequencia):
        if tipo.upper() == "HIPERTROFIA":
            desc = "Foco em hipertrofia muscular. 4 series de 8 a 12 repeticoes com cargas altas (RPE 8-9)."
            return Treino(id_aluno=id_aluno, tipo_treino="Hipertrofia", descricao=desc, frequencia=frequencia)
        elif tipo.upper() == "CARDIO":
            desc = "Foco em capacidade cardiorrespiratoria. 40 minutos de corrida moderada + 15 minutos de HIIT."
            return Treino(id_aluno=id_aluno, tipo_treino="Cardio", descricao=desc, frequencia=frequencia)
        else:
            desc = "Treino adaptativo geral. Circuitos full-body de resistencia leve, 3 series de 15 repeticoes."
            return Treino(id_aluno=id_aluno, tipo_treino="Geral", descricao=desc, frequencia=frequencia)