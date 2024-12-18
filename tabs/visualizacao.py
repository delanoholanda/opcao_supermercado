import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

# Caminho absoluto para o banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "produtos.db")

def criar_aba_visualizacao(notebook, preencher_campos_cadastro):
    """Cria a aba de Visualização de Produtos."""
    tab_visualizar = tk.Frame(notebook, bg="#ffffff")
    notebook.add(tab_visualizar, text="Visualizar Produtos")

    imagem_cache = {}  # Cache para armazenar imagens em miniatura

    # Configuração do Treeview (tabela)
    columns = ("Imagem", "Código", "Descrição", "Preço")
    tree = ttk.Treeview(tab_visualizar, columns=columns, show="headings", height=15)
    tree.heading("Imagem", text="Imagem")
    tree.heading("Código", text="Código")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Preço", text="Preço")
    tree.column("Imagem", width=100, anchor="center")
    tree.column("Código", width=100, anchor="center")
    tree.column("Descrição", width=300)
    tree.column("Preço", width=100, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Botões Editar e Excluir
    button_frame = tk.Frame(tab_visualizar, bg="#ffffff")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Editar Produto", command=lambda: editar_produto(), font=("Arial", 12),
              bg="#0078D7", fg="white", padx=10, pady=5).pack(side="left", padx=5)
    tk.Button(button_frame, text="Excluir Produto", command=lambda: excluir_produto(), font=("Arial", 12),
              bg="#E81123", fg="white", padx=10, pady=5).pack(side="left", padx=5)
    tk.Button(button_frame, text="Atualizar Lista", command=lambda: carregar_dados(), font=("Arial", 12),
              bg="#107C10", fg="white", padx=10, pady=5).pack(side="left", padx=5)

    # Função para carregar dados no Treeview
    def carregar_dados():
        """Carrega os produtos do banco de dados na tabela."""
        for row in tree.get_children():
            tree.delete(row)
        imagem_cache.clear()

        # Usa o caminho absoluto para acessar o banco de dados
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        cursor.execute("SELECT codigo, descricao, preco, imagem FROM produtos")
        for codigo, descricao, preco, imagem_path in cursor.fetchall():
            if imagem_path and os.path.exists(imagem_path):
                # Carregar imagem e redimensionar para miniatura
                img = Image.open(imagem_path).resize((50, 50), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                imagem_cache[codigo] = img_tk  # Salva a imagem no cache
                tree.insert("", "end", iid=codigo, values=("", codigo, descricao, f"R$ {preco:.2f}"), image=img_tk)
            else:
                tree.insert("", "end", iid=codigo, values=("", codigo, descricao, f"R$ {preco:.2f}"))
        conexao.close()

    # Função para editar um produto
    def editar_produto():
        """Edita o produto selecionado."""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um produto para editar!")
            return

        # Pega os dados da linha selecionada
        item = tree.item(selecionado, "values")
        codigo, descricao, preco = item[1], item[2], item[3].replace("R$ ", "")

        # Busca o caminho da imagem no banco
        conexao = sqlite3.connect("database/produtos.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT imagem FROM produtos WHERE codigo = ?", (codigo,))
        resultado = cursor.fetchone()
        conexao.close()

        imagem = resultado[0] if resultado and resultado[0] else ""  # Verifica se o valor existe

        # Preenche os campos da aba de cadastro
        preencher_campos_cadastro(codigo, descricao, preco, imagem)
        messagebox.showinfo("Modo de Edição", "Edite os campos e clique em Salvar Produto.")


    # Função para excluir um produto
    def excluir_produto():
        """Exclui o produto selecionado após confirmação."""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um produto para excluir!")
            return

        # Confirmação
        codigo = tree.item(selecionado, "values")[1]
        confirmar = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o produto '{codigo}'?")
        if confirmar:
            conexao = sqlite3.connect("database/produtos.db")
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM produtos WHERE codigo = ?", (codigo,))
            conexao.commit()
            conexao.close()
            carregar_dados()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

    # Carregar dados iniciais
    carregar_dados()
    return carregar_dados
