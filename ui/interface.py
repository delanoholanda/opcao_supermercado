import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from utils.database import criar_tabelas, adicionar_produto, buscar_produto
import sqlite3
import os

def iniciar_interface():
    criar_tabelas()  # Garante que o banco e tabelas existem

    # Configuração da janela principal
    app = tk.Tk()
    app.title("Opção Supermercado")
    app.geometry("1000x600")
    app.configure(bg="#f4f4f4")

    # Caminho absoluto para o arquivo logo.png
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "assets", "logo.png")

    # Nome e logo
    frame_logo = tk.Frame(app, bg="#f4f4f4")
    frame_logo.pack(fill="x", pady=10)
    logo = Image.open(logo_path).resize((100, 100), Image.Resampling.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo)
    tk.Label(frame_logo, image=logo_tk, bg="#f4f4f4").pack(side="left", padx=10)
    tk.Label(frame_logo, text="Opção Supermercado", bg="#f4f4f4", font=("Arial", 24, "bold"), fg="#333").pack(side="left")

    notebook = ttk.Notebook(app)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # =================== Aba de Consulta ===================
    tab_consulta = tk.Frame(notebook, bg="#ffffff")
    notebook.add(tab_consulta, text="Consulta de Preços")

    # Modo de busca
    modo_busca = tk.StringVar(value="codigo")
    tk.Label(tab_consulta, text="Selecione o Modo de Busca:", bg="#ffffff", font=("Arial", 12)).pack(pady=5)
    modos_frame = tk.Frame(tab_consulta, bg="#ffffff")
    modos_frame.pack(pady=5)
    tk.Radiobutton(modos_frame, text="Código de Barras", variable=modo_busca, value="codigo", bg="#ffffff",
                   font=("Arial", 10), command=lambda: alternar_busca()).pack(side="left", padx=10)
    tk.Radiobutton(modos_frame, text="Descrição", variable=modo_busca, value="descricao", bg="#ffffff",
                   font=("Arial", 10), command=lambda: alternar_busca()).pack(side="left", padx=10)

    # Busca por código
    busca_codigo_frame = tk.Frame(tab_consulta, bg="#ffffff")
    tk.Label(busca_codigo_frame, text="Digite o Código de Barras", bg="#ffffff", font=("Arial", 12)).pack(pady=5)
    consulta_codigo_entry = tk.Entry(busca_codigo_frame, font=("Arial", 14), justify="center")
    consulta_codigo_entry.pack(pady=5)

    # Busca por descrição
    busca_descricao_frame = tk.Frame(tab_consulta, bg="#ffffff")
    tk.Label(busca_descricao_frame, text="Buscar por Descrição", bg="#ffffff", font=("Arial", 12)).pack(pady=5)
    descricao_busca_entry = tk.Entry(busca_descricao_frame, font=("Arial", 14), justify="center")
    descricao_busca_entry.pack(pady=5)
    lista_sugestoes = tk.Listbox(busca_descricao_frame, height=5, font=("Arial", 12))
    lista_sugestoes.pack(pady=5)

    # Resultado e imagem
    resultado_label = tk.Label(tab_consulta, text="", bg="#ffffff", font=("Arial", 12))
    resultado_label.pack(pady=10)
    imagem_label = tk.Label(tab_consulta, bg="#ffffff")
    imagem_label.pack(pady=10)

    def alternar_busca():
        """Alterna entre os modos de busca."""
        if modo_busca.get() == "codigo":
            busca_descricao_frame.pack_forget()
            busca_codigo_frame.pack()
        else:
            busca_codigo_frame.pack_forget()
            busca_descricao_frame.pack()

    def consultar():
        """Consulta pelo código ou descrição."""
        if modo_busca.get() == "codigo":
            produto = buscar_produto(consulta_codigo_entry.get())
        else:
            produto = buscar_por_descricao()
        if produto:
            resultado_label.config(text=f"Descrição: {produto[2]}\nPreço: R$ {produto[3]:.2f}")
            if produto[4] and os.path.exists(produto[4]):
                img = Image.open(produto[4]).resize((200, 200), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                imagem_label.config(image=img_tk)
                imagem_label.image = img_tk
        else:
            messagebox.showerror("Erro", "Produto não encontrado!")

    def limpar_pesquisa():
        """Limpa os campos e resultados."""
        consulta_codigo_entry.delete(0, tk.END)
        descricao_busca_entry.delete(0, tk.END)
        lista_sugestoes.delete(0, tk.END)
        resultado_label.config(text="")
        imagem_label.config(image="")
        imagem_label.image = None

    def buscar_por_descricao():
        descricao = lista_sugestoes.get(lista_sugestoes.curselection())
        conexao = sqlite3.connect("database/produtos.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos WHERE descricao = ?", (descricao,))
        produto = cursor.fetchone()
        conexao.close()
        return produto

    def buscar_sugestoes(event):
        query = descricao_busca_entry.get()
        lista_sugestoes.delete(0, tk.END)
        if query:
            conexao = sqlite3.connect("database/produtos.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT descricao FROM produtos WHERE descricao LIKE ?", (f"%{query}%",))
            for row in cursor.fetchall():
                lista_sugestoes.insert(tk.END, row[0])
            conexao.close()

    descricao_busca_entry.bind("<KeyRelease>", buscar_sugestoes)
    lista_sugestoes.bind("<<ListboxSelect>>", lambda event: consultar())

    # Botões
    button_frame = tk.Frame(tab_consulta, bg="#ffffff")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Consultar", command=consultar, font=("Arial", 12), bg="#0078D7", fg="white",
              padx=10, pady=5).pack(side="left", padx=5)
    tk.Button(button_frame, text="Limpar", command=limpar_pesquisa, font=("Arial", 12), bg="#E81123", fg="white",
              padx=10, pady=5).pack(side="left", padx=5)

    alternar_busca()

    # =================== Aba de Cadastro ===================
    tab_cadastro = tk.Frame(notebook, bg="#ffffff")
    notebook.add(tab_cadastro, text="Cadastro de Produtos")

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
    imagem_path = tk.StringVar()
    tk.Button(tab_cadastro, text="Selecionar Imagem", command=lambda: selecionar_imagem(imagem_path),
              font=("Arial", 12), bg="#0078D7", fg="white", borderwidth=0).pack(pady=5)

    def salvar_produto():
        try:
            conexao = sqlite3.connect("database/produtos.db")
            cursor = conexao.cursor()
            codigo = codigo_entry.get()
            descricao = descricao_entry.get()
            preco = float(preco_entry.get().replace(",", "."))
            imagem = imagem_path.get()

            # Verifica duplicidade do código
            cursor.execute("SELECT * FROM produtos WHERE codigo = ?", (codigo,))
            if cursor.fetchone():
                messagebox.showerror("Erro", "Código de barras já cadastrado!")
                return

            cursor.execute("INSERT INTO produtos (codigo, descricao, preco, imagem) VALUES (?, ?, ?, ?)",
                           (codigo, descricao, preco, imagem))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            limpar_campos()
            carregar_dados()
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido! Use valores numéricos (ex: 1.50).")

    def limpar_campos():
        codigo_entry.delete(0, tk.END)
        descricao_entry.delete(0, tk.END)
        preco_entry.delete(0, tk.END)
        imagem_path.set("")

    tk.Button(tab_cadastro, text="Salvar Produto", command=salvar_produto, font=("Arial", 12), bg="#0078D7", fg="white",
              padx=10, pady=5).pack(pady=10)

    # =================== Aba de Visualização ===================
    tab_visualizar = tk.Frame(notebook, bg="#ffffff")
    notebook.add(tab_visualizar, text="Visualizar Produtos")

    # Configurações do Treeview
    tree = ttk.Treeview(tab_visualizar, columns=("Código", "Descrição", "Preço", "Ações"), show="headings", height=15)
    tree.heading("Código", text="Código de Barras")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Preço", text="Preço (R$)")
    tree.heading("Ações", text="Ações")
    tree.column("Ações", width=100, anchor="center")
    tree.pack(fill="both", expand=True)

    imagem_cache = {}  # Cache para imagens

    def carregar_dados():
        for row in tree.get_children():
            tree.delete(row)
        conexao = sqlite3.connect("database/produtos.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT codigo, descricao, preco, imagem FROM produtos")
        for codigo, descricao, preco, imagem_path in cursor.fetchall():
            # Carregar imagem se disponível
            if imagem_path and os.path.exists(imagem_path):
                img = Image.open(imagem_path).resize((50, 50), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                imagem_cache[codigo] = img_tk
                tree.insert("", "end", values=(codigo, descricao, f"R$ {preco:.2f}", "Editar/Excluir"), image=imagem_cache[codigo])
            else:
                tree.insert("", "end", values=(codigo, descricao, f"R$ {preco:.2f}", "Editar/Excluir"))
        conexao.close()

    def excluir_produto():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um produto para excluir!")
            return
        codigo = tree.item(selecionado)["values"][0]
        conexao = sqlite3.connect("database/produtos.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produtos WHERE codigo = ?", (codigo,))
        conexao.commit()
        conexao.close()
        carregar_dados()
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

    tk.Button(tab_visualizar, text="Excluir Produto", command=excluir_produto, font=("Arial", 12), bg="#E81123", fg="white",
              padx=10, pady=5).pack(pady=10)

    carregar_dados()

    def selecionar_imagem(path_var):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        path_var.set(caminho)

    # =================== Funções Gerais ===================
    def selecionar_imagem(path_var):
        """Seleciona a imagem do produto."""
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        path_var.set(caminho)


    app.mainloop()
