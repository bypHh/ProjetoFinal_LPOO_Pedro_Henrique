import tkinter as tk
from tkinter import messagebox, ttk
from dao.aluno_dao import AlunoDAO
from model.aluno import Aluno

class AlunoView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.dao = AlunoDAO()
        self.aluno_selecionado_id = None
        self.instrutor_map = {}
        
        self.bg_color = "#f4f6f9"
        self.primary_color = "#1e3d59"
        self.accent_color = "#17b978"
        self.danger_color = "#ff5e62"
        
        self.configure(bg=self.bg_color)
        self.criar_componentes()
        self.carregar_instrutores()
        self.atualizar_tabela()

    def criar_componentes(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 10), rowheight=25, background="white")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background=self.primary_color, foreground="white")

        main_container = tk.Frame(self, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=20, pady=15)

        lbl_titulo = tk.Label(main_container, text="GERENCIAMENTO DE ALUNOS", font=("Arial", 14, "bold"), fg=self.primary_color, bg=self.bg_color)
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        form_frame = tk.Frame(main_container, bg=self.bg_color)
        form_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        form_frame.columnconfigure(1, weight=1)

        labels = ["Nome:", "CPF (Apenas numeros):", "Telefone (Com DDD):", "Instrutor Resp.:"]
        for i, text in enumerate(labels):
            lbl = tk.Label(form_frame, text=text, font=("Arial", 10, "bold"), fg="#333333", bg=self.bg_color)
            lbl.grid(row=i, column=0, sticky="w", pady=6, padx=(0, 10))

        self.txt_nome = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid")
        self.txt_nome.grid(row=0, column=1, sticky="ew", pady=6)

        self.txt_cpf = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid")
        self.txt_cpf.grid(row=1, column=1, sticky="ew", pady=6)

        self.txt_telefone = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid")
        self.txt_telefone.grid(row=2, column=1, sticky="ew", pady=6)

        self.cb_instrutor = ttk.Combobox(form_frame, font=("Arial", 10), state="readonly")
        self.cb_instrutor.grid(row=3, column=1, sticky="ew", pady=6)

        btn_frame = tk.Frame(main_container, bg=self.bg_color)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        btn_style = {"font": ("Arial", 10, "bold"), "fg": "white", "bd": 0, "cursor": "hand2", "padx": 12, "pady": 6}

        tk.Button(btn_frame, text="Salvar Novo", bg=self.accent_color, command=self.salvar, **btn_style).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Atualizar", bg="#3a6073", command=self.atualizar, **btn_style).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Excluir", bg=self.danger_color, command=self.excluir, **btn_style).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Limpar", bg="#7f8c8d", command=self.limpar_campos, **btn_style).pack(side="left", padx=5)

        separator = ttk.Separator(main_container, orient="horizontal")
        separator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        busca_frame = tk.Frame(main_container, bg=self.bg_color)
        busca_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        busca_frame.columnconfigure(1, weight=1)

        tk.Label(busca_frame, text="Buscar por Nome:", font=("Arial", 10, "bold"), fg="#555555", bg=self.bg_color).pack(side="left", padx=(0, 5))
        self.txt_busca = tk.Entry(busca_frame, font=("Arial", 10), bd=1, relief="solid")
        self.txt_busca.pack(side="left", fill="x", expand=True, padx=5)
        
        tk.Button(busca_frame, text="Filtrar", bg=self.primary_color, fg="white", font=("Arial", 9, "bold"), bd=0, command=self.atualizar_tabela, padx=10, pady=3).pack(side="left")

        tabela_frame = tk.Frame(main_container)
        tabela_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")
        main_container.rowconfigure(5, weight=1)

        self.tree = ttk.Treeview(tabela_frame, columns=("ID", "Nome", "CPF", "Instrutor"), show="headings", height=6)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Instrutor", text="Instrutor")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Nome", width=150, anchor="w")
        self.tree.column("CPF", width=110, anchor="center")
        self.tree.column("Instrutor", width=120, anchor="w")
        
        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.carregar_aluno_selecionado)

    # VALIDAÇÃO OBRIGATÓRIA EXIGIDA NO ENUNCIADO (Algoritmo de CPF)
    def validar_cpf(self, cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11 or cpf == cpf[0] * 11: return False
        for j in [9, 10]:
            soma = sum(int(cpf[i]) * (j + 1 - i) for i in range(j))
            resto = (soma * 10) % 11
            if resto == 10: resto = 0
            if resto != int(cpf[j]): return False
        return True

    def validar_telefone(self, telefone):
        telefone = ''.join(filter(str.isdigit, telefone))
        return len(telefone) in [10, 11]

    def carregar_instrutores(self):
        try:
            self.instrutor_map.clear()
            instrutores = self.dao.listar_instrutores()
            nomes = []
            for id_inst, nome_inst in instrutores:
                nomes.append(nome_inst)
                self.instrutor_map[nome_inst] = id_inst
            self.cb_instrutor['values'] = nomes
            if nomes: self.cb_instrutor.current(0)
        except Exception as e:
            print(f"Erro ao carregar instrutores: {e}")

    def salvar(self):
        nome, cpf, telefone = self.txt_nome.get().strip(), self.txt_cpf.get().strip(), self.txt_telefone.get().strip()
        if not nome or not cpf or not self.cb_instrutor.get():
            messagebox.showwarning("Validacao", "Campos obrigatorios em branco!")
            return
        if not self.validar_cpf(cpf):
            messagebox.showerror("Erro", "CPF invalido!")
            return
        if telefone and not self.validar_telefone(telefone):
            messagebox.showerror("Erro", "Telefone invalido!")
            return
        
        try:
            id_inst = self.instrutor_map[self.cb_instrutor.get()]
            novo = Aluno(nome=nome, cpf=''.join(filter(str.isdigit, cpf)), telefone=''.join(filter(str.isdigit, telefone)), id_instrutor=id_inst)
            self.dao.cadastrar(novo)
            messagebox.showinfo("Sucesso", "Aluno matriculado!")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def atualizar(self):
        if not self.aluno_selecionado_id: return
        nome, cpf, telefone = self.txt_nome.get().strip(), self.txt_cpf.get().strip(), self.txt_telefone.get().strip()
        if not self.validar_cpf(cpf): return
        
        try:
            id_inst = self.instrutor_map[self.cb_instrutor.get()]
            aluno = Aluno(self.aluno_selecionado_id, nome, ''.join(filter(str.isdigit, cpf)), ''.join(filter(str.isdigit, telefone)), id_inst)
            self.dao.atualizar(aluno)
            messagebox.showinfo("Sucesso", "Aluno atualizado!")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    def excluir(self):
        if not self.aluno_selecionado_id: return
        if messagebox.askyesno("Confirmar", "Deseja realmente deletar o aluno?"):
            self.dao.deletar(self.aluno_selecionado_id)
            self.limpar_campos()
            self.atualizar_tabela()

    def atualizar_tabela(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        try:
            for alu in self.dao.listar_todos(self.txt_busca.get()):
                self.tree.insert("", "end", values=(alu.id, alu.nome, alu.cpf, alu.nome_instrutor if alu.nome_instrutor else "Sem Prof."))
        except Exception as e:
            print(f"Erro tabela: {e}")

    def carregar_aluno_selecionado(self, event):
        item = self.tree.selection()
        if item:
            valores = self.tree.item(item, "values")
            self.aluno_selecionado_id = valores[0]
            self.txt_nome.delete(0, tk.END)
            self.txt_nome.insert(0, valores[1])
            self.txt_cpf.delete(0, tk.END)
            self.txt_cpf.insert(0, valores[2])
            for alu in self.dao.listar_todos():
                if str(alu.id) == str(self.aluno_selecionado_id):
                    self.txt_telefone.delete(0, tk.END)
                    self.txt_telefone.insert(0, alu.telefone if alu.telefone else "")
                    self.cb_instrutor.set(alu.nome_instrutor if alu.nome_instrutor else "")

    def limpar_campos(self):
        self.aluno_selecionado_id = None
        self.txt_nome.delete(0, tk.END)
        self.txt_cpf.delete(0, tk.END)
        self.txt_telefone.delete(0, tk.END)