# Setup

Installare `tcpdump`

    sudo apt install tcpdump 

Se avete già Python3, installare solo la libreria `requests`

    sudo apt install python3-requests
    
oppure

    pip install requests

Se non avete Python3, installare Pyhton e la libreria `requests`

    sudo apt install python3 python3-requests


# Configurazione

Impostate i parametri del lab e i tempi di operazione all'inizio del file `tcp_monitor.py`

    lsb_ip = '10.112.0.9'   # Lab VPN IP = IP of the machine running this program
    lsb_port = 9880         # Lab VPN port = port on which the LSB is running
    wg_if = 'wg0'           # Wire>Guard interface

    check_interval = 30     # Check intervale [sec]
    timeout_disconnect = 60 # Inactivity threhold [sec]

# Esecuzione

Avviare lo script con registrazione dell'output

    python3 tcp_monitor.py > tcp_monitor.log

Per vedere il log dell'output in tempo reale

    tail -f tcp_monitor.log

Il programma usa `tcpdump` per catturare i pacchetti scambiati tra i client e il server LSB.
Ogni `check_interval` secondi viene effettuato un controllo sullo stato di attività di tutte 
le connessioni attive. Le connessioni che non sono attive per un tempo superiore a
`timeout_disconnect` secondi, saranno chiuse inviando il segnale `disconnect` al sistema 
centrale SRL.


