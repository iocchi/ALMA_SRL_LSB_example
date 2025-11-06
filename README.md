# ALMA_SRL_Mocks  
Questo sistema è pensato come supporto per chiunque voglia sviluppare il proprio LSB.  
Il sisteam offre diversi endpoint che simulano il comportamento di SRL, al fine di poterli usare con il proprio LSB in fase di sviluppo prima del passaggio in produzione.  
Una volta avviato il sistema, i servizi saranno esposti su *http://localhost:8001*.  
E' possibile eseguire il sistema in due diverse modalità:  
 * Docker container
 * Virtual environment

## Docker container 
Eseguire i container docker con:  
./run-containers.sh
## Requirements
Il file requirements.txt contiene tutte le installazioni necessarie per il funzionamento del programma.  
Si consiglia l'uso di un virtual envoronment per poi procedere all'installazione usando:  
pip install -r requirements.txt  