from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Orthanc server details from environment variables
ORTHANC_URL = os.getenv('ORTHANC_URL')
ORTHANC_USER = os.getenv('ORTHANC_USER')
ORTHANC_PASS = os.getenv('ORTHANC_PASS')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/modalities', methods=['GET'])
def list_modalities():
    try:
        response = requests.get(f'{ORTHANC_URL}/modalities/', auth=HTTPBasicAuth(ORTHANC_USER, ORTHANC_PASS))
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        modalities = response.json()  # This will be a list, not a dict
        return render_template('modalities.html', modalities=modalities)
    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': f"HTTP error occurred: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        return jsonify({'error': f"Request error occurred: {req_err}"}), 500
    except ValueError as json_err:
        return jsonify({'error': f"Invalid JSON response: {json_err}"}), 500
    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500

@app.route('/modalities/add', methods=['POST'])
def add_modality():
    data = request.form
    modality_name = data.get('name')
    aet = data.get('aet')
    host = data.get('host')
    port = data.get('port')

    try:
        response = requests.put(
            f'{ORTHANC_URL}/modalities/{modality_name}',
            json={'AET': aet, 'Host': host, 'Port': int(port)},
            auth=HTTPBasicAuth(ORTHANC_USER, ORTHANC_PASS)
        )
        if response.status_code == 200:
            return redirect(url_for('list_modalities'))
        else:
            return jsonify({'error': response.text}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/modalities/delete/<modality_name>', methods=['POST'])
def delete_modality(modality_name):
    try:
        response = requests.delete(f'{ORTHANC_URL}/modalities/{modality_name}', auth=HTTPBasicAuth(ORTHANC_USER, ORTHANC_PASS))
        if response.status_code == 200:
            return redirect(url_for('list_modalities'))
        else:
            return jsonify({'error': response.text}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def server_status():
    try:
        response = requests.get(f'{ORTHANC_URL}/system', auth=HTTPBasicAuth(ORTHANC_USER, ORTHANC_PASS))
        status = response.json()
        return render_template('status.html', status=status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
