import tkinter as tk
from tkinter import messagebox, ttk
from config.database import Database

class InstrutorView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.instrutor_selecionado_id = None
        
        self.bg_color = "#f4f6f9"
        self.primary_color = "#1e3d59"
        self.accent_color = "#17b978"
        self.danger_color = "#ff5e62"
        
        self.configure(bg=self.bg_color)
        self.criar_componentes()
        self.atualizar_tabela()

    def criar_componentes(self):
        main_container = tk.Frame(self, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=20, pady=15)

        lbl_titulo = tk.Label(main_container, text="CADASTRO DE INSTRUTORES", font=("Arial", 14, "bold"), fg=self.primary_color, bg=self.bg_color)
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        form_frame = tk.Frame(main_container, bg=self.bg_color)
        form_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        form_frame.columnconfigure(1, weight=1)

        tk.Label(form_frame, text="Nome Completo:", font=("Arial", 10, "bold"), bg=self.bg_color).grid(row=0, column=0, sticky="w", pady=6)
        self.txt_nome = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid")
        self.txt_nome.grid(row=0, column=1, sticky="ew", pady=6, padx=(10, 0))

        tk.Label(form_frame, text="Inscricao CREF:", font=("Arial", 10, "bold"), bg=self.bg_color).grid(row=1, column=0, sticky="w", pady=6)
        self.txt_cref = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid")
        self.txt_cref.grid(row=1, column=1, sticky="ew", pady=6, padx=(10, 0))

        btn_frame = tk.Frame(main_container, bg=self.bg_color)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        btn_style = {"font": ("Arial", 10, "bold"), "fg": "white", "bd": 0, "cursor": "hand2", "padx": 12, "pady": 6}

        tk.Button(btn_frame, text="Salvar Novo", bg=self.accent_color, command=self.salvar, **btn_style).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Atualizar", bg="#3a6073", command=self.atualizar, **btn_style).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Excluir", bg=self.danger_color, command=self.excluir, **btn_style).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Limpar", bg="#7f8c8d", command=self.limpar_campos, **btn_style).pack(side="left", padx=5)

        separator = ttk.Separator(main_container, orient="horizontal")
        separator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        tabela_frame = tk.Frame(main_container)
        tabela_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        main_container.rowconfigure(4, weight=1)

        self.tree = ttk.Treeview(tabela_frame, columns=("ID", "Nome", "CREF"), show="headings", height=6)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome do Profissional")
        self.tree.heading("CREF", text="Nº de Registro CREF")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nome", width=250, anchor="w")
        self.tree.column("CREF", width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.carregar_selecionado)

    def salvar(self):
        nome, cref = self.txt_nome.get().strip(), self.txt_cref.get().strip()
        if not nome or not cref:
            messagebox.showwarning("Validacao", "Nome e CREF sao obrigatorios!")
            return

        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO instrutor (nome, cref) VALUES (%s, %s)", (nome, cref))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Sucesso", "Instrutor cadastrado!")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    def atualizar(self):
        if not self.instrutor_selecionado_id: return
        nome, cref = self.txt_nome.get().strip(), self.txt_cref.get().strip()
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE instrutor SET nome=%s, cref=%s WHERE id=%s", (nome, cref, self.instrutor_selecionado_id))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Sucesso", "Cadastro atualizado!")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    def excluir(self):
        if not self.instrutor_selecionado_id: return
        if messagebox.askyesno("Confirmar", "Remover este instrutor?"):
            try:
                conn = Database.get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM instrutor WHERE id=%s", (self.instrutor_selecionado_id,))
                conn.commit()
                cursor.close()
                conn.close()
                self.limpar_campos()
                self.atualizar_tabela()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")

    def atualizar_tabela(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, cref FROM instrutor ORDER BY id")
            for r in cursor.fetchall(): self.tree.insert("", "end", values=r)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Erro listar: {e}")

    def carregar_selecionado(self, event):
        item = self.tree.selection()
        if item:
            valores = self.tree.item(item, "values")
            self.instrutor_selecionado_id = valores[0]
            self.txt_nome.delete(0, tk.END)
            self.txt_nome.insert(0, valores[1])
            self.txt_cref.delete(0, tk.END)
            self.txt_cref.insert(0, valores[2])

    def limpar_campos(self):
        self.instrutor_selecionado_id = None
        self.txt_nome.delete(0, tk.END)
        self.txt_cref.delete(0, tk.END)