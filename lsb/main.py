import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template_string
from flask_socketio import SocketIO
import math
import random
import time
import argparse

app = Flask(__name__)
socketio = SocketIO(app)

# Global variable for SRL service URL
SRL_SERVICE_URL = "http://localhost:8000"

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Experiment Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.min.js"></script>
    <style>
        body { font-family: sans-serif; margin: 20px; background: #f8f9fa; }
        h1 { text-align: center; }
        .charts { display: flex; flex-wrap: wrap; justify-content: space-around; }
        .chart-box { width: 45%; min-width: 300px; margin: 20px 0; }
        .slider-container { text-align: center; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>🔬 Real-Time Experiment Dashboard</h1>

    <div id="user-data" style="text-align: center; margin: 20px 0; padding: 15px; background: #e9ecef; border-radius: 8px;">
        <div id="user-info">Loading user data...</div>
        <button id="disconnect-btn" style="margin-top: 15px; padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; font-weight: bold;">
            🔌 Disconnect from Lab
        </button>
        <div id="disconnect-message" style="margin-top: 10px;"></div>
    </div>

    <div class="slider-container">
        <label for="amplitude">Amplitude: </label>
        <input type="range" id="amplitude" min="0" max="5" step="0.1" value="1">
        <span id="amp-value">1</span>
    </div>

    <div class="charts">
        <div class="chart-box"><div id="line-plot"></div></div>
        <div class="chart-box"><div id="bar-plot"></div></div>
        <div class="chart-box"><div id="pie-chart"></div></div>
    </div>

    <div id="waiting-users-section" style="margin: 20px auto; max-width: 800px; padding: 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="text-align: center; margin-bottom: 15px;">👥 Users Waiting to Enter the Lab</h3>
        <div id="waiting-users-list">Loading waiting users...</div>
    </div>

    <div id="inlab-users-section" style="margin: 20px auto; max-width: 800px; padding: 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="text-align: center; margin-bottom: 15px;">✅ Users Currently in the Lab</h3>
        <div id="inlab-users-list">Loading users in lab...</div>
    </div>

    <div id="bookings-section" style="margin: 20px auto; max-width: 800px; padding: 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="text-align: center; margin-bottom: 15px;">📅 Current Lab Bookings</h3>
        <div id="bookings-list">Loading bookings...</div>
    </div>

    <script>
        const SRL_SERVICE_URL = "{{ srl_url }}";
        
        // Fetch user data from SRL service
        async function fetchUserData() {
            try {
                const vpnId = 123; // You can change this or make it dynamic
                const response = await fetch(`${SRL_SERVICE_URL}/user_data?vpn_id=${vpnId}`);
                const data = await response.json();
                
                if (data.message) {
                    const userData = data.message;
                    const userInfoDiv = document.getElementById('user-info');
                    userInfoDiv.innerHTML = `
                        <h2 style="margin: 10px 0;">Welcome back, ${userData.first_name} ${userData.last_name}!</h2>
                        <div style="display: flex; justify-content: center; align-items: center; gap: 20px; flex-wrap: wrap; margin-top: 15px;">
                            <span><strong>Email:</strong> ${userData.email}</span>
                            <span><strong>Matricola:</strong> ${userData.matricola}</span>
                            <span><strong>Role:</strong> ${userData.role}</span>
                            <span><strong>Status:</strong> ${userData.status}</span>
                            <span><strong>You accessed the lab at:</strong> ${userData.LabAccessTime}</span>
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Error fetching user data:', error);
                document.getElementById('user-info').innerHTML = '<p style="color: red;">Error loading user data</p>';
            }
        }

        // Fetch waiting users from SRL service
        async function fetchWaitingUsers() {
            try {
                const response = await fetch(`${SRL_SERVICE_URL}/waiting_users`);
                const data = await response.json();
                
                if (data.waiting_users) {
                    const users = data.waiting_users;
                    const waitingListDiv = document.getElementById('waiting-users-list');
                    
                    if (users.length === 0) {
                        waitingListDiv.innerHTML = '<p style="text-align: center; color: #6c757d;">No users waiting</p>';
                    } else {
                        let listHTML = '<ul style="list-style: none; padding: 0;">';
                        users.forEach(user => {
                            listHTML += `
                                <li style="padding: 12px; margin: 8px 0; background: #f8f9fa; border-left: 4px solid #007bff; border-radius: 4px;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                                        <span style="font-weight: bold; font-size: 1.1em;">${user.first_name} ${user.last_name}</span>
                                        <span style="color: #6c757d;">Matricola: ${user.matricola}</span>
                                        <span style="color: #6c757d;">Email: ${user.email}</span>
                                        <span style="color: #6c757d;">Role: ${user.role}</span>
                                        <span style="color: #dc3545; font-size: 0.9em;">⏰ Waiting since: ${user.waiting_since}</span>
                                    </div>
                                </li>
                            `;
                        });
                        listHTML += '</ul>';
                        waitingListDiv.innerHTML = listHTML;
                    }
                }
            } catch (error) {
                console.error('Error fetching waiting users:', error);
                document.getElementById('waiting-users-list').innerHTML = '<p style="color: red; text-align: center;">Error loading waiting users</p>';
            }
        }

        // Fetch in-lab users from SRL service
        async function fetchInLabUsers() {
            try {
                const response = await fetch(`${SRL_SERVICE_URL}/inlab_users`);
                const data = await response.json();
                
                if (data.waiting_users) {
                    const users = data.waiting_users;
                    const inlabListDiv = document.getElementById('inlab-users-list');
                    
                    if (users.length === 0) {
                        inlabListDiv.innerHTML = '<p style="text-align: center; color: #6c757d;">No users in lab</p>';
                    } else {
                        let listHTML = '<ul style="list-style: none; padding: 0;">';
                        users.forEach(user => {
                            listHTML += `
                                <li style="padding: 12px; margin: 8px 0; background: #f8f9fa; border-left: 4px solid #28a745; border-radius: 4px;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                                        <span style="font-weight: bold; font-size: 1.1em;">${user.first_name} ${user.last_name}</span>
                                        <span style="color: #6c757d;">Matricola: ${user.matricola}</span>
                                        <span style="color: #6c757d;">Email: ${user.email}</span>
                                        <span style="color: #6c757d;">Role: ${user.role}</span>
                                        <span style="color: #6c757d;">VPN ID: ${user.vpn_id}</span>
                                        <span style="color: #28a745; font-size: 0.9em;">🚪 Accessed at: ${user.access_at}</span>
                                    </div>
                                </li>
                            `;
                        });
                        listHTML += '</ul>';
                        inlabListDiv.innerHTML = listHTML;
                    }
                }
            } catch (error) {
                console.error('Error fetching in-lab users:', error);
                document.getElementById('inlab-users-list').innerHTML = '<p style="color: red; text-align: center;">Error loading in-lab users</p>';
            }
        }

        // Fetch bookings from SRL service
        async function fetchBookings() {
            try {
                const response = await fetch(`${SRL_SERVICE_URL}/bookings`);
                const data = await response.json();
                
                if (data.current_bookings) {
                    const bookings = data.current_bookings;
                    const bookingsListDiv = document.getElementById('bookings-list');
                    
                    if (bookings.length === 0) {
                        bookingsListDiv.innerHTML = '<p style="text-align: center; color: #6c757d;">No bookings available</p>';
                    } else {
                        let listHTML = '<ul style="list-style: none; padding: 0;">';
                        bookings.forEach(booking => {
                            listHTML += `
                                <li style="padding: 12px; margin: 8px 0; background: #f8f9fa; border-left: 4px solid #ffc107; border-radius: 4px;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                                        <span style="font-weight: bold; font-size: 1.1em;">${booking.first_name} ${booking.last_name}</span>
                                        <span style="color: #6c757d;">Email: ${booking.email}</span>
                                        <span style="color: #6c757d;">Role: ${booking.role}</span>
                                        <span style="color: #ffc107; font-size: 0.9em;">📅 Time Slot: ${booking.time_slot}</span>
                                    </div>
                                </li>
                            `;
                        });
                        listHTML += '</ul>';
                        bookingsListDiv.innerHTML = listHTML;
                    }
                }
            } catch (error) {
                console.error('Error fetching bookings:', error);
                document.getElementById('bookings-list').innerHTML = '<p style="color: red; text-align: center;">Error loading bookings</p>';
            }
        }

        // Handle disconnect button
        async function disconnectFromLab() {
            try {
                const vpnId = 123; // Should match the VPN ID used in fetchUserData
                const disconnectBtn = document.getElementById('disconnect-btn');
                const messageDiv = document.getElementById('disconnect-message');
                
                // Disable the button
                disconnectBtn.disabled = true;
                disconnectBtn.style.background = '#6c757d';
                disconnectBtn.style.cursor = 'not-allowed';
                
                const response = await fetch(`${SRL_SERVICE_URL}/close_connection?vpn_id=${vpnId}`);
                const data = await response.json();
                
                console.log('API Response:', data); // Log the full response
                
                if (data.release_lsb) {
                    console.log('Disconnect message:', data.release_lsb); // Log the message
                    messageDiv.innerHTML = `<p style="color: #28a745; font-weight: bold;">✅ ${data.release_lsb}</p>`;
                } else {
                    console.warn('No release_lsb message in response');
                    messageDiv.innerHTML = '<p style="color: #ffc107; font-weight: bold;">⚠️ Disconnected but no message received</p>';
                }
                
                // Re-enable the button and clear message after 10 seconds
                setTimeout(() => {
                    disconnectBtn.disabled = false;
                    disconnectBtn.style.background = '#dc3545';
                    disconnectBtn.style.cursor = 'pointer';
                    messageDiv.innerHTML = '';
                }, 5000);
                
            } catch (error) {
                console.error('Error disconnecting:', error);
                const messageDiv = document.getElementById('disconnect-message');
                const disconnectBtn = document.getElementById('disconnect-btn');
                
                messageDiv.innerHTML = '<p style="color: red; font-weight: bold;">❌ Error disconnecting from lab</p>';
                
                // Re-enable the button and clear message after 10 seconds even on error
                setTimeout(() => {
                    disconnectBtn.disabled = false;
                    disconnectBtn.style.background = '#dc3545';
                    disconnectBtn.style.cursor = 'pointer';
                    messageDiv.innerHTML = '';
                }, 5000);
            }
        }

        // Add event listener to disconnect button
        document.getElementById('disconnect-btn').addEventListener('click', disconnectFromLab);

        // Fetch user data when page loads
        fetchUserData();
        fetchWaitingUsers();
        fetchInLabUsers();
        fetchBookings();

        const socket = io();
        const ampSlider = document.getElementById('amplitude');
        const ampValue = document.getElementById('amp-value');

        ampSlider.addEventListener('input', () => {
            ampValue.textContent = ampSlider.value;
            socket.emit('set_amplitude', parseFloat(ampSlider.value));
        });

        let x = [], y = [];
        const maxPoints = 50;

        Plotly.newPlot('line-plot', [{ x: [], y: [], mode: 'lines', name: 'Signal', line: { shape: 'spline' } }], { title: 'Signal Over Time' });
        Plotly.newPlot('bar-plot', [{ x: ['A','B','C'], y: [0,0,0], type: 'bar', name: 'Category Values' }], { title: 'Bar Chart' });
        Plotly.newPlot('pie-chart', [{ labels: ['A','B','C'], values: [0,0,0], type: 'pie', textinfo: 'label+percent', insidetextorientation: 'radial' }], { title: 'Pie Chart' });

        socket.on('new_data', function(data) {
            x.push(data.time);
            y.push(data.value);
            if (x.length > maxPoints) { x.shift(); y.shift(); }

            Plotly.update('line-plot', { x: [x], y: [y] });
            Plotly.update('bar-plot', { y: [[data.categories.A, data.categories.B, data.categories.C]] });
            Plotly.update('pie-chart', { values: [[data.categories.A, data.categories.B, data.categories.C]] });
        });
    </script>
</body>
</html>
"""

amplitude = 1.0

@app.route("/")
def index():
    return render_template_string(HTML_PAGE, srl_url=SRL_SERVICE_URL)

@socketio.on('set_amplitude')
def set_amplitude(value):
    global amplitude
    amplitude = value

def emit_experiment_data():
    t = 0
    while True:
        scalar_value = amplitude * math.sin(t) + random.gauss(0, 0.1)
        categories = {"A": random.randint(10,30), "B": random.randint(5,25), "C": random.randint(15,35)}
        socketio.emit('new_data', {'time': round(t,1), 'value': round(scalar_value,3), 'categories': categories})
        t += 0.1
        time.sleep(0.5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LSB Service')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the LSB service (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind the LSB service (default: 5000)')
    parser.add_argument('--srl-host', type=str, default='localhost', help='Host of the SRL service (default: localhost)')
    parser.add_argument('--srl-port', type=int, default=8000, help='Port of the SRL service (default: 8000)')
    args = parser.parse_args()
    
    SRL_SERVICE_URL = f"http://{args.srl_host}:{args.srl_port}"
    
    print(f"🚀 Live dashboard running at http://{args.host}:{args.port}")
    print(f"🔗 Connecting to SRL service at {SRL_SERVICE_URL}")
    socketio.start_background_task(emit_experiment_data)
    socketio.run(app, host=args.host, port=args.port)
