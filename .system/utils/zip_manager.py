import os
import zipfile
import time
from io import BytesIO

def create_zip_file(paths, base_dir, temp_dir):
    """
    Compacta arquivos e pastas, salva fisicamente na pasta .temp e retorna o caminho do arquivo.
    Os arquivos ZIP são mantidos na pasta .temp como histórico.
    
    Args:
        paths (list): Lista de caminhos relativos ao base_dir.
                      Exemplo: 'files/dev' ou 'files/dev/avatar/avatar.jpg'
                      Não deve incluir o prefixo 'database/' pois base_dir já aponta para 'database/'.
        base_dir (str): Diretório base para validar e localizar os arquivos (ex: .../database).
        temp_dir (str): Diretório onde o arquivo ZIP será salvo fisicamente.
        
    Returns:
        str: Caminho absoluto do arquivo ZIP gerado.
        
    Raises:
        ValueError: Se nenhum arquivo válido for encontrado nos caminhos fornecidos.
    """
    os.makedirs(temp_dir, exist_ok=True)
    zip_filename = f"download_{int(time.time())}.zip"
    zip_path = os.path.join(temp_dir, zip_filename)
    
    real_base = os.path.realpath(os.path.normpath(base_dir))
    files_added = 0
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for path in paths:
            # Normalizar separadores e remover prefixo 'database/' caso venha com ele
            clean_path = path.replace('\\', '/').strip('/')
            if clean_path.startswith('database/'):
                clean_path = clean_path[len('database/'):]
            
            safe_path = os.path.normpath(clean_path)
            if safe_path.startswith('..'):
                continue
            
            full_path = os.path.join(base_dir, safe_path)
            if not os.path.exists(full_path):
                continue
                
            real_path = os.path.realpath(full_path)
            # Segurança: garantir que o caminho está dentro do base_dir
            if not (real_path == real_base or real_path.startswith(real_base + os.sep)):
                continue
            
            if os.path.isfile(full_path):
                # Arquivo individual: preservar apenas o nome do arquivo no ZIP
                arcname = os.path.basename(full_path)
                zip_file.write(full_path, arcname=arcname)
                files_added += 1
            elif os.path.isdir(full_path):
                # Pasta: preservar estrutura interna relativa ao pai da pasta selecionada
                parent_dir = os.path.dirname(full_path)
                for root, dirs, walk_files in os.walk(full_path):
                    # Remover pastas ocultas e __pycache__
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
                    for file in walk_files:
                        if file.startswith('.'):
                            continue
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, parent_dir)
                        zip_file.write(file_path, arcname=arcname)
                        files_added += 1
    
    if files_added == 0:
        raise ValueError(f"Nenhum arquivo válido encontrado nos caminhos: {paths}")
    
    return zip_path
