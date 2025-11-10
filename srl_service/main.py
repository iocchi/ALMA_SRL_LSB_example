# file: main.py
from fastapi import FastAPI, HTTPException
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

@app.get("/user_data")
async def get_user(vpn_id: int):
    """
    Retrieve user data by ID.

    - **vpn_id**: The VPN ID to identify the user
    """
    try:
        if vpn_id <= 0:
            raise ValueError("Invalid VPN ID")
        user_data = {
            "vpn_id" : vpn_id,
            "matricola" : "1111234",
            "first_name": "Mario",
            "last_name": "Rossi",
            "email" : "mrossi@test.it",
            "status" : "active",
            "role" : "student",
            "ID_lab" : "1", 
            "privilege" : "1",
            "IDMAccessTime" : "2025-06-11 14:30:00",
            "LabAccessTime" : "2025-06-11 15:30:00",
            "created_at" : "2025-05-11 14:30:00"
        }
        return {"message": user_data}
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
                "waiting_since": "2025-05-11 14:45:15"
            },
            {
                "id": "4",
                "first_name": "Giovanni",
                "last_name": "Neri",
                "email": "gneri@test.it",
                "matricola" : "7777654",
                "role": "student",
                "waiting_since": "2025-05-11 15:00:00"
            },
        ]
        return {"waiting_users": waiting_users}
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
        waiting_users = [
            {
                "id": "3",
                "first_name": "Lucia",
                "last_name": "Verdi",
                "email": "lverdi@test.it",
                "matricola" : "3333456",
                "role": "student",
                "access_at": "2025-05-11 14:45:15",
                "vpn_id" : "192.168.0.14"
            },
            {
                "id": "4",
                "first_name": "Giovanni",
                "last_name": "Neri",
                "email": "gneri@test.it",
                "matricola" : "4444456",
                "role": "student",
                "access_at": "2025-05-11 15:00:00",
                "vpn_id" : "192.168.0.15"
            },
        ]
        return {"waiting_users": waiting_users}
    except ValueError as ve:
        # Handle known validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@app.get("/close_connection")
async def close_connection(vpn_id: int):
    """
    Notifies SRL that the connection with the LSB has being closed by the user.

    - **vpn_id**: The VPN ID to identify the user
    """
    try:
        if vpn_id <= 0:
            raise ValueError("Invalid VPN ID")
        return {"release_lsb": "Successfully closed connection with SRL"}
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
                "time_slot" : "2025-05-11 14:30:00",
                "id" : "1",
                "first_name" : "Mario",
                "last_name" : "Rossi",
                "email" : "mrossi@test.it",
                "role" : "student"
            },
            {
                "time_slot" : "2025-05-11 15:30:00",
                "id" : "2",
                "first_name" : "Bob",
                "last_name" : "Bbianchi",
                "email" : "bbianchi@test.it",
                "role" : "student"
            }
        ]
        return {"current_bookings": bookings}
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
