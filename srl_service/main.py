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


@app.get("/user_data")
async def get_user(vpn_ip: str, request: Request):
    """
    Retrieve user data.

    - **vpn_ip**: The VPN IP to identify the user
    """

    client_ip = request.client.host
    print(f"Connection from {client_ip}")
    
    try:
        user_data = {
            "vpn_ip" : vpn_ip,
            "matricola" : "1111234",
            "first_name": "Mario",
            "last_name": "Rossi",
            "email" : "mrossi@test.it",
            "status" : "active",
            "role" : "student",
            "ID_lab" : "1", 
            "privilege" : "1",
            "IDMAccessTime" : "2025-05-20 15:25:38",
            "LabAccessTime" : "2025-05-20 15:30:00",
            "LabEndTime" : "2025-05-20 16:00:00",
            "created_at" : "2025-04-23 23:30:00"
        }
        return {"user_data": user_data}
    except ValueError as ve:
        # Handle known validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/close_connection")
async def close_connection(vpn_ip: str):
    """
    Notifies SRL that the connection with the LSB has being closed by the user.

    - **vpn_ip**: The VPN IP to identify the user
    """
    try:
        return {"close_connection": {"status": "success", "vpn_ip" : vpn_ip} }
    except ValueError as ve:
        # Handle known validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@app.get("/inlab_users")
async def inlab_users():
    """
    Returns the list of users that are inside the lab
    """
    try: 
        inlab_users = [
            {
                "id": "3",
                "first_name": "Alberto",
                "last_name": "Bianchi",
                "email": "abianchi@test.it",
                "matricola" : "3333456",
                "role": "student",
                "access_at": "2025-05-20 15:35:15",
                "vpn_ip" : "192.168.0.14"
            },
            {
                "id": "4",
                "first_name": "Giovanna",
                "last_name": "Verdi",
                "email": "gverdi@test.it",
                "matricola" : "4444456",
                "role": "student",
                "access_at": "2025-05-20 15:40:20",
                "vpn_ip" : "192.168.0.15"
            },
        ]
        return {"inlab_users": inlab_users}
    except ValueError as ve:
        # Handle known validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@app.get("/waiting_users")
async def waiting_users():
    """
    Returns the list of users that are outside the lab and are waiting to enter
    """
    try:
        waiting_users = [
            {
                "id": "3",
                "first_name": "Lucia",
                "last_name": "Verdi",
                "email": "lverdi@test.it",
                "matricola" : "2345678",
                "role": "student",
                "waiting_since": "2025-05-20 15:45:25"
            },
            {
                "id": "4",
                "first_name": "Giovanni",
                "last_name": "Neri",
                "email": "gneri@test.it",
                "matricola" : "7777654",
                "role": "student",
                "waiting_since": "2025-05-20 15:50:30"
            },
        ]
        return {"waiting_users": waiting_users}
    except ValueError as ve:
        # Handle known validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@app.get("/bookings")
async def bookings():
    """
    Returns the list of bookings available for the lab.
    """
    try:
        bookings = [
            {
                "time_slot" : "2025-05-21 14:30:00",
                "id" : "1",
                "first_name" : "Mario",
                "last_name" : "Rossi",
                "email" : "mrossi@test.it",
                "matricola" : "1111234",
                "role" : "studente"
            },
            {
                "time_slot" : "2025-05-21 15:30:00",
                "id" : "2",
                "first_name" : "Carla",
                "last_name" : "Bianchi",
                "email" : "cbianchi@test.it",
                "matricola" : "5553456",
                "role" : "studente"
            }
        ]
        return {"bookings": bookings}
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
