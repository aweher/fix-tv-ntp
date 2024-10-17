#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hecho por Ayuda.LA
# https://ayuda.la/

import logging
import time
import threading
import ntplib
from flask import Flask, jsonify, request

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ntp_client = ntplib.NTPClient()
ntp_server = 'pool.ntp.org'
current_time = int(time.time() * 1000)

def sync_time():
    """
    Sincroniza continuamente la hora actual via NTP.
    """

    global current_time

    while True:
        try:
            response = ntp_client.request(ntp_server, version=3)
            current_time = int(response.tx_time * 1000)
            logger.info("Hora sincronizada con éxito.")
        except Exception as e:
            logger.error(f"Error al sincronizar la hora: {e}")
        time.sleep(3600)

@app.route('/')
def home():
    """
    Genera una respuesta JSON que necesitan los TV para setear la hora.
    """

    response = {
        "retCode": "0",
        "time": current_time,
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
    threading.Thread(target=sync_time, daemon=True).start()
    app.run(debug=True)
