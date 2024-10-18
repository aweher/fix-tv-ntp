#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hecho por Ayuda.LA
# https://ayuda.la/

import logging
import time
import threading
from flask import Flask, jsonify, request

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    """
    Genera una respuesta JSON que necesitan los TV para setear la hora.
    """

    response = {
        "retCode": "0",
        "time": int(time.time() * 1000),
        "ips": ["synctime.hismarttv.com"]
    }
    return jsonify(response)

@app.errorhandler(404)
def not_found(e):
    """
    Maneja todos los requests enviandolos a home.
    """
    return home()

app.after_request
def add_header(response):
    """
    Añade encabezados para evitar el cacheo de la página.
    """
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.before_request
def log_request_info():
    """
    Registra la información de la solicitud entrante.
    """
    logger.info(f"Solicitud recibida: {request.remote_addr} {request.method} {request.url} {request.referrer}")
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Cuerpo: {request.get_data()}")

if __name__ == '__main__':
    logger.info("Iniciando la aplicación.")
    app.run(debug=True)
