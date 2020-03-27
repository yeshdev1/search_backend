from flask import Flask, request
import json
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import sqlite3
from flask import g

from run import run_preprocessing;
from run import load_inverted_index, extract_links_only;

@app.route('/index_data', methods=['GET'])
def inverted_index_construction():
    run_preprocessing('websites');
    return jsonify({"index":"done"}), 200

@app.route('/search_benchmark_index', methods=['GET'])
def search_benchmark_index():
    run_preprocessing('test');
    return jsonify({"index":"done"}), 200

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query');
    extracted_links_and_ranks = load_inverted_index(query);
    links = extract_links_only(extracted_links_and_ranks);
    return jsonify(links), 200
