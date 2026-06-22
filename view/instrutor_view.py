import tkinter as tk
from tkinter import ttk, messagebox
from config.database import DatabaseConnection

class InstrutorView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.instrutor_selecionado_id = None
        self.criar_componentes()
        self.atualizar_tabela()

    def criar_componentes(self):
        # Configuração de Grid Responsivo para a Tela
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # -------------------------------------------------------------------------
        # PAINEL ESQUERDO: Formulário de Cadastro (Mesmo estilo do AlunoView)
        # -------------------------------------------------------------------------
        form_frame = ttk.LabelFrame(self, text=" Gestão de Instrutores ", padding=20)
        form_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

        # Campo Nome
        ttk.Label(form_frame, text="Nome Completo: *", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.txt_nome = ttk.Entry(form_frame, font=("Helvetica", 11), width=35)
        self.txt_nome.pack(fill=tk.X, pady=(0, 15))

        # Campo CREF
        ttk.Label(form_frame, text="Registro CREF: *", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.txt_cref = ttk.Entry(form_frame, font=("Helvetica", 11), width=35)
        self.txt_cref.pack(fill=tk.X, pady=(0, 25))

        # Container para os Botões de Ação (Estilo Bloco Uniforme)
        btn_container = ttk.Frame(form_frame)
        btn_container.pack(fill=tk.X, side=tk.BOTTOM, pady=(20, 0))

        self.btn_salvar = ttk.Button(btn_container, text="➕ Salvar Novo", command=self.salvar, style="Accent.TButton")
        self.btn_salvar.pack(fill=tk.X, pady=4)

        self.btn_atualizar = ttk.Button(btn_container, text="🔄 Atualizar Cadastro", command=self.atualizar)
        self.btn_atualizar.pack(fill=tk.X, pady=4)

        self.btn_excluir = ttk.Button(btn_container, text="❌ Excluir Instrutor", command=self.excluir)
        self.btn_excluir.pack(fill=tk.X, pady=4)

        ttk.Separator(btn_container, orient="horizontal").pack(fill=tk.X, pady=10)

        self.btn_limpar = ttk.Button(btn_container, text="🧹 Limpar Campos", command=self.limpar_campos)
        self.btn_limpar.pack(fill=tk.X, pady=4)

        # -------------------------------------------------------------------------
        # PAINEL DIREITO: Listagem de Dados (Mesmo design com Scrollbar)
        # -------------------------------------------------------------------------
        list_frame = ttk.LabelFrame(self, text=" Instrutores Cadastrados ", padding=15)
        list_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        colunas = ("id", "nome", "cref")
        self.tree = ttk.Treeview(list_frame, columns=colunas, show="headings", selectmode="browse")
        
        # Cabeçalhos
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome do Profissional")
        self.tree.heading("cref", text="CREF")

        # Alinhamentos e Larguras
        self.tree.column("id", width=60, minwidth=50, anchor=tk.CENTER)
        self.tree.column("nome", width=280, minwidth=200, anchor=tk.W)
        self.tree.column("cref", width=140, minwidth=100, anchor=tk.CENTER)

        # Scrollbar Integrada
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Evento de Clique na Linha da Tabela
        self.tree.bind("<<TreeviewSelect>>", self.carregar_campos_selecionados)

    # -------------------------------------------------------------------------
    # MÉTODOS DE REGRA DE NEGÓCIO E PERSISTÊNCIA VIA SINGLETON
    # -------------------------------------------------------------------------
    def salvar(self):
        nome, cref = self.txt_nome.get().strip(), self.txt_cref.get().strip()
        if not nome or not cref:
            messagebox.showwarning("Validação", "Os campos Nome e CREF são obrigatórios!")
            return

        try:
            conn = DatabaseConnection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO instrutor (nome, cref) VALUES (%s, %s)", (nome, cref))
            conn.commit()
            cursor.close()
            messagebox.showinfo("Sucesso", "Instrutor cadastrado com sucesso!")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}")

    def atualizar(self):
        if not self.instrutor_selecionado_id:
            messagebox.showwarning("Seleção", "Selecione um instrutor na tabela para atualizar!")
            return
        
        nome, cref = self.txt_nome.get().strip(), self.txt_cref.get().strip()
        if not nome or not cref:
            messagebox.showwarning("Validação", "Os campos não podem ficar vazios!")
            return

        try:
            conn = DatabaseConnection()
            cursor = conn.cursor()
            cursor.execute("UPDATE instrutor SET nome=%s, cref=%s WHERE id=%s", (nome, cref, self.instrutor_selecionado_id))
            conn.commit()
            cursor.close()
            messagebox.showinfo("Sucesso", "Cadastro de instrutor atualizado!")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

    def excluir(self):
        if not self.instrutor_selecionado_id:
            messagebox.showwarning("Seleção", "Selecione um instrutor na tabela para excluir!")
            return
            
        if messagebox.askyesno("Confirmar Exclusão", "Deseja realmente remover este instrutor?\n\nNota: Alunos vinculados a ele ficarão com a indicação de instrutor vazia."):
            try:
                conn = DatabaseConnection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM instrutor WHERE id=%s", (self.instrutor_selecionado_id,))
                conn.commit()
                cursor.close()
                messagebox.showinfo("Sucesso", "Instrutor removido do sistema!")
                self.limpar_campos()
                self.atualizar_tabela()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = DatabaseConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, cref FROM instrutor ORDER BY id")
            for r in cursor.fetchall():
                self.tree.insert("", "end", values=r)
            cursor.close()
        except Exception as e:
            print(f"Erro ao atualizar tabela de instrutores: {e}")

    def carregar_campos_selecionados(self, event):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            return
            
        valores = self.tree.item(item_selecionado[0], "values")
        self.instrutor_selecionado_id = valores[0]
        
        self.txt_nome.delete(0, tk.END)
        self.txt_nome.insert(0, valores[1])
        
        self.txt_cref.delete(0, tk.END)
        self.txt_cref.insert(0, valores[2])

    def limpar_campos(self):
        self.instrutor_selecionado_id = None
        self.txt_nome.delete(0, tk.END)
        self.txt_cref.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())