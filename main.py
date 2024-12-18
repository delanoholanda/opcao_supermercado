import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utils.database import criar_tabelas
from tabs.cadastro import criar_aba_cadastro
from tabs.consulta import criar_aba_consulta
from tabs.visualizacao import criar_aba_visualizacao

# Variáveis globais para os campos de cadastro
codigo_entry = None
descricao_entry = None
preco_entry = None
imagem_path = None

def preencher_campos_cadastro(codigo, descricao, preco, imagem):
    """Preenche os campos da aba de cadastro com os dados fornecidos."""
    global codigo_entry, descricao_entry, preco_entry, imagem_path
    codigo_entry.delete(0, tk.END)
    descricao_entry.delete(0, tk.END)
    preco_entry.delete(0, tk.END)
    imagem_path.set("")

    codigo_entry.insert(0, codigo)
    descricao_entry.insert(0, descricao)
    preco_entry.insert(0, preco)
    imagem_path.set(imagem)

def iniciar_interface():
    criar_tabelas()  # Cria as tabelas no banco de dados, se não existirem

    # Configuração da janela principal
    app = tk.Tk()
    app.title("Opção Supermercado")
    app.geometry("1000x600")
    app.configure(bg="#f4f4f4")

        # Caminho absoluto para o arquivo logo.png
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "assets", "logo.png")

    # Cabeçalho com logo e nome
    frame_logo = tk.Frame(app, bg="#f4f4f4")
    frame_logo.pack(fill="x", pady=10)
    logo = Image.open(logo_path).resize((100, 100), Image.Resampling.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo)
    tk.Label(frame_logo, image=logo_tk, bg="#f4f4f4").pack(side="left", padx=10)
    tk.Label(frame_logo, text="Opção Supermercado", bg="#f4f4f4", font=("Arial", 24, "bold"), fg="#333").pack(side="left")

    # Notebook para as abas
    notebook = ttk.Notebook(app)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # ===================== Configuração Global =====================
    global codigo_entry, descricao_entry, preco_entry, imagem_path

    # Variáveis compartilhadas entre as abas
    imagem_path = tk.StringVar()

    # ===================== Criação das Abas =====================
    # Aba de Consulta
    criar_aba_consulta(notebook)
    
    # Aba de Cadastro
    # codigo_entry, descricao_entry, preco_entry = criar_aba_cadastro(notebook, imagem_path)


    # Aba de Visualização
    # criar_aba_visualizacao(notebook, preencher_campos_cadastro)

    carregar_visualizacao = criar_aba_visualizacao(notebook, preencher_campos_cadastro)
    criar_aba_cadastro(notebook, imagem_path, carregar_visualizacao)


    app.mainloop()

if __name__ == "__main__":
    iniciar_interface()
