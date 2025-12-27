# Setup

Install `tcpdump`

    sudo apt install tcpdump 

If you have Python3 already installed

Install python libs

    sudo apt install python3-requests
    
or

    pip install requests

If you do not have Python3 installed

    sudo apt install python3 python3-requests


# Configure

Set your configuration in the Python script

    lsb_ip = '10.112.0.9'   # Lab VPN IP = IP of the machine running this program
    lsb_port = 9880         # Lab VPN port = port on which the LSB is running
    wg_if = 'wg0'           # Wire>Guard interface

    check_interval = 30     # Check intervale [sec]
    timeout_disconnect = 60 # Inactivity threhold [sec]

# Run

Run the script logging the output

    python3 tcp_monitor.py > tcp_monitor.log

This script will check every `check_interval` seconds the status of all the connecrions
to the lab. If any connection is inactive for more than `timeout_disconnect`  seconds,
it will send a `disconnect` mesasage to the SRL for this client.


