from serial import Serial
import time
arduino = Serial('COM3', 250000)
time.sleep(2)

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

arduino.write(b'forward_on\n')
time.sleep(0.1)
arduino.write(b'forward_off\n')
time.sleep(0.1)
arduino.write(b'backward_on\n')
time.sleep(0.1)
arduino.write(b'backward_off\n')
time.sleep(0.1)
arduino.write(b'left_on\n')
time.sleep(0.1)
arduino.write(b'left_off\n')
time.sleep(0.1)
arduino.write(b'right_on\n')
time.sleep(0.1)
arduino.write(b'right_off\n')

status = {
    'forward': False,
    'backward': False,
    'left': False,
    'right': False
}

@app.route("/status")
def get_status():
    return jsonify(status)

@app.route("/stop")
def stop():
    status['forward'] = False
    status['backward'] = False
    status['left'] = False
    status['right'] = False
    arduino.write(b'left_off\n')
    arduino.write(b'right_off\n')
    arduino.write(b'forward_off\n')
    arduino.write(b'backward_off\n')
    return "stop"

@app.route("/forward-on")
def forwardOn():
    if status['forward']:
        return "Forward on"
    status['forward'] = True
    arduino.write(b'forward_on\n')
    return "Forward on"

@app.route("/forward-off")
def forwardOff():
    if not status['forward']:
        return "Forward off"
    status['forward'] = False
    arduino.write(b'forward_off\n')
    return "Forward off"

@app.route("/backward-on")
def backwardOn():
    if status['backward']:
        return "Backward on"
    status['backward'] = True
    arduino.write(b'backward_on\n')
    return "Backward on"

@app.route("/backward-off")
def backwardOff():
    if not status['backward']:
        return "Backward off"
    status['backward'] = False
    arduino.write(b'backward_off\n')
    return "Backward off"

@app.route("/left-on")
def leftOn():
    if status['left']:
        return "Left on"
    status['left'] = True
    arduino.write(b'left_on\n')
    return "Left on"

@app.route("/left-off")
def leftOff():
    if not status['left']:
        return "Left off"
    status['left'] = False
    arduino.write(b'left_off\n')
    return "Left off"

@app.route("/right-on")
def rightOn():
    if status['right']:
        return "Right on"
    status['right'] = True
    arduino.write(b'right_on\n')
    return "Right on"

@app.route("/right-off")
def rightOff():
    if not status['right']:
        return "Right off"
    status['right'] = False
    arduino.write(b'right_off\n')
    return "Right off"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
