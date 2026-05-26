from flask import Flask, send_from_directory, request, send_file
import os
import time
import datetime
from collections import defaultdict

# Carregar variaveis de ambiente do arquivo .env
try:
    from dotenv import load_dotenv
    # Procura o .env na raiz do projeto (um nível acima de maintenance/)
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()  # Tenta carregar do diretório atual
except ImportError:
    # Fallback caso python-dotenv nao esteja instalado
    print("⚠️ Aviso: python-dotenv nao encontrado. Usando variaveis de ambiente do sistema.")

# Garantir caminhos absolutos para o diretório do script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=SCRIPT_DIR, static_url_path='')

# Configurações de Rate Limiting
RATE_LIMIT_COUNT = 10
RATE_LIMIT_PERIOD = 10
request_counts = defaultdict(lambda: {'count': 0, 'timestamp': 0})

# Caminho para a pasta de logs na raiz do projeto (index/logs)
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
LOG_BASE_DIR = os.path.join(PROJECT_DIR, 'logs')

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

def registrar_log(mensagem):
    """Salva a mensagem no arquivo de log do dia na pasta de manutenção."""
    try:
        hoje_str = datetime.date.today().strftime('%Y-%m-%d')
        dia_dir = os.path.join(LOG_BASE_DIR, hoje_str)
        os.makedirs(dia_dir, exist_ok=True)
        
        log_file = os.path.join(dia_dir, 'maintenance.log')
        with open(log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            f.write(f"[{timestamp}] {mensagem}\n")
    except Exception as e:
        print(f"Erro ao salvar log de manutenção: {e}")

@app.before_request
def maintenance_logic():
    # Lógica de Favicon
    if request.path.endswith(('favicon.ico', 'favicon.png')):
        favicon_path = os.path.join(SCRIPT_DIR, 'favicon.png')
        if os.path.exists(favicon_path):
            return send_file(favicon_path)
        # Se não existir, tenta o favicon.ico se for o pedido
        favicon_ico = os.path.join(SCRIPT_DIR, 'favicon.ico')
        if request.path.endswith('favicon.ico') and os.path.exists(favicon_ico):
            return send_file(favicon_ico)
        return '', 204

    # Ignora arquivos estáticos (CSS, JS, Imagens)
    extensoes_estaticas = ('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.woff', '.woff2', '.ttf', '.otf')
    if request.path.endswith(extensoes_estaticas):
        return

    # Proteção contra ataques
    client_ip = request.remote_addr
    redacted_ip = redact_ip(client_ip)
    current_time = time.time()
    if current_time - request_counts[client_ip]['timestamp'] > RATE_LIMIT_PERIOD:
        request_counts[client_ip] = {'count': 1, 'timestamp': current_time}
    else:
        request_counts[client_ip]['count'] += 1

    if request_counts[client_ip]['count'] > RATE_LIMIT_COUNT:
        registrar_log(f"⚠️ BLOQUEIO (Manutenção): IP {redacted_ip}")
        return send_from_directory(SCRIPT_DIR, '429.html'), 429
    
    registrar_log(f"🚧 Acesso em Manutenção: {redacted_ip} -> {request.path}")

@app.route('/')
def index():
    return send_from_directory(SCRIPT_DIR, '503.html')

# Rota para servir arquivos estáticos da própria pasta de manutenção
# Isso resolve o problema de carregar /maintenance/error-pages.css
@app.route('/maintenance/<path:filename>')
def serve_maintenance_files(filename):
    return send_from_directory(SCRIPT_DIR, filename)

# Mantém as rotas de API ativas (simulando ou redirecionando)
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_proxy(path):
    return {"status": "success", "message": "API está funcionando normalmente durante a manutenção", "path": path}, 200

@app.route('/<path:path>')
def static_files(path):
    # Se o arquivo existir na pasta de manutenção, serve ele
    file_path = os.path.join(SCRIPT_DIR, path)
    if os.path.exists(file_path):
        return send_from_directory(SCRIPT_DIR, path)
    # Caso contrário, mostra a página de manutenção
    return send_from_directory(SCRIPT_DIR, '503.html')

@app.errorhandler(404)
@app.errorhandler(500)
def handle_maintenance_errors(e):
    return send_from_directory(SCRIPT_DIR, '503.html')

if __name__ == '__main__':
    print("🚧 Modo Manutenção ATIVO na porta 5000")
    registrar_log("--- Modo Manutenção Iniciado ---")
    app.run(host="0.0.0.0", port=5000, debug=False)
