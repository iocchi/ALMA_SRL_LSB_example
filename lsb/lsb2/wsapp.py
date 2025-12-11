import asyncio
import json
import requests
import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import websockets
import argparse


# Necessita delle librerie 'websockets' e 'requests': pip install websockets requests

# --- Configurazione ---
SRL_SERVICE_URL = 'http://localhost:8000' 
WEBSOCKET_PORT = 8001
HTTP_PORT = 8000

# --- Gestione API SRL (Sincrona con Requests) ---

def safe_fetch_json(url, method='GET'):
    """Esegue una richiesta HTTP sincrona al servizio SRL."""
    try:
        response = requests.request(method, f"{SRL_SERVICE_URL}{url}", timeout=5)
        if response.status_code == 200:
            return response.json()
        print(f"API Error fetching {url}: Status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {url}: {e}")
    return None

def get_vpn_ip():
    """Simulazione dell'IP VPN per l'utente corrente."""
    return "10.8.0.2"

# --- Gestione WebSocket per Aggiornamento Stato ---

async def websocket_handler(websocket):
    """Gestisce i messaggi in ingresso/uscita dal client tramite WebSocket."""
    print(f"Client connesso: {websocket.remote_address}")
    
    vpn_ip = get_vpn_ip()

    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get('action')
            
            # Requisito 1: Richiesta di aggiornamento di tutti i dati statici
            if action == 'fetch_all_data':
                print("Ricevuta richiesta di fetch_all_data.")
                context = get_all_srl_data(vpn_ip)
                # Invia tutti i dati al client in un unico payload
                await websocket.send(json.dumps({
                    'type': 'full_update',
                    'context': context
                }))

            # Requisito 2: Richiesta di azioni (Disconnect, Set Available/Unavailable)
            elif action in ['disconnect', 'set_available', 'set_unavailable']:
                await handle_user_action(websocket, action, vpn_ip)

            else:
                await websocket.send(json.dumps({'type': 'error', 'message': f'Azione non riconosciuta: {action}'}))
    
    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client disconnesso normalmente: {websocket.remote_address}")
    except Exception as e:
        print(f"Errore nella gestione WebSocket: {e}")
    finally:
        print(f"Chiusura connessione con {websocket.remote_address}")

def get_all_srl_data(vpn_ip):
    """Recupera tutti i dati statici dal servizio SRL."""
    context = {}
    
    context['user'] = safe_fetch_json(f"/api/user/by-ip/{vpn_ip}")
    context['inlab'] = safe_fetch_json("/api/service/inlab")
    context['waiting'] = safe_fetch_json("/api/service/waiting")
    context['bookings'] = safe_fetch_json("/api/service/bookings")
    
    return context

async def handle_user_action(websocket, action, vpn_ip):
    """Esegue azioni utente (disconnessione, disponibilità lab) tramite API."""
    url = ""
    method = ""

    if action == 'disconnect':
        url = f"/api/user/{vpn_ip}/disconnect"
        method = 'PUT'
    elif action == 'set_available':
        url = "/api/service/availability/true"
        method = 'PATCH'
    elif action == 'set_unavailable':
        url = "/api/service/availability/false"
        method = 'PATCH'

    if url:
        result = safe_fetch_json(url, method)
        if result is not None:
            await websocket.send(json.dumps({'type': 'action_result', 'action': action, 'status': 'success'}))
        else:
            await websocket.send(json.dumps({'type': 'action_result', 'action': action, 'status': 'error', 'message': 'API call failed.'}))
    else:
        await websocket.send(json.dumps({'type': 'action_result', 'action': action, 'status': 'error', 'message': 'Invalid action URL.'}))

# --- Server HTTP per servire index.html (per il primo caricamento) ---

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Serve il file HTML iniziale con i dati statici pre-renderizzati."""
    def do_GET(self):
        if self.path == '/' or self.path == '/index_ws.html':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            vpn_ip_sim = get_vpn_ip()
            context = get_all_srl_data(vpn_ip_sim)
            
            # Leggi il template HTML
            try:
                with open("index_ws.html", "r", encoding="utf-8") as f:
                    html_template = f.read()
            except FileNotFoundError:
                self.wfile.write("<h1>File index.html non trovato.</h1>".encode('utf-8'))
                return

            # Esegui la formattazione e la sostituzione dei placeholder in Python
            
            # Placeholder Utente
            user_info_html = "Loading user data..." 
            if context['user'] and context['user'].get('user'):
                u = context['user']['user']
                user_info_html = f"""
                    <h2 style="margin: 10px 0;">Ciao {u.get('first_name', '')} {u.get('last_name', '')}!</h2>
                    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;"> 
                        <span><strong>Email:</strong> {u.get('email', '')}</span>
                        <span><strong>Matricola:</strong> {u.get('matricola', '')}</span>
                        <span><strong>Ruolo:</strong> {u.get('role', '')}</span>
                        <span><strong>Stato:</strong> {u.get('status', '')}</span>
                        <span><strong>IP:</strong> {u.get('vpn_ip', '')}</span>
                        {'<span><strong>La connessione sarà attiva fino a:</strong> ' + u['booking_end_time'] + '</span>' if u.get('booking_end_time') else ''}
                    </div>
                """
            html_template = html_template.replace("<!-- USER_INFO_PLACEHOLDER -->", user_info_html)
            
            # Il resto dei placeholder può essere lasciato a 'Loading...' e aggiornato via WS

            self.wfile.write(html_template.encode('utf-8'))
        else:
            # Serve altri file (CSS, JS, ecc.)
            super().do_GET()


async def main():
    """Avvia entrambi i server (WebSocket e HTTP)."""
    
    # Avvio del server WebSocket
    ws_server = await websockets.serve(websocket_handler, "0.0.0.0", WEBSOCKET_PORT)
    print(f"Server WebSocket avviato su ws://0.0.0.0:{WEBSOCKET_PORT}")

    # Avvio del server HTTP in un thread
    print(f"Server HTTP avviato su http://0.0.0.0:{HTTP_PORT} per servire index.html")
    httpd = TCPServer(("", HTTP_PORT), CustomHTTPRequestHandler)
    import threading
    http_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    http_thread.start()
    
    # Mantiene il loop asyncio in esecuzione
    await ws_server.wait_closed() 



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='LSB Service')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the LSB service (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind the LSB service (default: 8000)')
    parser.add_argument('--srl-host', type=str, default='localhost', help='Host of the SRL service (default: localhost)')
    parser.add_argument('--srl-port', type=int, default=5000, help='Port of the SRL service (default: 5000)')
    parser.add_argument('--srl-browser-host', type=str, default='localhost', help='Host of the SRL service for browser requests (default: localhost)')
    args = parser.parse_args()
    
    SRL_SERVICE_URL = f"http://{args.srl_host}:{args.srl_port}"
    SRL_SERVICE_URL_BROWSER = f"http://{args.srl_browser_host}:{args.srl_port}"
    
    print(f"🚀 LSB running at http://{args.host}:{args.port}")
    print(f"🔗 Connecting to SRL service at {SRL_SERVICE_URL}")
    #print(f"🌐 Browser will connect to SRL service at {SRL_SERVICE_URL_BROWSER}")

    HTTP_PORT = args.port
    WEBSOCKET_PORT = args.port+1

    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())
    
    
    
    
