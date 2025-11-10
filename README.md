# ALMA_SRL_Mocks  
Questo sistema è pensato come supporto per chiunque voglia sviluppare il proprio LSB.  
Il sisteam offre diversi endpoint che simulano il comportamento di SRL, al fine di poterli usare con il proprio LSB in fase di sviluppo prima del passaggio in produzione.  
Una volta avviato il sistema, i servizi saranno esposti di default su *http://localhost:8000*.  
E' possibile eseguire il sistema in due diverse modalità:  
 * Docker container
 * Virtual environment

## Docker container 
Eseguire entrambi i container docker con:  
./run-containers.sh

Oppure se si desidera eseguire i due servizi separatamente:  
./run-containers.sh lsb_service  
./run-containers.sh srl_service  

## Virtual Environment
Il file requirements.txt contiene tutte le installazioni necessarie per il funzionamento del programma.  
Si consiglia l'uso di un virtual envoronment per poi procedere all'installazione usando:  
pip install -r requirements.txt  