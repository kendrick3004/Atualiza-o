from flask import Flask, send_file, request, jsonify
import sys
import datetime
import os
import time
import subprocess
from collections import defaultdict
try:
    from dotenv import load_dotenv
    # Carregar variaveis de ambiente do arquivo .env
    load_dotenv()
except ImportError:
    # Fallback caso python-dotenv nao esteja instalado
    print("⚠️ Aviso: python-dotenv nao encontrado. Usando variaveis de ambiente do sistema.")

# Importar o registrador de rotas
from routes import register_routes

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload

# Configurações de Rate Limiting
RATE_LIMIT_COUNT = 30
RATE_LIMIT_PERIOD = 10
request_counts = defaultdict(lambda: {'count': 0, 'timestamp': 0})

visitas_total = 0
visitas_hoje = 0
data_atual = datetime.date.today()

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_BASE_DIR = os.path.join(BASE_DIR, 'logs')
MAINTENANCE_DIR = os.path.join(BASE_DIR, 'maintenance')
TEMP_DIR = os.path.join(BASE_DIR, '.temp')
ZIP_DIR = os.path.join(TEMP_DIR, '.zip')
REPO_DIR = os.path.join(TEMP_DIR, '.repo')
DATABASE_DIR = os.path.abspath(os.path.join(BASE_DIR, 'database'))
UPLOAD_FOLDER = os.path.join(DATABASE_DIR, 'files')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def redact_ip(ip):
    """Pseudonimiza o endereço IP para privacidade"""
    if not ip: return "0.0.0.0"
    parts = ip.split('.')
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.xxx.xxx"
    return "xxx.xxx.xxx.xxx"

# Sobrescrever log_message do Werkzeug para mascarar IPs nos logs de servidor
try:
    from werkzeug.serving import WSGIRequestHandler
    def new_log_message(self, format, *args):
        ip = self.address_string()
        redacted = redact_ip(ip)
        self.log("info", f"{redacted} - - %s", format % args)
    WSGIRequestHandler.log_message = new_log_message
except Exception as e:
    print(f"⚠️ Aviso: Não foi possível aplicar máscara de IP nos logs do Werkzeug: {e}")

def get_log_file(log_type='site'):
    hoje_str = datetime.date.today().strftime('%Y-%m-%d')
    dia_dir = os.path.join(LOG_BASE_DIR, hoje_str)
    os.makedirs(dia_dir, exist_ok=True)
    if log_type == 'database':
        return os.path.join(dia_dir, 'database_access.log')
    return os.path.join(dia_dir, 'site_access.log')

def registrar_log(mensagem, log_type='site'):
    """
    Registers a log message in the daily log file.
    """
    try:
        with open(get_log_file(log_type), 'a', encoding='utf-8') as f:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            f.write(f"[{timestamp}] {mensagem}\n")
    except Exception as e:
        print(f"Erro ao salvar log: {e}")

def atualizar_linha():
    """
    Updates the console output and logs the current visit statistics.
    """
    log_msg = f"📊 Visitas Total: {visitas_total} | Hoje: {visitas_hoje}"
    sys.stdout.write(f"\r{log_msg}")
    sys.stdout.flush()
    registrar_log(log_msg)

def generate_structure_json(specific_file=None):
    """
    Executes the external script to generate or update the database structure JSON.
    """
    try:
        script_path = os.path.join(DATABASE_DIR, 'generate_assets_structure.py')
        cmd = [sys.executable, script_path]
        if specific_file:
            cmd.append(specific_file)
        subprocess.run(cmd, check=True)
        msg = f"✅ Estrutura JSON {'atualizada' if specific_file else 'gerada'} com sucesso."
        registrar_log(msg, log_type='database')
        return True
    except Exception as e:
        registrar_log(f"❌ Erro ao atualizar estrutura JSON: {e}", log_type='database')
        return False

def send_error_file(path, code):
    try:
        return send_file(path), code
    except:
        return f"Erro {code}", code

