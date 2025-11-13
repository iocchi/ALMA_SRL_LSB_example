# file: main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import argparse
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Servizi SRL prova</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background: #f8f9fa; }
        h1 { text-align: center; }
    </style>
</head>
<body>
    <h1>Servizi SRL di prova</h1>
    
    <p> <span style="color: #0807a5;font-size: 1.2em;">  <a href="#" id="alink1"> <code>/user_data?vpn_ip=....</code> </a> </span>: dati dell'utente connesso con VPN IP specificato </p>
    <p> <span style="color: #0807a5;font-size: 1.2em;">  <a href="#" id="alink2"> <code>/close_connection?vpn_ip=...</code> </a> </span>: segnale di chiusura della connessione dell'utente con VPN IP specificato </p>
    <p> <span style="color: #0807a5;font-size: 1.2em;"> <a href="#" id="alink3"> <code>/inlab_users</code> </a> </span>: lista degli utenti attualmente nel Lab </p>
    <p> <span style="color: #0807a5;font-size: 1.2em;"> <a href="#" id="alink4"> <code>/waiting_users</code> </a> </span>: lista degli utenti in attesa di entrare in Lab </p>
    <p> <span style="color: #0807a5;font-size: 1.2em;"> <a href="#" id="alink5"> <code>/bookings</code> </a> </span>: lista delle prenotazioni del Lab </p>

<script>

const host = window.location.host; 
    
document.getElementById('alink1').href=`//${host}/user_data?vpn_ip=10.0.1.100`;
document.getElementById('alink2').href=`//${host}/close_connection?vpn_ip=10.0.1.100`;
document.getElementById('alink3').href=`//${host}/inlab_users`;
document.getElementById('alink4').href=`//${host}/waiting_users`;
document.getElementById('alink5').href=`//${host}/bookings`;
    
</script>

</body>
</html>
"""

@app.get("/")
async def index():
    return HTMLResponse(content=HTML_PAGE)


@app.get("/user/by-ip/{vpn_ip}")
async def get_user(vpn_ip: str, request: Request):
    """
    Retrieve user data.

    - **vpn_ip**: The VPN IP to identify the user
    """

    client_ip = request.client.host
    print(f"Connection from {client_ip}")
    
    try:
        user = {
            "vpn_ip" : vpn_ip,
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
        return {"user": user,"exists": "true"}
    except ValueError as ve:
        # Handle known validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.put("/user/{vpn_ip}/disconnect")
async def disconnect(vpn_ip: str):
    """
    Notifies SRL that the connection with the LSB has being closed by the user.

    - **vpn_ip**: The VPN IP to identify the user
    """
    try:
        disconnected_user = {
        "vpn_ip" : vpn_ip,
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
        return disconnected_user
    except ValueError as ve:
        # Handle known validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/service/inlab")
async def inlab():
    """
    Returns the list of users that are inside the lab
    """
    try: 
        inlab_users = [
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
        return inlab_users
    except ValueError as ve:
        # Handle known validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@app.get("/service/waiting")
async def waiting():
    """
    Returns the list of users that are outside the lab and are waiting to enter
    """
    try:
        waiting_users = [
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
            },
        ]
        return waiting_users
    except ValueError as ve:
        # Handle known validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@app.get("/service/bookings")
async def bookings():
    """
    Returns the list of bookings available for the lab.
    """
    try:

        bookings = [
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
        return bookings
    except ValueError as ve:
        # Handle known validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.patch("/service/availability/{available}")
async def set_availability(available: bool):
    """
    Updates the availability status of the lab service.

    - **available**: Boolean value (true/false) indicating if the lab is available
    """
    try:
        data = {
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
            "available": available,
            "ip": "10.112.0.1",
            "port": "5000",
            "protocol": "tcp",
            "entry_point": "",
            "id": 1,
            "created_at": "2025-02-14 22:30:00"
        }
        return data
    except ValueError as ve:
        # Handle known validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SRL Service')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the SRL service (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind the SRL service (default: 8000)')
    args = parser.parse_args()
    
    print(f"🚀 SRL service running at http://{args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)
