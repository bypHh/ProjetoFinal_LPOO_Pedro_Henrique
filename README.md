# FitManager Pro — Sistema de Gestão Integrada de Academia

O **FitManager Pro** é uma aplicação desktop robusta desenvolvida em Python para a gestão operacional e técnica de academias de ginástica e centros fitness. O sistema foi projetado seguindo rigorosamente os princípios da **Orientação a Objetos (OO)** e o padrão de arquitetura em camadas **MVC (Model-View-DAO)**, garantindo modularidade, facilidade de manutenção e extensibilidade.

A aplicação oferece um ecossistema completo para a administração de matrículas de alunos, vínculo com profissionais de educação física (instrutores) e prescrição dinâmica e automatizada de rotinas de treinamento por meio de padrões de projeto de software (Design Patterns).

---

## 🛠️ Tecnologias e Ambiente Técnico

* **Linguagem de Programação:** Python 3.10+
* **Interface Gráfica (GUI):** Tkinter & Ttk (Componentes com design customizado e responsivo)
* **Banco de Dados Relacional:** PostgreSQL 14+
* **Driver de Conectividade:** `psycopg2` (Operações e transações puras e seguras)
* **Paradigma Principal:** Programação Orientada a Objetos (Herança, Encapsulamento, Polimorfismo e Abstração)

---

## 🏗️ Padrões de Projeto (Design Patterns) Implementados

Para atender às exigências de arquitetura avançada de software, o sistema faz uso explícito de dois padrões de projeto:

### 1. DAO (Data Access Object) — *Padrão de Persistência*
Toda a lógica de manipulação e persistência de dados está completamente isolada da interface gráfica. As classes `AlunoDAO` e `TreinoDAO` abstraem os comandos SQL puros (`INSERT`, `SELECT`, `UPDATE`, `DELETE`), atuando como pontes exclusivas entre o banco de dados PostgreSQL e as regras de negócio das entidades. Isso impede o acoplamento e facilita a manutenção.

### 2. Factory Method (Método Fábrica) — *Padrão Criacional*
Implementado com sucesso no domínio de prescrição de treinos através da classe `TreinoFactory` (localizada em `model/treino.py`). A interface do sistema não instancia objetos da classe `Treino` diretamente. Em vez disso, ela delega essa responsabilidade para o método fábrica, que analisa a categoria de treino selecionada pelo usuário (**Hipertrofia**, **Cardio** ou **Geral**) e constrói dinamicamente o objeto com as descrições técnicas e diretrizes predefinidas.

---

## 📊 Diagrama de Classes UML

Abaixo está o mapeamento visual das entidades do sistema, seus respectivos atributos, métodos e os relacionamentos de associação e dependência:

**[Diagrama de Classes do Sistema]**

<img width="944" height="623" alt="image" src="https://github.com/user-attachments/assets/7c82cee9-3a55-460d-bfd0-6211cdb7482d" />

---

## 📂 Estrutura Arquitetural do Projeto

```text
Sistema_Academia/
│
├── config/
│   └── database.py        # Configurações de conexão e encoding com o PostgreSQL
│
├── model/
│   ├── aluno.py           # Classe de domínio Aluno
│   ├── instrutor.py       # Classe de domínio Instrutor
│   └── treino.py          # Classe de domínio Treino + Fábrica Criacional
│
├── dao/
│   ├── aluno_dao.py       # Persistência de dados e CRUD de alunos e instrutores
│   └── treino_dao.py      # Persistência de dados e sub-rotinas de fichas técnicas
│
├── view/
│   ├── main_window.py     # Janela Mestre (Controle de navegação superior e menus)
│   ├── aluno_view.py      # Interface de gestão de Alunos, filtros e validações
│   ├── instrutor_view.py  # Interface de gestão de Instrutores e registros CREF
│   └── treino_view.py     # Interface de montagem automatizada via Factory Method
│
└── main.py                # Entry Point que inicializa a aplicação

```
---

## 🤖 Declaração de Uso de Inteligência Artificial e Autoria Assistida

Em estrita conformidade com as diretrizes e critérios de integridade acadêmica estabelecidos para a Atividade Integradora Final da disciplina de LPOO, declara-se que este projeto foi **totalmente idealizado, estruturado e pilotado pelo desenvolvedor Pedro Henrique**, contando com o suporte assistido do modelo de inteligência artificial generativa (**Gemini 1.5 Pro**) atuando estritamente como copiloto técnico nas seguintes sub-rotinas:

1. **Refatoração Estática da Interface:** Suporte na padronização visual dos componentes `ttk.Style` utilizando uma paleta de cores moderna (Modern Blue Layout).
2. **Otimização de Algoritmos:** Auxílio na estruturação analítica dos loops de cálculo para validação matemática dos dígitos verificadores do CPF (recomendações da Receita Federal).
3. **Resolução de Exceções de Ambiente:** Suporte na parametrização de encodings locais (`client_encoding="latin1"`) para evitar quebras de caractere e conflitos entre o driver `psycopg2` e o prompt de comando do Windows.
