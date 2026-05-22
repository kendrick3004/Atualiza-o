import json
import os
import sys
import time

def get_file_info(path, project_root):
    """
    Collects detailed information about an individual file.
    
    Args:
        path (str): Absolute path to the file.
        project_root (str): The root directory of the project.
        
    Returns:
        dict: A dictionary containing file metadata (id, name, path, size, etc.) or None if an error occurs.
    """
    try:
        stat = os.stat(path)
        abs_path = os.path.abspath(path)
        database_dir = os.path.join(project_root, "database")
        
        # O path no JSON deve ser relativo à pasta 'database' para o Flask servir corretamente
        rel_path = "database/" + os.path.relpath(abs_path, database_dir).replace("\\", "/")

        ext = os.path.splitext(path)[1][1:].lower()

        if ext in ["jpg", "jpeg", "png", "gif", "svg", "webp"]:
            type_cat = "image"
        elif ext in ["pdf"]:
            type_cat = "pdf"
        elif ext in ["zip", "rar", "7z", "tar", "gz"]:
            type_cat = "archive"
        elif ext in ["js", "html", "css", "py", "php", "json", "ts"]:
            type_cat = "code"
        elif ext in ["mp4", "webm", "ogg", "mov"]:
            type_cat = "video"
        elif ext in ["mp3", "wav", "flac"]:
            type_cat = "audio"
        elif ext in ["ttf", "otf", "woff", "woff2"]:
            type_cat = "font"
        else:
            type_cat = "file"

        return {
            "id": rel_path,
            "name": os.path.basename(path),
            "path": rel_path,
            "size": stat.st_size,
            "extension": ext,
            "type": type_cat,
            "modified": int(stat.st_mtime * 1000),
            "preview": rel_path if type_cat == "image" else None,
        }
    except Exception:
        return None

def generate_structure(target_dir, project_root, specific_file=None):
    """
    Scans the 'files' directory and generates a JSON structure representing the database.
    
    Args:
        target_dir (str): The directory to scan for files.
        project_root (str): The root directory of the project.
        specific_file (str, optional): If provided, performs an incremental update for this specific file only.
        
    Returns:
        dict: The generated or updated structure dictionary.
    """
    database_dir = os.path.join(project_root, "database")
    output_path = os.path.join(database_dir, "philistudies.json")
    
    structure = {}
    if specific_file and os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                structure = json.load(f)
        except Exception:
            structure = {}

    if not structure or not specific_file:
        # Geração completa
        structure = {}
        for root, dirs, files in os.walk(target_dir):
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")
            if ".git" in dirs:
                dirs.remove(".git")

            abs_root = os.path.abspath(root)
            abs_target = os.path.abspath(target_dir)
            
            if abs_root == abs_target:
                json_key = "database_root"
            else:
                # Garante que o caminho relativo seja calculado corretamente e use barras normais (Linux style)
                rel_from_db = os.path.relpath(abs_root, database_dir).replace(os.sep, "/")
                json_key = "database/" + rel_from_db

            current_entry = {"files": [], "folders": []}

            for d in dirs:
                folder_path = os.path.join(root, d)
                folder_id = "database/" + os.path.relpath(folder_path, database_dir).replace("\\", "/")
                try:
                    current_entry["folders"].append({
                        "id": folder_id,
                        "name": d,
                        "path": folder_id,
                        "modified": int(os.path.getmtime(folder_path) * 1000),
                    })
                except Exception: pass

            for f in files:
                if f in ["generate_assets_structure.py", "philistudies.json"]: continue
                file_path = os.path.join(root, f)
                file_info = get_file_info(file_path, project_root)
                if file_info:
                    current_entry["files"].append(file_info)

            structure[json_key] = current_entry
    else:
        # Atualização incremental para um arquivo específico
        abs_file_path = os.path.abspath(specific_file)
        file_dir = os.path.dirname(abs_file_path)
        abs_file_dir = os.path.abspath(file_dir)
        abs_target = os.path.abspath(target_dir)
        
        if abs_file_dir == abs_target:
            json_key = "database_root"
        else:
            rel_from_db = os.path.relpath(abs_file_dir, database_dir).replace(os.sep, "/")
            json_key = "database/" + rel_from_db
        
        file_info = get_file_info(abs_file_path, project_root)
        if file_info:
            if json_key not in structure:
                structure[json_key] = {"files": [], "folders": []}
            
            # Remover versão antiga se existir
            structure[json_key]["files"] = [f for f in structure[json_key]["files"] if f["name"] != file_info["name"]]
            # Adicionar nova versão
            structure[json_key]["files"].append(file_info)
            
            # Garantir que as pastas pai existam na estrutura (simplificado)
            # Em um sistema real, poderíamos subir a árvore, mas aqui focamos no arquivo
            
    return structure

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_script_dir, ".."))
    files_path = os.path.join(current_script_dir, "files")
    output_path = os.path.join(current_script_dir, "philistudies.json")

    specific_file = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        structure = generate_structure(files_path, project_root, specific_file)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(structure, f, indent=4, ensure_ascii=False)
        print(f"Estrutura {'atualizada' if specific_file else 'gerada'} com sucesso.")
        sys.exit(0)
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
