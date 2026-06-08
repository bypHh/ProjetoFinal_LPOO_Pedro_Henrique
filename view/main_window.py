import tkinter as tk
from tkinter import messagebox
from view.aluno_view import AlunoView
from view.treino_view import TreinoView
from view.instrutor_view import InstrutorView

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FitManager Pro - Gestão Integrada")
        self.geometry("580x620") 
        self.resizable(True, True)
        self.configure(bg="#f4f6f9")
        
        self.configurar_menu()
        
        self.container = tk.Frame(self, bg="#f4f6f9")
        self.container.pack(fill="both", expand=True)
        
        self.mostrar_tela_alunos()

    def configurar_menu(self):
        menu_bar = tk.Menu(self)
        
        menu_sistema = tk.Menu(menu_bar, tearoff=0)
        menu_sistema.add_command(label="Alunos (Matrículas)", command=self.mostrar_tela_alunos)
        menu_sistema.add_command(label="Instrutores (Profissionais)", command=self.mostrar_tela_instrutores)
        menu_sistema.add_command(label="Treinos (Prescrições)", command=self.mostrar_tela_treinos)
        menu_sistema.add_separator()
        menu_sistema.add_command(label="Sair", command=self.quit)
        menu_bar.add_cascade(label="Navegação", menu=menu_sistema)
        
        menu_ajuda = tk.Menu(menu_bar, tearoff=0)
        menu_ajuda.add_command(label="Sobre o Autor", command=self.mostrar_sobre)
        menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
        
        self.config(menu=menu_bar)

    def mostrar_tela_alunos(self):
        self.limpar_container()
        frame = AlunoView(self.container)
        frame.pack(fill="both", expand=True)

    def mostrar_tela_instrutores(self):
        self.limpar_container()
        frame = InstrutorView(self.container)
        frame.pack(fill="both", expand=True)

    def mostrar_tela_treinos(self):
        self.limpar_container()
        frame = TreinoView(self.container)
        frame.pack(fill="both", expand=True)

    def mostrar_sobre(self):
        messagebox.showinfo(
            "Sobre o Sistema", 
            "FitManager Pro v2.5\n\n"
            "Solução acadêmica orientada a objetos para o controle de rotinas fitness.\n"
            "Padrões: DAO & Factory Method.\n"
            "Autor: Pedro Henrique\nAno: 2026"
        )

    def limpar_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()