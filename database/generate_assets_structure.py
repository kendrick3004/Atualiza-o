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

def ensure_parent_links(structure, abs_dir, target_dir, database_dir):
    """
    Ensures that abs_dir and all its parent directories up to target_dir
    exist in the structure and are correctly linked in their parents' "folders" lists.
    """
    abs_dir = os.path.abspath(abs_dir)
    abs_target = os.path.abspath(target_dir)
    
    if abs_dir == abs_target:
        if "database_root" not in structure:
            structure["database_root"] = {"files": [], "folders": []}
        return
        
    parent_dir = os.path.dirname(abs_dir)
    abs_parent = os.path.abspath(parent_dir)
    
    # Recursively ensure parent links exist first
    ensure_parent_links(structure, abs_parent, target_dir, database_dir)
    
    if abs_parent == abs_target:
        parent_key = "database_root"
    else:
        rel_parent = os.path.relpath(abs_parent, database_dir).replace(os.sep, "/")
        parent_key = "database/" + rel_parent
        
    rel_dir = os.path.relpath(abs_dir, database_dir).replace(os.sep, "/")
    dir_key = "database/" + rel_dir
    dir_name = os.path.basename(abs_dir)
    
    if dir_key not in structure:
        structure[dir_key] = {"files": [], "folders": []}
        
    if parent_key in structure:
        folders_list = structure[parent_key].setdefault("folders", [])
        exists = any(f["id"] == dir_key for f in folders_list)
        if not exists:
            try:
                folders_list.append({
                    "id": dir_key,
                    "name": dir_name,
                    "path": dir_key,
                    "modified": int(os.path.getmtime(abs_dir) * 1000),
                })
            except Exception:
                pass

def update_dir_contents(structure, abs_dir, target_dir, project_root, database_dir):
    """
    Scans the immediate contents of abs_dir and updates its entry in structure.
    """
    abs_dir = os.path.abspath(abs_dir)
    abs_target = os.path.abspath(target_dir)
    
    if abs_dir == abs_target:
        dir_key = "database_root"
    else:
        rel_dir = os.path.relpath(abs_dir, database_dir).replace(os.sep, "/")
        dir_key = "database/" + rel_dir
        
    files = []
    folders = []
    
    try:
        for item in os.listdir(abs_dir):
            if item in ["__pycache__", ".git"]:
                continue
            item_path = os.path.join(abs_dir, item)
            if os.path.isdir(item_path):
                folder_id = "database/" + os.path.relpath(item_path, database_dir).replace("\\", "/")
                try:
                    folders.append({
                        "id": folder_id,
                        "name": item,
                        "path": folder_id,
                        "modified": int(os.path.getmtime(item_path) * 1000),
                    })
                except Exception:
                    pass
            else:
                if item in ["generate_assets_structure.py", "philistudies.json"]:
                    continue
                file_info = get_file_info(item_path, project_root)
                if file_info:
                    files.append(file_info)
    except Exception:
        pass
        
    if dir_key not in structure:
        structure[dir_key] = {}
    structure[dir_key]["files"] = files
    structure[dir_key]["folders"] = folders

def update_incremental(structure, path, target_dir, project_root, database_dir):
    """
    Updates the JSON structure incrementally for a modified file or directory.
    """
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        # Handle deletion
        rel_from_db = os.path.relpath(abs_path, database_dir).replace(os.sep, "/")
        json_key = "database/" + rel_from_db
        if json_key in structure:
            del structure[json_key]
        
        parent_dir = os.path.dirname(abs_path)
        abs_parent = os.path.abspath(parent_dir)
        abs_target = os.path.abspath(target_dir)
        if abs_parent == abs_target:
            parent_key = "database_root"
        else:
            rel_parent = os.path.relpath(abs_parent, database_dir).replace(os.sep, "/")
            parent_key = "database/" + rel_parent
        
        name = os.path.basename(abs_path)
        if parent_key in structure:
            structure[parent_key]["files"] = [f for f in structure[parent_key].get("files", []) if f["name"] != name]
            structure[parent_key]["folders"] = [d for d in structure[parent_key].get("folders", []) if d["name"] != name]
        return structure

    if os.path.isdir(abs_path):
        ensure_parent_links(structure, abs_path, target_dir, database_dir)
        update_dir_contents(structure, abs_path, target_dir, project_root, database_dir)
    else:
        parent_dir = os.path.dirname(abs_path)
        ensure_parent_links(structure, parent_dir, target_dir, database_dir)
        
        abs_parent = os.path.abspath(parent_dir)
        abs_target = os.path.abspath(target_dir)
        if abs_parent == abs_target:
            parent_key = "database_root"
        else:
            rel_parent = os.path.relpath(abs_parent, database_dir).replace(os.sep, "/")
            parent_key = "database/" + rel_parent
            
        file_info = get_file_info(abs_path, project_root)
        if file_info:
            if parent_key not in structure:
                structure[parent_key] = {"files": [], "folders": []}
            structure[parent_key]["files"] = [f for f in structure[parent_key]["files"] if f["name"] != file_info["name"]]
            structure[parent_key]["files"].append(file_info)
            
    return structure

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
        # Atualização incremental inteligente
        structure = update_incremental(structure, specific_file, target_dir, project_root, database_dir)
            
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