@app.before_request
def security_and_tracking():
    global visitas_total, visitas_hoje, data_atual
    
    if request.path.endswith(('favicon.ico', 'favicon.png')):
        return '', 204
    
    extensoes_ignoradas = (
        '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', 
        '.woff', '.woff2', '.ttf', '.otf', '.json', '.map', '.ico', '.webp'
    )
    pastas_ignoradas = ('/assets/', '/css/', '/js/', '/img/', '/src/', '/maintenance/')
    
    # Verifica se termina com extensão ignorada ou se o caminho começa com uma das pastas ignoradas
    if request.path.endswith(extensoes_ignoradas) or any(request.path.startswith(p) for p in pastas_ignoradas):
        return

    # Filtrar requisições de API que não representam visitas reais
    api_paths_to_ignore = ('/api/config', '/api/health', '/api/status')
    if request.path in api_paths_to_ignore:
        return

    client_ip = request.remote_addr
    redacted_ip = redact_ip(client_ip)
    
    current_time = time.time()
    if current_time - request_counts[client_ip]['timestamp'] > RATE_LIMIT_PERIOD:
        request_counts[client_ip] = {'count': 1, 'timestamp': current_time}
    else:
        request_counts[client_ip]['count'] += 1
    
    if request_counts[client_ip]['count'] > RATE_LIMIT_COUNT:
        return send_error_file(os.path.join(MAINTENANCE_DIR, '429.html'), 429)
    
    hoje = datetime.date.today()
    if hoje != data_atual:
        visitas_hoje = 0
        data_atual = hoje
    
    visitas_total += 1
    visitas_hoje += 1
    
    try:
        if request.path.startswith('/database'):
            registrar_log(f"👤 Acesso Database: {redacted_ip} -> {request.path}", log_type='database')
            registrar_log(f"📊 Visitas Total: {visitas_total} | Hoje: {visitas_hoje}", log_type='database')
        else:
            registrar_log(f"👤 Acesso: {redacted_ip} -> {request.path}")
            atualizar_linha()
    except Exception as e:
        print(f"Erro ao processar logs de acesso: {e}")

# --- ROTA DE CONFIGURACAO DO FRONTEND (Carrega chaves do .env) ---
@app.route('/api/config', methods=['GET'])
def get_frontend_config():
    """
    Endpoint que fornece as variaveis de ambiente necessarias para o frontend.
    """
    config_data = {
        'FIREBASE_API_KEY': os.getenv('FIREBASE_API_KEY', ''),
        'FIREBASE_AUTH_DOMAIN': os.getenv('FIREBASE_AUTH_DOMAIN', ''),
        'FIREBASE_PROJECT_ID': os.getenv('FIREBASE_PROJECT_ID', ''),
        'FIREBASE_STORAGE_BUCKET': os.getenv('FIREBASE_STORAGE_BUCKET', ''),
        'FIREBASE_MESSAGING_SENDER_ID': os.getenv('FIREBASE_MESSAGING_SENDER_ID', ''),
        'FIREBASE_APP_ID': os.getenv('FIREBASE_APP_ID', ''),
        'FIREBASE_MEASUREMENT_ID': os.getenv('FIREBASE_MEASUREMENT_ID', ''),
        'FIREBASE_DATABASE_URL': os.getenv('FIREBASE_DATABASE_URL', ''),
        'WEATHER_API_KEY': os.getenv('WEATHER_API_KEY', '')
    }
    # Log reduzido: evitar poluir logs com chamadas frequentes do frontend
    # Registra apenas a cada 100 chamadas para diagnóstico
    if not hasattr(get_frontend_config, '_call_count'):
        get_frontend_config._call_count = 0
    get_frontend_config._call_count += 1
    if get_frontend_config._call_count == 1 or get_frontend_config._call_count % 100 == 0:
        registrar_log(f"📋 Configuracao do frontend solicitada por {redact_ip(request.remote_addr)} (chamada #{get_frontend_config._call_count})")
    return jsonify(config_data), 200

# Configuracao para passar para o routes.py
config = {
    'BASE_DIR': BASE_DIR,
    'DATABASE_DIR': DATABASE_DIR,
    'MAINTENANCE_DIR': MAINTENANCE_DIR,
    'TEMP_DIR': TEMP_DIR,
    'ZIP_DIR': ZIP_DIR,
    'REPO_DIR': REPO_DIR,
    'UPLOAD_FOLDER': UPLOAD_FOLDER,
    'registrar_log': registrar_log,
    'generate_structure_json': generate_structure_json,
    'send_error_file': send_error_file,
    'redact_ip': redact_ip
}

# Registrar as rotas a partir do arquivo separado
register_routes(app, config)

if __name__ == '__main__':
    print("\n🚀 Servidor ONLINE na porta 5000")
    # Rodar com debug=False por padrão, conforme relatório
    app.run(host="0.0.0.0", port=5000, debug=False)
