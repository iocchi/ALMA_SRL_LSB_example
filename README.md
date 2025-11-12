# ALMA_SRL_Mocks

Nell'ambito del progetto Digital Education Hub ALMA, è stato sviluppato il sistema Sapienza Remote Lab (SRL) che consente di definire e accedere a laboratori remoti attraverso l'implementazione di Lab Specific Bridge (LSB).

Questo repository contiene alcune informazioni e diversi esempi utili allo sviluppo di LSB.
In particolare, sono presenti uno stub che simula i servizi esposti dal sistema SRL per sviluppare e debbuggare l'interfaccia tra SRL e LSB
e alcuni esempi di porzioni di codice che possono essere inserite o da cui prendere spunto per implementare l'interazione SRL - LSB.


## Stub SRL dei servizi offerti da SRL

- **SRL Service**: API FastAPI che simula il comportamento dei servizi SRL 

## Client lato LSB per accedere ai servizi offerti da SRL

- **LSB Python**: Dashboard real-time con Flask e Socket.IO 

- **LSB HTML/JS**: Dashboard HTML/Javascript self-contained

- **Linea di comando**: Accesso ai servizi tramite comandi di sistema


## Esecuzione del sistema

Tre opzioni disponibili:

### 1. Esecuzione del sistema senza installazione di app e librerie

In questa mnodalità è possibile accedere solo tramite *LSB HTML/JS* usando il server SRL Service disponibile all'URL `http://151.100.59.107:8000/`


Aprire il file con un browser  `file://<PATH_TO>/lsb/lsb1.html`

Oppure copiare il file `lsb/lsb1.html` in una directory servita da un server web
e accedere a tale file tramite la URL sel server web.



### 2. Esecuzione dei sistemi con Docker container 

È necessario installare docker engine e il plugin compose, seguendo le istruzioni in questi link:
- https://docs.docker.com/engine/
- https://docs.docker.com/install/linux/linux-postinstall/
- https://docs.docker.com/compose/install/linux/


Nota: la prima volta che si lancia il sistema, viene eseguita una sessione di creazione delle immagini docker che richiede alcuni minuti.


**Eseguire tutti i servizi (SRL + LSB Python + LSB HTML/JS):**

```bash
./run-containers.sh
```

oppure

```bash
docker compose up
```

**Eseguire solo SRL e LSB HTML/JS (versione HTML self-contained):**
```bash
./run-containers.sh srl_service lsb_html
```

oppure

```bash
docker compose up srl_service lsb_html
```




### 3. Esecuzione dei sistemi con Virtual Environment

Installare le librerie Python usando i file `srl_service/requirements.txt` e `lsb/requirements.txt`

I file `requirements.txt` contengono tutte le installazioni necessarie per il funzionamento dei programmi.
Si consiglia l'uso di un virtual environment per poi procedere all'installazione usando:
```bash
pip install -r srl_service/requirements.txt
pip install -r lsb/requirements.txt
```


**Avvio Server servizi SRL:**
```bash
cd srl_service
python main.py --host 0.0.0.0 --port 8000
```

Parametri
- `--host`: Host su cui esporre il servizio (default: `0.0.0.0`)
- `--port`: Porta su cui esporre il servizio (default: `8000`)


**Avvio LSB Python:**
```bash
cd lsb
python main.py --host 0.0.0.0 --port 5000 --srl-host localhost --srl-port 8000
```

Parametri
- `--host`: Host su cui esporre il servizio LSB (default: `0.0.0.0`)
- `--port`: Porta su cui esporre il servizio LSB (default: `5000`)
- `--srl-host`: Host del servizio SRL a cui connettersi (default: `localhost`)
- `--srl-port`: Porta del servizio SRL a cui connettersi (default: `8000`)
- `--srl-browser-host`: Host del servizio SRL per le richieste browser (default: `localhost`)


**Avvio LSB HTML/JS:**
```bash
cd lsb
python -m http.server 5080
```
Parametri
- `port`: Porta del server http


**Esempio con parametri personalizzati:**
```bash
# SRL su porta 9000
python srl_service/main.py --host 0.0.0.0 --port 9000

# LSB Python su porta 6000 che si connette a SRL su porta 9000
python lsb/main.py --host 0.0.0.0 --port 6000 --srl-host localhost --srl-port 9000
```



## Servizi disponibili

- `/user_data?vpn_ip=....`
- `/inlab_users`
- `/close_connection`
- `/waiting_users`
- `/bookings`



