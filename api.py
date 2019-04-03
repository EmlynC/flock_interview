from flask import Flask, jsonify
import requests
import logging

app = Flask(__name__)
BOBS_URL = 'https://bobs-epic-drone-shack-inc.herokuapp.com'

cache = {}

logging.basicConfig(
    format='%(asctime)-15s: %(message)s',
    level=logging.INFO,
)

class UnavailableUpstream(Exception):
    pass

@app.before_request
def start_request():
    logging.info('Request started')
    
@app.after_request
def end_request(resp):
    logging.info('Request end')
    resp.headers['Cache-Control'] = 'max-age=60'
    return resp
    
def cache_data(req, key):
    if req.ok:
        data = req.json()
        cache[key] = data
        logging.info('Cache set with new data')
    else:
        if key in cache:
            data = cache[key]
            logging.info('Data retreived from cache')
        else:
            logging.info(str(req))
            raise UnavailableUpstream('Upstream API unavailable')

    return data

@app.route('/api/v0/drones')
def drones_list():
    
    resp = requests.get(f'{BOBS_URL}/api/v0/drones')

    try:
        data = cache_data(resp, 'latest')
        payload = jsonify(data), 200
    except UnavailableUpstream as e:
        payload = str(e), 502

    logging.info('Request end')
    return payload


@app.route('/api/v0/drones/<id>')
def get_drone(id):
    resp = requests.get(f'{BOBS_URL}/api/v0/drone/{id}')
    cache_key = f'latest_{id}'

    try:
        data = cache_data(resp, cache_key)
        payload = jsonify(data), 200
    except UnavailableUpstream as e:
        payload = str(e), 502

    return payload


logging.info('Bring up the webserver')
app.run()
