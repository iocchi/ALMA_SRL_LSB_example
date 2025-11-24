# ALMA_SRL_Mocks

Nell'ambito del progetto Digital Education Hub ALMA, è stato sviluppato il sistema Sapienza Remote Lab (SRL) che consente di definire e accedere a laboratori remoti attraverso l'implementazione di Lab Specific Bridge (LSB).

Questo repository contiene alcune informazioni e diversi esempi utili allo sviluppo di LSB.
In particolare, sono presenti uno stub che simula i servizi esposti dal sistema SRL per sviluppare e debbuggare l'interfaccia tra SRL e LSB e alcuni esempi di porzioni di codice che possono essere inserite o da cui prendere spunto per implementare l'interazione SRL - LSB. La versione finale del LSB dovrà poi collegarsi con il server di produzione (le istruzioni saranno fornite agli sviluppatori del LSB).

I servizi offerti da SRL a LSB sono esposti mediante il protocollo HTTP (metodi GET, PUT, PATCH) e restituiscono informazioni in formato JSON.


## Servizi disponibili

- **GET** `/api/user/by-ip/{vpn_ip}` : dati dell'utente connesso con VPN IP specificato
- **PUT** `/api/user/{vpn_ip}/disconnect` : segnale di chiusura della connessione dell'utente con VPN IP specificato
- **GET** `/api/service/myip` : lista delle prenotazioni del Lab
- **GET** `/api/service/inlab` : lista degli utenti attualmente nel Lab
- **GET** `/api/service/waiting` : lista degli utenti in attesa di entrare in Lab
- **GET** `/api/service/bookings` : lista delle prenotazioni del Lab
- **PATCH** `/api/service/availability/{available}` : imposta la disponibilità del Lab (true/false)