## Accesso diretto ai servizi

Nota: gli esempi che seguono usano l'accesso al server SRL locale tramite `localhost`. Per accedere ai servizi remoti, usare invece l'IP `151.100.59.107`.

**SRL API** 

Usare la URL `http://localhost:8000/<service_name>` (example:  `http://localhost:8000/inlab_users`)

Esempio da linea di comando:
```bash
curl http://localhost:8000/inlab_users
curl http://localhost:8000/user_data?vpn_ip=192.168.1.100
```


## Accesso ai servizi tramite LSB Python o LSB HTML/JS

Usare un browser per accedere a questi URL

- **LSB Python Dashboard**: `http://localhost:5000`

- **LSB HTML/JS Dashboard**: `http://localhost:5080/index.html`

I file `lsb/main.py` e `lsb/index.html` contengono degli esempi di accesso al server dei servizi SRL usando rispettivamente Python e Javascript.



## Customizzazione di IP e porte per l'ambiente docker

Usando l'ambiente docker, lo script `./run-containers.sh` usa i valori di default per indirizzi e porte di connessione. Tuttavia, è possibile specificare  indirizzi e porte personalizzati usando le seguenti variabili d'ambiente:

#### Parametri disponibili:

| Parametro | Descrizione | Default | Esempio |
|-----------|-------------|---------|---------|
| `SRL_PORT` | Porta esterna per accedere al servizio SRL | `8000` | `SRL_PORT=9000` |
| `LSB_PORT` | Porta esterna per accedere al servizio LSB Python | `5000` | `LSB_PORT=6000` |
| `LSB_STATIC_PORT` | Porta esterna per accedere al servizio LSB Static | `8080` | `LSB_STATIC_PORT=9090` |
| `SRL_CONNECT_HOST` | Host a cui LSB si connette per raggiungere SRL | `srl_service` | `SRL_CONNECT_HOST=151.100.59.107` |
| `SRL_CONNECT_PORT` | Porta a cui LSB si connette per raggiungere SRL | `8000` | `SRL_CONNECT_PORT=9000` |

#### Esempi d'uso:

**1. Configurazione di default (tutti i servizi):**
```bash
docker-compose up
```
- SRL disponibile su: `http://localhost:8000`
- LSB Python disponibile su: `http://localhost:5000`
- LSB Static disponibile su: `http://localhost:8080/index.html`
- LSB si connette a SRL tramite rete Docker interna

**2. Porte personalizzate:**
```bash
SRL_PORT=9000 LSB_PORT=6000 LSB_STATIC_PORT=9090 docker-compose up
```
- SRL disponibile su: `http://localhost:9000`
- LSB Python disponibile su: `http://localhost:6000`
- LSB Static disponibile su: `http://localhost:9090/index.html`

**3. Solo servizio SRL con porta personalizzata:**
```bash
SRL_PORT=9000 ./run-containers.sh srl_service
```
- SRL disponibile su: `http://localhost:9000`

**4. Solo servizio LSB che si connette a SRL esterno:**
```bash
LSB_PORT=6000 SRL_CONNECT_HOST=151.100.59.107 SRL_CONNECT_PORT=8000 ./run-containers.sh lsb_service
```
- LSB disponibile su: `http://localhost:6000`
- LSB si connette a SRL su `151.100.59.107:8000`

**5. LSB si connette a SRL sulla macchina host:**
```bash
SRL_CONNECT_HOST=host.docker.internal ./run-containers.sh lsb_service
```
Utile quando SRL gira fuori da Docker sulla macchina host.





## Differenze tra LSB Python e LSB HTML/JS

| Caratteristica | LSB Python (`main.py`) | LSB Static (`static_index.html`) |
|----------------|------------------------|----------------------------------|
| **Tecnologia** | Flask + Socket.IO | HTML + JavaScript |
| **Dipendenze** | Richiede Python e librerie | Solo browser web |
| **Dati real-time** | Socket.IO server-side | Simulazione client-side |
| **Esecuzione** | Richiede server Python | Qualsiasi HTTP server |
| **Use case** | Sviluppo con dati real-time | Deploy rapido, testing, demo |

**LSB HTML/JS** è completamente self-contained e può essere aperto direttamente nel browser. Tenta di connettersi a un Socket.IO server su `localhost:5000` se disponibile, altrimenti simula i dati client-side.

