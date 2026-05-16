from flask import render_template, request, send_file, redirect, url_for, send_from_directory, jsonify
import os
import sys
import subprocess
from werkzeug.utils import secure_filename
from functools import wraps
import json
import zipfile
import time
from io import BytesIO

def register_routes(app, config):
    """
    Registra todas as rotas e redirecionamentos no aplicativo Flask.
    config: dicionário contendo caminhos e funções auxiliares (registrar_log, generate_structure_json, etc.)
    """
    
    BASE_DIR = config['BASE_DIR']
    DATABASE_DIR = config['DATABASE_DIR']
    MAINTENANCE_DIR = config['MAINTENANCE_DIR']
    UPLOAD_FOLDER = config['UPLOAD_FOLDER']
    registrar_log = config['registrar_log']
    generate_structure_json = config['generate_structure_json']
    send_error_file = config['send_error_file']

    # --- Rotas de Páginas Principais ---
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/calendar')
    def calendar():
        return render_template('pages/calendar.html')

    @app.route('/login')
    def login():
        return render_template('pages/login.html')

    # --- Middleware de Autenticação ---
    
    def require_auth(f):
        """Decorator para exigir autenticação via Firebase token no backend"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar se há um token Firebase válido no header ou cookie
            auth_header = request.headers.get('Authorization', '')
            auth_cookie = request.cookies.get('firebase_auth_token', '')
            
            # Se não houver token, redirecionar para login com redirect
            if not auth_header and not auth_cookie:
                redirect_url = request.full_path
                return redirect(f"/login?redirect={redirect_url}")
            
            # Nota: Validação completa do token Firebase seria feita aqui
            # Por enquanto, apenas verificamos se existe um token
            # Em produção, usar firebase_admin.auth.verify_id_token()
            
            return f(*args, **kwargs)
        return decorated_function
    
    # --- Rotas do Database ---

    @app.route('/database')
    @require_auth
    def database():
        return render_template('database/index.html')

    @app.route('/database/upload', methods=['POST'])
    @require_auth
    def upload_file():
        if 'files[]' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400
        
        files = request.files.getlist('files[]')
        uploaded_count = 0
        client_ip = request.remote_addr

        # Determinar pasta de destino a partir do parâmetro 'current_path'
        # O frontend envia o currentPath (ex: 'database/files/Anderson' ou 'database_root')
        current_path_param = request.form.get('current_path', 'database_root')

        # Inicializa com a pasta padrão (database/files)
        dest_folder = UPLOAD_FOLDER

        if current_path_param and current_path_param != 'database_root':
            # Remover prefixo 'database/' para obter o caminho relativo dentro de DATABASE_DIR
            relative = current_path_param
            if relative.startswith('database/'):
                relative = relative[len('database/'):]
            
            # Montar caminho absoluto dentro de DATABASE_DIR
            proposed_dest = os.path.normpath(os.path.join(DATABASE_DIR, relative))
            
            # Segurança: garantir que o destino está dentro de DATABASE_DIR
            # Usar realpath para resolver symlinks e path traversal
            try:
                real_database = os.path.realpath(os.path.normpath(DATABASE_DIR))
                real_proposed = os.path.realpath(proposed_dest)
                
                # Verificar se o caminho proposto está dentro de DATABASE_DIR
                if real_proposed.startswith(real_database):
                    dest_folder = real_proposed
                else:
                    registrar_log(f"⚠️ Tentativa de path traversal bloqueada: {current_path_param}", log_type='database')
                    dest_folder = UPLOAD_FOLDER
            except Exception as e:
                registrar_log(f"⚠️ Erro ao validar caminho: {e}", log_type='database')
                dest_folder = UPLOAD_FOLDER

        os.makedirs(dest_folder, exist_ok=True)
        
        for file in files:
            if file.filename == '':
                continue
            filename = secure_filename(file.filename)
            filepath = os.path.join(dest_folder, filename)
            file.save(filepath)
            uploaded_count += 1
            registrar_log(f"⬆️ Upload: {client_ip} enviou {filename} -> {dest_folder}", log_type='database')
            
            # Atualização incremental da estrutura para cada arquivo enviado
            generate_structure_json(filepath)
        
        return jsonify({
            "message": f"{uploaded_count} arquivo(s) enviados com sucesso",
            "count": uploaded_count,
            "destination": dest_folder
        }), 200

    @app.route('/database/generate-structure', methods=['POST'])
    @require_auth
    def trigger_generate_structure():
        if generate_structure_json():
            return jsonify({"status": "success"})
        return jsonify({"status": "error"}), 500

    @app.route('/database/<path:filename>')
    @require_auth
    def serve_database_files(filename):
        site_database_dir = os.path.join(os.path.dirname(__file__), 'database')
        target_path = os.path.join(site_database_dir, filename)
        if os.path.exists(target_path):
            return send_from_directory(site_database_dir, filename)
        return send_from_directory(DATABASE_DIR, filename)

    # --- Rota de Download com Compressao no Servidor ---

    @app.route('/database/download-zip', methods=['POST'])
    @require_auth
    def download_zip():
        """Compacta arquivos/pastas no servidor e retorna ZIP"""
        try:
            data = request.get_json()
            paths = data.get('paths', [])
            
            if not paths:
                return jsonify({"error": "Nenhum caminho fornecido"}), 400
            
            # Criar ZIP em memoria
            zip_buffer = BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for path in paths:
                    # Sanitizar caminho para evitar path traversal
                    safe_path = os.path.normpath(path)
                    if safe_path.startswith('..'):
                        continue
                    
                    full_path = os.path.join(DATABASE_DIR, safe_path)
                    real_database = os.path.realpath(os.path.normpath(DATABASE_DIR))
                    real_path = os.path.realpath(full_path)
                    
                    # Verificar se o caminho esta dentro de DATABASE_DIR
                    if not real_path.startswith(real_database):
                        continue
                    
                    if os.path.isfile(full_path):
                        # Adicionar arquivo
                        arcname = os.path.basename(full_path)
                        zip_file.write(full_path, arcname=arcname)
                    elif os.path.isdir(full_path):
                        # Adicionar pasta recursivamente
                        for root, dirs, files in os.walk(full_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, full_path)
                                zip_file.write(file_path, arcname=os.path.join(os.path.basename(full_path), arcname))
            
            zip_buffer.seek(0)
            registrar_log(f"📦 Download ZIP gerado: {len(paths)} item(s)", log_type='database')
            
            return send_file(
                zip_buffer,
                mimetype='application/zip',
                as_attachment=True,
                download_name=f'download_{int(time.time())}.zip'
            )
        
        except Exception as e:
            registrar_log(f"❌ Erro ao gerar ZIP: {e}", log_type='database')
            return jsonify({"error": str(e)}), 500

    # --- Rotas de Manutenção e Estáticos ---

    @app.route('/maintenance/<path:filename>')
    def serve_maintenance_files(filename):
        return send_from_directory(MAINTENANCE_DIR, filename)

    # --- Tratamento de Erros ---

    @app.errorhandler(404)
    def error_404(e): 
        return send_error_file(os.path.join(MAINTENANCE_DIR, '404.html'), 404)

    @app.errorhandler(500)
    @app.errorhandler(Exception)
    def error_500(e): 
        registrar_log(f"❌ 500: {str(e)}")
        return send_error_file(os.path.join(MAINTENANCE_DIR, '500.html'), 500)

    # --- Redirecionamentos Personalizados ---
    
    @app.route('/go-calendar')
    def redirect_calendar():
        return redirect(url_for('calendar'))

    @app.route('/go-database')
    def redirect_database():
        return redirect(url_for('database'))

    @app.route('/go-site')
    def redirect_site():
        return redirect(url_for('index'))