I servizi si possono provare accedendo alla pagina [`http://151.100.59.107:9890/`](http://151.100.59.107:9890/)


Esempi:

```

    http://151.100.59.107:9890/api/user/by-ip/10.0.1.100   GET
    
    {"user": 
      {
        "vpn_ip" : 10.0.1.100,
        "id": 1234567,
        "matricola" : "1111234",
        "first_name": "Mario",
        "last_name": "Rossi",
        "email" : "mrossi@test.it",
        "status" : "active",
        "role" : "student",
        "lab_id" : 1, 
        "privilege" : 1,
        "srl_access_timestamp" : "2025-05-20 15:25:38",
        "lsb_access_timestamp" : "2025-05-20 15:30:00",
        "booking_end_time" : "2025-05-20 16:00:00",
        "wait_timestamp": None,
        "created_at" : "2025-04-23 23:30:00"
        }
     "exists": "true"
    }


    http://151.100.59.107:9890/api/user/10.0.1.100/disconnect   PUT

    {
        "vpn_ip" : 10.0.1.100,
        "id": 1234567,
        "matricola" : "1111234",
        "first_name": "Mario",
        "last_name": "Rossi",
        "email" : "mrossi@test.it",
        "status" : "insrl_outlsb",
        "role" : "student",
        "lab_id" : 1, 
        "privilege" : 1,
        "srl_access_timestamp" : "2025-05-20 15:25:38",
        "lsb_access_timestamp" : "2025-05-20 15:30:00",
        "booking_end_time" : "2025-05-20 16:00:00",
        "wait_timestamp": None,
        "created_at" : "2025-04-23 23:30:00"
    }


    http://151.100.59.107:9890/api/service/myip   GET

    {
        "vpn_ip":"10.0.1.100"
    }


    http://151.100.59.107:9890/api/service/inlab   GET

    [
        {
            "id": 2345678,
            "first_name": "Alberto",
            "last_name": "Bianchi",
            "email": "abianchi@test.it",
            "matricola" : "3333456",
            "role": "student",
            "status": "insrl_inlsb",
            "srl_access_timestamp": "2025-05-20 15:30:00",
            "lsb_access_timestamp": "2025-05-20 15:35:15",
            "vpn_ip" : "192.168.0.14",
            "privilege": 2,
            "lab_id": 1,
            "wait_timestamp": None,
            "created_at": "2025-05-13 23:30:00",
            "booking_end_time": "2025-05-20 16:00:00"
        },
        {
            "id": "4",
            "first_name": "Giovanna",
            "last_name": "Verdi",
            "email": "gverdi@test.it",
            "matricola" : "4444456",
            "role": "student",
            "status": "insrl_inlsb",
            "srl_access_timestamp": "2025-05-20 16:30:00",
            "lsb_access_timestamp": "2025-05-20 16:35:15",
            "vpn_ip" : "192.168.0.15",
            "privilege": 1,
            "lab_id": 1,
            "wait_timestamp": None,
            "created_at": "2025-05-14 22:30:00",
            "booking_end_time": "2025-05-20 17:00:00"
        }
    ]


    http://151.100.59.107:9890/api/service/waiting  GET

    [
        {
            "id": 3456789,
            "first_name": "Lucia",
            "last_name": "Verdi",
            "email": "lverdi@test.it",
            "matricola" : 2345678,
            "role": "student",
            "status": "insrl_outlsb",
            "privilege": 2,
            "lab_id": 1,
            "waiting_since": "2025-05-20 15:45:25",
            "srl_access_timestamp": "2025-05-20 15:00:00",
            "lsb_access_timestamp": None,
            "vpn_ip" : "192.168.0.16",
            "wait_timestamp": None,
            "created_at": "2025-05-14 22:30:00",
            "booking_end_time": None
        },
        {
            "id": 4567890,
            "first_name": "Giovanni",
            "last_name": "Neri",
            "email": "gneri@test.it",
            "matricola" : "7777654",
            "role": "student",
            "status": "insrl_outlsb",
            "privilege": 2,
            "lab_id": 1,
            "waiting_since": "2025-05-20 15:48:30",
            "srl_access_timestamp": "2025-05-20 15:40:00",
            "lsb_access_timestamp": None,
            "vpn_ip" : "192.168.0.17",
            "wait_timestamp": None,
            "created_at": "2025-05-12 22:30:00",
            "booking_end_time": None
        }
    ]
    


    http://151.100.59.107:9890/api/service/bookings   GET

    [
        {
            "user_id" : 6789012,
            "service_id": 1,
            "num_slots": 1,
            "booked_capacity": 1,
            "token": "TOKEN_vpuq78",
            "start_time": "2025-04-20 17:30:00",
            "end_time": "2025-04-20 18:00:00",
            "id": 10,
            "status": "expired",
            "created_at": "2025-04-14 22:30:00",
        },
        {
            "user_id": 7890123,
            "service_id": 1,
            "num_slots": 1,
            "booked_capacity": 1,
            "token": "TOKEN1",
            "start_time": "2025-05-20 18:00:00",
            "end_time": None,
            "id": 1,
            "status": "confirmed",
            "created_at": "2025-05-14 22:30:00"
        }
    ]

    
    http://151.100.59.107:9890/api/service/availability/true   PATCH

    {
      "name": "Dashboard Esperimento LSB di prova",
      "creator_id": 3,
      "description_ita": "Router remoto per test",
      "description_eng": "Remote router for lab tests",
      "opening_time": "00:00:00",
      "closing_time": "23:59:00",
      "under_maintenance": "false",
      "use_bookings": "false",
      "slot_duration": 15,
      "max_capacity": 1,
      "max_num_bookable_slots": 1,
      "spectator_mode": "false",
      "spectator_mode_link": "",
      "available": true,
      "ip": "10.112.0.1",
      "port": "5000",
      "protocol": "tcp",
      "entry_point": "",
      "id": 1,
      "created_at": "2025-02-14 22:30:00"
    }

```


## Stub SRL dei servizi offerti da SRL

- **SRL Service**: API FastAPI che simula il comportamento dei servizi SRL 

## Client lato LSB per accedere ai servizi offerti da SRL

- **LSB Python**: Dashboard Flask e Socket.IO 

- **LSB HTML/JS**: Dashboard HTML/Javascript

- **LSB HTML/PHP**: Dashboard HTML/PHP

- **Linea di comando**: Accesso ai servizi tramite comandi di sistema


## Esecuzione del sistema

Tre opzioni disponibili:

### 1. Esecuzione del sistema senza installazione di app e librerie

In questa modalità è possibile accedere solo tramite *LSB HTML/JS* usando il server SRL Service disponibile all'URL `http://151.100.59.107:9890/`


Aprire il file con un browser  `file://<PATH_TO>/lsb/index.html?srl_service_host=151.100.59.107:9890`

Oppure copiare il file `lsb/index.html` in una directory servita da un server web
e accedere a tale file tramite la URL del server web aggiungendo il parametro 
`srl_service_host=151.100.59.107:9890`.



### 2. Esecuzione dei sistemi con Docker container 

È necessario installare docker engine e il plugin compose, seguendo le istruzioni in questi link:
- https://docs.docker.com/engine/
- https://docs.docker.com/install/linux/linux-postinstall/
- https://docs.docker.com/compose/install/linux/


Nota: la prima volta che si lancia il sistema, viene eseguita una sessione di creazione delle immagini docker che richiede alcuni minuti.


**Eseguire tutti i servizi (SRL + LSB Python + LSB HTML/JS + LSB PHP):**

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


Per LSB PHP, installare anche `php`

**Avvio LSB PHP:**
```bash
cd lsb
php -S 0.0.0.0:5090
```

Parametri
- `port`: Porta del server php


**Esempio con parametri personalizzati:**
```bash
# SRL su porta 9000
python srl_service/main.py --host 0.0.0.0 --port 9000

# LSB Python su porta 6000 che si connette a SRL su porta 9000
python lsb/main.py --host 0.0.0.0 --port 6000 --srl-host localhost --srl-port 9000
```






## Accesso diretto ai servizi

Nota: gli esempi che seguono usano l'accesso al server SRL locale tramite `localhost:8000`. Per accedere ai servizi remoti, usare invece `151.100.59.107:9890`.

**SRL API** 

Usare la URL `http://localhost:8000/<service_name>`

Esempi da linea di comando:

```bash
curl http://localhost:8000/api/user/by-ip/10.0.1.100
curl -X PUT http://localhost:8000/api/user/10.0.1.100/disconnect
curl http://localhost:8000/api/service/myip
curl http://localhost:8000/api/service/inlab
curl http://localhost:8000/api/service/waiting
curl http://localhost:8000/api/service/bookings
curl -X PATCH http://localhost:8000/api/service/availability/true
```


## Accesso ai servizi tramite LSB Python, HTML/JS o HTML/PHP

Usare un browser per accedere a questi URL

- **LSB Python Dashboard**: `http://localhost:5000`

- **LSB HTML/JS Dashboard**: `http://localhost:5080/index.html`

- **LSB PHP Dashboard**: `http://localhost:5090/index.php`

I file `lsb/main.py`, `lsb/index.html`, `lsb/index.php` contengono degli esempi di accesso al server dei servizi SRL usando rispettivamente Python e Javascript.



## Customizzazione di IP e porte per l'ambiente docker

Usando l'ambiente docker, lo script `./run-containers.sh` usa i valori di default per indirizzi e porte di connessione. Tuttavia, è possibile specificare  indirizzi e porte personalizzati usando le seguenti variabili d'ambiente:

#### Parametri disponibili:

| Parametro | Descrizione | Default | Esempio |
|-----------|-------------|---------|---------|
| `SRL_PORT` | Porta esterna per accedere al servizio SRL | `8000` | `SRL_PORT=9000` |
| `LSB_PORT` | Porta esterna per accedere al servizio LSB Python | `5000` | `LSB_PORT=6000` |
| `LSB_HTTP_PORT` | Porta esterna per accedere al servizio LSB HTML/JS | `5080` | `LSB_HTTP_PORT=9080` |
| `LSB_PHP_PORT` | Porta esterna per accedere al servizio LSB PHP | `5090` | `LSB_PHP_PORT=9090` |
| `SRL_CONNECT_HOST` | Host a cui LSB si connette per raggiungere SRL | `srl_service` | `SRL_CONNECT_HOST=151.100.59.107` |
| `SRL_CONNECT_PORT` | Porta a cui LSB si connette per raggiungere SRL | `8000` | `SRL_CONNECT_PORT=9000` |

#### Esempi d'uso:

**1. Configurazione di default (tutti i servizi):**
```bash
docker-compose up
```
- SRL disponibile su: `http://localhost:8000`
- LSB Python disponibile su: `http://localhost:5000`
- LSB HTML/JS disponibile su: `http://localhost:5080/index.html`
- LSB PHO disponibile su: `http://localhost:5090/index.php`
- LSB si connette a SRL tramite rete Docker interna

**2. Porte personalizzate:**
```bash
SRL_PORT=9000 LSB_PORT=6000 LSB_HTTP_PORT=9090 docker-compose up
```
- SRL disponibile su: `http://localhost:9000`
- LSB Python disponibile su: `http://localhost:6000`
- LSB HTML/JS disponibile su: `http://localhost:9090/index.html`

**3. Solo servizio SRL con porta personalizzata:**
```bash
SRL_PORT=9000 ./run-containers.sh srl_service
```
- SRL disponibile su: `http://localhost:9000`

**4. Solo servizio LSB che si connette a SRL esterno:**
```bash
LSB_PORT=6000 SRL_CONNECT_HOST=151.100.59.107 SRL_CONNECT_PORT=9890 ./run-containers.sh lsb_service
```
- LSB Python disponibile su: `http://localhost:6000`
- LSB si connette a SRL su `151.100.59.107:9890`

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

