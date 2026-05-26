from flask import render_template, request, send_file, redirect, url_for, send_from_directory, jsonify
import os
import sys
import subprocess
from werkzeug.utils import secure_filename
from functools import wraps
import json
import time
from io import BytesIO
# Importar utilitário do sistema
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.system', 'utils')))
from zip_manager import create_zip_file

def register_routes(app, config):
    """
    Registra todas as rotas e redirecionamentos no aplicativo Flask.
    config: dicionário contendo caminhos e funções auxiliares (registrar_log, generate_structure_json, etc.)
    """
    
    BASE_DIR = config['BASE_DIR']
    DATABASE_DIR = config['DATABASE_DIR']
    MAINTENANCE_DIR = config['MAINTENANCE_DIR']
    TEMP_DIR = config['TEMP_DIR']
    ZIP_DIR = config['ZIP_DIR']
    UPLOAD_FOLDER = config['UPLOAD_FOLDER']
    registrar_log = config['registrar_log']
    generate_structure_json = config['generate_structure_json']
    send_error_file = config['send_error_file']
    redact_ip = config.get('redact_ip', lambda ip: ip)

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
                
                # Segurança: garantir que o destino está dentro de DATABASE_DIR
                # Adicionar separador para evitar bypass como /database_evil
                if real_proposed.startswith(os.path.join(real_database, '')):
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
            registrar_log(f"⬆️ Upload: {redact_ip(client_ip)} enviou {filename} -> {dest_folder}", log_type='database')
            
            # Otimização: Não chamamos generate_structure_json(filepath) aqui para múltiplos arquivos
            # Chamaremos uma vez ao final para a pasta de destino para ser mais eficiente
            pass
        
        # Atualização única para a pasta de destino (ou regeneração completa se preferir)
        # Como o script atualiza um arquivo por vez ou tudo, vamos disparar uma atualização da pasta
        generate_structure_json(dest_folder) 
        
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
        # Corrigido: Usar DATABASE_DIR definido no config
        target_path = os.path.join(DATABASE_DIR, filename)
        if os.path.exists(target_path):
            return send_from_directory(DATABASE_DIR, filename)
        
        # Fallback para pasta database local se existir (legado)
        site_database_dir = os.path.join(os.path.dirname(__file__), 'database')
        if os.path.exists(os.path.join(site_database_dir, filename)):
            return send_from_directory(site_database_dir, filename)
            
        return jsonify({"error": "Arquivo não encontrado"}), 404

    # --- Rota de Download com Compressao no Servidor ---

    @app.route('/database/download-zip', methods=['POST'])
    @require_auth
    def download_zip():
        """Compacta arquivos/pastas no servidor e retorna ZIP via streaming usando utilitário centralizado"""
        try:
            data = request.get_json()
            paths = data.get('paths', [])
            
            if not paths:
                return jsonify({"error": "Nenhum caminho fornecido"}), 400
            
            # Usar o utilitário centralizado em .system/utils
            # O arquivo ZIP agora é salvo fisicamente em .temp/.zip e mantido lá
            zip_path = create_zip_file(paths, DATABASE_DIR, ZIP_DIR)
            
            # Registrar apenas no log que o ZIP foi gerado
            client_ip = request.remote_addr
            registrar_log(f"📦 [ZIP] Servidor gerou e salvou pacote em {zip_path} para {redact_ip(client_ip)}", log_type='database')
            
            # Envia o arquivo salvo fisicamente
            return send_file(
                zip_path,
                mimetype='application/zip',
                as_attachment=True,
                download_name=os.path.basename(zip_path)
            )
        
        except Exception as e:
            registrar_log(f"❌ Erro ao processar ZIP no servidor: {e}", log_type='database')
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
