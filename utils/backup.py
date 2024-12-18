import shutil
import os
from datetime import datetime

def realizar_backup():
    """Cria um backup do banco de dados."""
    origem = os.path.join("database", "produtos.db")
    destino_dir = "backup"
    os.makedirs(destino_dir, exist_ok=True)
    
    # Nome do backup com data
    nome_backup = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.db"
    destino = os.path.join(destino_dir, nome_backup)
    
    shutil.copy(origem, destino)
    print(f"Backup realizado com sucesso: {destino}")
