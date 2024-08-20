from flask import Flask, jsonify, render_template, request
from lib import *

# Component value selections
component_values = {
    "Resistor": ["10 Ohm", "5 Ohm", "2.2 Ohm", "1 Ohm", "0.5 Ohm", "0.2 Ohm", "0.1 Ohm", "0.01 Ohm"],
    "Inductor": ["1.2 mH", "1 mH", "1.5 mH", "0.8 mH", "0.5 mH", "0.2 mH", "0.1 mH", "0.05 mH"],
    "Capacitor": ["330 uF", "220 uF", "180 uF", "150 uF", "100 uF", "50 uF", "20 uF", "10 uF"]
}

parameters = [
    {
        "label": "Low Pass Filter - Inductor",
        "default": "1.2 mH",
        "kind": "Inductor",
        "variable": "inductor_low"
    },
    {
        "label": "Low Pass Filter - Capacitor",
        "default": "330 uF",
        "kind": "Capacitor",
        "variable": "capacitor_low"
    },
    {
        "label": "High Pass Filter - Resistor 1",
        "default": "10 Ohm",
        "kind": "Resistor",
        "variable": "resistor_high1"
    },
    {
        "label": "High Pass Filter - Capacitor",
        "default": "330 uF",
        "kind": "Capacitor",
        "variable": "capacitor_high"
    },
    {
        "label": "High Pass Filter - Inductor",
        "default": "1.2 mH",
        "kind": "Inductor",
        "variable": "inductor_high"
    },
    {
        "label": "High Pass Filter - Resistor 2",
        "default": "5 Ohm",
        "kind": "Resistor",
        "variable": "resistor_high2"
    },
]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/getParameters', methods = ['GET'])
def getParameters():
    response = { 
        "values" : component_values,
        "parameters": parameters
    } 
    return jsonify(response) 


@app.route('/generateSchematics', methods = ['GET'])
def generateSchematics():
    query_args = request.args

    low_pass, high_pass = drawSchematics(
        query_args.get('inductor_low'),
        query_args.get('capacitor_low'),
        query_args.get('resistor_high1'),
        query_args.get('capacitor_high'),
        query_args.get('inductor_high'),
        query_args.get('resistor_high2')
    )

    response = { 
        "low_pass" : low_pass,
        "high_pass" : high_pass,
    } 

    return jsonify(response) 


@app.route('/saveSchematicsPng', methods = ['GET'])
def saveSchematicsPng():
    exportPng()
    return jsonify({ "status": "ok" })

@app.route('/sendArduino', methods = ['GET'])
def sendArduino() :
    print('Sending to Arduino')
    query_args = request.args

    sendCommand(
        query_args.get('inductor_low'),
        query_args.get('capacitor_low'),
        query_args.get('resistor_high1'),
        query_args.get('capacitor_high'),
        query_args.get('inductor_high'),
        query_args.get('resistor_high2')
    )
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)