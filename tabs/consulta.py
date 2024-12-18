import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
from utils.database import buscar_produto

# Caminho absoluto para o banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "produtos.db")

def criar_aba_consulta(notebook):
    """Cria a aba de Consulta de Produtos."""
    tab_consulta = tk.Frame(notebook, bg="#ffffff")
    notebook.add(tab_consulta, text="Consulta de Preços")

    # Variável de modo de busca
    modo_busca = tk.StringVar(value="codigo")

    # Estrutura de duas colunas
    frame_esquerda = tk.Frame(tab_consulta, bg="#ffffff", width=400)
    frame_esquerda.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    frame_direita = tk.Frame(tab_consulta, bg="#ffffff", width=600)
    frame_direita.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    tab_consulta.columnconfigure(0, weight=1)
    tab_consulta.columnconfigure(1, weight=1)

    # ====================== Coluna Esquerda (Busca) ======================
    tk.Label(frame_esquerda, text="Selecione o Modo de Busca:", bg="#ffffff", font=("Arial", 12)).pack(pady=5)
    frame_modo = tk.Frame(frame_esquerda, bg="#ffffff")
    frame_modo.pack(pady=5)
    tk.Radiobutton(frame_modo, text="Código de Barras", variable=modo_busca, value="codigo", bg="#ffffff",
                   font=("Arial", 10), command=lambda: alternar_busca()).pack(side="left", padx=10)
    tk.Radiobutton(frame_modo, text="Descrição", variable=modo_busca, value="descricao", bg="#ffffff",
                   font=("Arial", 10), command=lambda: alternar_busca()).pack(side="left", padx=10)

    # Busca por código
    frame_busca_codigo = tk.Frame(frame_esquerda, bg="#ffffff")
    tk.Label(frame_busca_codigo, text="Digite o Código de Barras:", bg="#ffffff", font=("Arial", 12)).pack()
    codigo_entry = tk.Entry(frame_busca_codigo, font=("Arial", 14))
    codigo_entry.pack(pady=5)
    codigo_entry.bind("<Return>", lambda event: buscar_por_codigo())

    # Busca por descrição com sugestões
    frame_busca_descricao = tk.Frame(frame_esquerda, bg="#ffffff")
    tk.Label(frame_busca_descricao, text="Buscar por Descrição:", bg="#ffffff", font=("Arial", 12)).pack()
    descricao_entry = tk.Entry(frame_busca_descricao, font=("Arial", 14))
    descricao_entry.pack(pady=5)
    sugestoes_listbox = tk.Listbox(frame_busca_descricao, height=5, font=("Arial", 12))
    sugestoes_listbox.pack(pady=5)
    descricao_entry.bind("<KeyRelease>", lambda event: buscar_por_descricao())
    sugestoes_listbox.bind("<<ListboxSelect>>", lambda event: selecionar_descricao())

    # ====================== Coluna Direita (Resultado) ======================
    resultado_label = tk.Label(frame_direita, text="", bg="#ffffff", font=("Arial", 12), justify="center")
    resultado_label.pack(pady=10)
    imagem_label = tk.Label(frame_direita, bg="#ffffff")
    imagem_label.pack(pady=10)

    # ====================== Funções ======================
    def alternar_busca():
        """Alterna entre busca por código e por descrição."""
        if modo_busca.get() == "codigo":
            frame_busca_descricao.pack_forget()
            frame_busca_codigo.pack(pady=10)
        else:
            frame_busca_codigo.pack_forget()
            frame_busca_descricao.pack(pady=10)

    def buscar_por_codigo():
        """Busca um produto pelo código."""
        codigo = codigo_entry.get()
        produto = buscar_produto(codigo)
        mostrar_resultado(produto)

    def buscar_por_descricao():
        """Busca sugestões de produtos pela descrição."""
        query = descricao_entry.get()
        sugestoes_listbox.delete(0, tk.END)
        if query:
            # Usa o caminho absoluto para acessar o banco de dados
            conexao = sqlite3.connect(DB_PATH)
            cursor = conexao.cursor()
            cursor.execute("SELECT descricao FROM produtos WHERE descricao LIKE ?", (f"%{query}%",))
            for row in cursor.fetchall():
                sugestoes_listbox.insert(tk.END, row[0])
            conexao.close()

    def selecionar_descricao():
        """Seleciona um produto da lista de sugestões."""
        descricao = sugestoes_listbox.get(sugestoes_listbox.curselection())
        # Usa o caminho absoluto para acessar o banco de dados
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos WHERE descricao = ?", (descricao,))
        produto = cursor.fetchone()
        conexao.close()
        mostrar_resultado(produto)

    def mostrar_resultado(produto):
        """Mostra os detalhes do produto no resultado."""
        if produto:
            resultado_label.config(text=f"Descrição: {produto[2]}\nPreço: R$ {produto[3]:.2f}")
            if produto[4] and os.path.exists(produto[4]):
                img = Image.open(produto[4]).resize((200, 200), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                imagem_label.config(image=img_tk)
                imagem_label.image = img_tk
        else:
            messagebox.showerror("Erro", "Produto não encontrado!")

    def limpar():
        """Limpa os campos e o resultado."""
        codigo_entry.delete(0, tk.END)
        descricao_entry.delete(0, tk.END)
        sugestoes_listbox.delete(0, tk.END)
        resultado_label.config(text="")
        imagem_label.config(image="")
        imagem_label.image = None

    # Botões
    button_frame = tk.Frame(frame_esquerda, bg="#ffffff")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Consultar", command=buscar_por_codigo, font=("Arial", 12), bg="#0078D7", fg="white",
              padx=10, pady=5).pack(side="left", padx=5)
    tk.Button(button_frame, text="Limpar", command=limpar, font=("Arial", 12), bg="#E81123", fg="white",
              padx=10, pady=5).pack(side="left", padx=5)

    # Inicializa a tela
    alternar_busca()
