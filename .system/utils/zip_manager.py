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
        base_dir (str): Diretório base para validar e localizar os arquivos.
        temp_dir (str): Diretório onde o arquivo ZIP será salvo fisicamente.
        
    Returns:
        str: Caminho absoluto do arquivo ZIP gerado.
    """
    os.makedirs(temp_dir, exist_ok=True)
    zip_filename = f"download_{int(time.time())}.zip"
    zip_path = os.path.join(temp_dir, zip_filename)
    
    real_base = os.path.realpath(os.path.normpath(base_dir))
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for path in paths:
            safe_path = os.path.normpath(path)
            if safe_path.startswith('..'):
                continue
            
            full_path = os.path.join(base_dir, safe_path)
            if not os.path.exists(full_path):
                continue
                
            real_path = os.path.realpath(full_path)
            if not real_path.startswith(os.path.join(real_base, '')):
                continue
            
            if os.path.isfile(full_path):
                arcname = os.path.basename(full_path)
                zip_file.write(full_path, arcname=arcname)
            elif os.path.isdir(full_path):
                for root, dirs, files in os.walk(full_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(full_path))
                        zip_file.write(file_path, arcname=arcname)
    
    return zip_path
