import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3

def criar_aba_cadastro(notebook, imagem_path, carregar_visualizacao):
    """Cria a aba de Cadastro de Produtos."""
    tab_cadastro = tk.Frame(notebook, bg="#ffffff")
    notebook.add(tab_cadastro, text="Cadastro de Produtos")

    # Campos de cadastro
    tk.Label(tab_cadastro, text="Código de Barras", bg="#ffffff", font=("Arial", 12)).pack(pady=5)
    codigo_entry = tk.Entry(tab_cadastro, font=("Arial", 12))
    codigo_entry.pack(pady=5)

    tk.Label(tab_cadastro, text="Descrição", bg="#ffffff", font=("Arial", 12)).pack(pady=5)
    descricao_entry = tk.Entry(tab_cadastro, font=("Arial", 12))
    descricao_entry.pack(pady=5)

    tk.Label(tab_cadastro, text="Preço", bg="#ffffff", font=("Arial", 12)).pack(pady=5)
    preco_entry = tk.Entry(tab_cadastro, font=("Arial", 12))
    preco_entry.pack(pady=5)

    tk.Label(tab_cadastro, text="Imagem", bg="#ffffff", font=("Arial", 12)).pack(pady=5)
    tk.Button(tab_cadastro, text="Selecionar Imagem", command=lambda: selecionar_imagem(imagem_path),
              font=("Arial", 12), bg="#0078D7", fg="white").pack(pady=5)

    def salvar_produto():
        """Salva o produto no banco de dados."""
        try:
            conexao = sqlite3.connect("database/produtos.db")
            cursor = conexao.cursor()
            codigo = codigo_entry.get()
            descricao = descricao_entry.get()
            preco = float(preco_entry.get().replace(",", "."))
            imagem = imagem_path.get()

            # Verificar duplicidade
            cursor.execute("SELECT * FROM produtos WHERE codigo = ?", (codigo,))
            if cursor.fetchone():
                cursor.execute("UPDATE produtos SET descricao = ?, preco = ?, imagem = ? WHERE codigo = ?",
                               (descricao, preco, imagem, codigo))
                mensagem = "Produto atualizado com sucesso!"
            else:
                cursor.execute("INSERT INTO produtos (codigo, descricao, preco, imagem) VALUES (?, ?, ?, ?)",
                               (codigo, descricao, preco, imagem))
                mensagem = "Produto cadastrado com sucesso!"

            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", mensagem)
            limpar_campos()
            carregar_visualizacao()  # Atualiza a lista na aba de visualização
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido!")

    def limpar_campos():
        """Limpa os campos do formulário."""
        codigo_entry.delete(0, tk.END)
        descricao_entry.delete(0, tk.END)
        preco_entry.delete(0, tk.END)
        imagem_path.set("")

    def selecionar_imagem(path_var):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        path_var.set(caminho)

    tk.Button(tab_cadastro, text="Salvar Produto", command=salvar_produto, font=("Arial", 12),
              bg="#107C10", fg="white").pack(pady=10)

    return codigo_entry, descricao_entry, preco_entry
