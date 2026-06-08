import tkinter as tk
from tkinter import messagebox, ttk

from dao.aluno_dao import AlunoDAO
from dao.treino_dao import TreinoDAO
from model.treino import TreinoFactory

class TreinoView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.aluno_dao = AlunoDAO()
        self.treino_dao = TreinoDAO()
        self.aluno_map = {}
        
        self.bg_color = "#f4f6f9"
        self.primary_color = "#1e3d59"
        self.accent_color = "#17b978"
        self.danger_color = "#ff5e62"
        
        self.configure(bg=self.bg_color)
        self.criar_componentes()
        self.carregar_combobox_alunos()

    def criar_componentes(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 9), rowheight=28, background="white")
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"), background=self.primary_color, foreground="white")

        main_container = tk.Frame(self, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=20, pady=15)

        lbl_titulo = tk.Label(main_container, text="MONTAGEM DE FICHAS DE TREINO", font=("Arial", 13, "bold"), fg=self.primary_color, bg=self.bg_color)
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        form_frame = tk.Frame(main_container, bg=self.bg_color)
        form_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        form_frame.columnconfigure(1, weight=1)

        tk.Label(form_frame, text="Selecione o Aluno:", font=("Arial", 10, "bold"), bg=self.bg_color).grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))
        self.cb_aluno = ttk.Combobox(form_frame, font=("Arial", 10), state="readonly")
        self.cb_aluno.grid(row=0, column=1, sticky="ew", pady=8)
        self.cb_aluno.bind("<<ComboboxSelected>>", self.carregar_treinos_aluno)

        tk.Label(form_frame, text="Estilo (Factory):", font=("Arial", 10, "bold"), bg=self.bg_color).grid(row=1, column=0, sticky="w", pady=8, padx=(0, 10))
        self.cb_tipo = ttk.Combobox(form_frame, values=["Hipertrofia", "Cardio", "Geral"], font=("Arial", 10), state="readonly")
        self.cb_tipo.grid(row=1, column=1, sticky="ew", pady=8)
        self.cb_tipo.current(0)

        tk.Label(form_frame, text="Frequencia (Dias):", font=("Arial", 10, "bold"), bg=self.bg_color).grid(row=2, column=0, sticky="w", pady=8, padx=(0, 10))
        self.txt_freq = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid")
        self.txt_freq.grid(row=2, column=1, sticky="ew", pady=8)

        btn_frame = tk.Frame(main_container, bg=self.bg_color)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        btn_style = {"font": ("Arial", 10, "bold"), "fg": "white", "bd": 0, "cursor": "hand2", "padx": 15, "pady": 7}

        tk.Button(btn_frame, text="Gerar via Fabrica e Salvar", bg=self.accent_color, command=self.salvar_treino, **btn_style).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Excluir Rotina", bg=self.danger_color, command=self.excluir_treino, **btn_style).pack(side="left", padx=10)

        separator = ttk.Separator(main_container, orient="horizontal")
        separator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        tabela_frame = tk.Frame(main_container)
        tabela_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        main_container.rowconfigure(4, weight=1)

        self.tree = ttk.Treeview(tabela_frame, columns=("ID", "Tipo", "Prescricao Gerada", "Vezes"), show="headings", height=5)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Prescricao Gerada", text="Prescricao Gerada")
        self.tree.heading("Vezes", text="Freq")
        
        self.tree.column("ID", width=35, anchor="center")
        self.tree.column("Tipo", width=90, anchor="center")
        self.tree.column("Prescricao Gerada", width=300, anchor="w")
        self.tree.column("Vezes", width=50, anchor="center")
        
        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def carregar_combobox_alunos(self):
        self.aluno_map.clear()
        try:
            alunos = self.aluno_dao.listar_todos()
            nomes = [f"{a.nome} (CPF: {a.cpf})" for a in alunos]
            for a in alunos: self.aluno_map[f"{a.nome} (CPF: {a.cpf})"] = a.id
            self.cb_aluno['values'] = nomes
        except Exception as e:
            messagebox.showerror("Erro", f"Erro alunos: {e}")

    def carregar_treinos_aluno(self, event=None):
        for item in self.tree.get_children(): self.tree.delete(item)
        selecionado = self.cb_aluno.get()
        if not selecionado: return
        try:
            for t in self.treino_dao.listar_por_aluno(self.aluno_map[selecionado]):
                self.tree.insert("", "end", values=(t.id, t.tipo_treino, t.descricao, f"{t.frequencia}x"))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    def salvar_treino(self):
        selecionado, freq = self.cb_aluno.get(), self.txt_freq.get().strip()
        if not selecionado or not freq:
            messagebox.showwarning("Aviso", "Selecione o aluno e informe os dias!")
            return

        try:
            id_aluno = self.aluno_map[selecionado]
            tipo = self.cb_tipo.get()
            
            # Executa o Factory Method para gerar a descrição
            novo_treino = TreinoFactory.criar_treino(tipo, id_aluno, freq)
            self.treino_dao.salvar_treino(novo_treino)
            
            messagebox.showinfo("Sucesso", "Treino montado pela Fabrica e salvo!")
            self.txt_freq.delete(0, tk.END)
            self.carregar_treinos_aluno()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    def excluir_treino(self):
        item = self.tree.selection()
        if not item: return
        id_treino = self.tree.item(item, "values")[0]
        if messagebox.askyesno("Confirmar", "Remover este treino?"):
            self.treino_dao.deletar_treino(id_treino)
            self.carregar_treinos_aluno()