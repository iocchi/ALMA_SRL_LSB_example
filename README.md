# ALMA_SRL_Mocks  
Questo sistema è pensato come supporto per chiunque voglia sviluppare il proprio LSB.  
Il sistema offre diversi endpoint che simulano il comportamento di SRL, al fine di poterli usare con il proprio LSB in fase di sviluppo prima del passaggio in produzione.  

## Servizi disponibili
- **SRL Service**: API FastAPI che simula il comportamento di SRL (default: `http://localhost:8000`)
- **LSB Service (Python)**: Dashboard real-time con Flask e Socket.IO (default: `http://localhost:5000`)
- **LSB Static**: Dashboard HTML statica self-contained (default: `http://localhost:8080/static_index.html`)

È possibile eseguire il sistema in due diverse modalità:  
 * Docker container
 * Virtual environment

## Docker container 

### Esecuzione rapida

**Eseguire tutti i servizi (SRL + LSB Python + LSB Static):**
```bash
docker-compose up
```

**Eseguire solo SRL e LSB Static (versione HTML self-contained):**
```bash
docker-compose up srl_service lsb_static
```

**Oppure usando lo script:**
```bash
./run-containers.sh
```

**Eseguire servizi separatamente:**
```bash
./run-containers.sh lsb_service  
./run-containers.sh srl_service
./run-containers.sh lsb_static
```

### Accesso ai servizi
- **SRL API**: http://localhost:8000
- **LSB Python Dashboard**: http://localhost:5000
- **LSB Static Dashboard**: http://localhost:8080/static_index.html  

### Customizzazione di IP e porta
Se si esegue `./run-containers.sh` senza specificare parametri, verranno usati i valori di default. Tuttavia, è possibile specificare porte e indirizzi personalizzati usando le seguenti variabili d'ambiente:

#### Parametri disponibili:

| Parametro | Descrizione | Default | Esempio |
|-----------|-------------|---------|---------|
| `SRL_PORT` | Porta esterna per accedere al servizio SRL | `8000` | `SRL_PORT=9000` |
| `LSB_PORT` | Porta esterna per accedere al servizio LSB Python | `5000` | `LSB_PORT=6000` |
| `LSB_STATIC_PORT` | Porta esterna per accedere al servizio LSB Static | `8080` | `LSB_STATIC_PORT=9090` |
| `SRL_CONNECT_HOST` | Host a cui LSB si connette per raggiungere SRL | `srl_service` | `SRL_CONNECT_HOST=192.168.1.100` |
| `SRL_CONNECT_PORT` | Porta a cui LSB si connette per raggiungere SRL | `8000` | `SRL_CONNECT_PORT=9000` |

#### Esempi d'uso:

**1. Configurazione di default (tutti i servizi):**
```bash
docker-compose up
```
- SRL disponibile su: `http://localhost:8000`
- LSB Python disponibile su: `http://localhost:5000`
- LSB Static disponibile su: `http://localhost:8080/static_index.html`
- LSB si connette a SRL tramite rete Docker interna

**2. Porte personalizzate:**
```bash
SRL_PORT=9000 LSB_PORT=6000 LSB_STATIC_PORT=9090 docker-compose up
```
- SRL disponibile su: `http://localhost:9000`
- LSB Python disponibile su: `http://localhost:6000`
- LSB Static disponibile su: `http://localhost:9090/static_index.html`

**3. Solo servizio SRL con porta personalizzata:**
```bash
SRL_PORT=9000 ./run-containers.sh srl_service
```
- SRL disponibile su: `http://localhost:9000`

**4. Solo servizio LSB che si connette a SRL esterno:**
```bash
LSB_PORT=6000 SRL_CONNECT_HOST=192.168.1.100 SRL_CONNECT_PORT=8000 ./run-containers.sh lsb_service
```
- LSB disponibile su: `http://localhost:6000`
- LSB si connette a SRL su `192.168.1.100:8000`

**5. LSB si connette a SRL sulla macchina host:**
```bash
SRL_CONNECT_HOST=host.docker.internal ./run-containers.sh lsb_service
```
Utile quando SRL gira fuori da Docker sulla macchina host.

## Virtual Environment
Il file requirements.txt contiene tutte le installazioni necessarie per il funzionamento del programma.  
Si consiglia l'uso di un virtual environment per poi procedere all'installazione usando:  
```bash
pip install -r requirements.txt
```

### Esecuzione servizi con Virtual Environment

**Servizio SRL:**
```bash
cd srl_service
python main.py --host 0.0.0.0 --port 8000
```

**Servizio LSB:**
```bash
cd lsb
python main.py --host 0.0.0.0 --port 5000 --srl-host localhost --srl-port 8000
```

#### Parametri da linea di comando:

**SRL Service:**
- `--host`: Host su cui esporre il servizio (default: `0.0.0.0`)
- `--port`: Porta su cui esporre il servizio (default: `8000`)

**LSB Service (Python):**
- `--host`: Host su cui esporre il servizio LSB (default: `0.0.0.0`)
- `--port`: Porta su cui esporre il servizio LSB (default: `5000`)
- `--srl-host`: Host del servizio SRL a cui connettersi (default: `localhost`)
- `--srl-port`: Porta del servizio SRL a cui connettersi (default: `8000`)
- `--srl-browser-host`: Host del servizio SRL per le richieste browser (default: `localhost`)

**LSB Static (HTML):**
Per servire la versione statica, usare un semplice HTTP server:
```bash
cd lsb
python -m http.server 8080
```
Poi aprire: `http://localhost:8080/static_index.html`

**Esempio con parametri personalizzati:**
```bash
# SRL su porta 9000
python srl_service/main.py --host 0.0.0.0 --port 9000

# LSB Python su porta 6000 che si connette a SRL su porta 9000
python lsb/main.py --host 0.0.0.0 --port 6000 --srl-host localhost --srl-port 9000
```

## Differenze tra LSB Python e LSB Static

| Caratteristica | LSB Python (`main.py`) | LSB Static (`static_index.html`) |
|----------------|------------------------|----------------------------------|
| **Tecnologia** | Flask + Socket.IO | HTML + JavaScript puro |
| **Dipendenze** | Richiede Python e librerie | Solo browser web |
| **Dati real-time** | Socket.IO server-side | Simulazione client-side |
| **Esecuzione** | Richiede server Python | Qualsiasi HTTP server |
| **Porta default** | 5000 | 8080 |
| **Use case** | Sviluppo con dati real-time | Deploy rapido, testing, demo |

**LSB Static** è completamente self-contained e può essere aperto direttamente nel browser. Tenta di connettersi a un Socket.IO server su `localhost:5000` se disponibile, altrimenti simula i dati client-side.