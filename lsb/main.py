import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template_string
from flask_socketio import SocketIO
import math
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)

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

    <script>
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
    return render_template_string(HTML_PAGE)

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
    print("🚀 Live dashboard running at http://127.0.0.1:5000")
    socketio.start_background_task(emit_experiment_data)
    socketio.run(app, host="0.0.0.0", port=5000)
