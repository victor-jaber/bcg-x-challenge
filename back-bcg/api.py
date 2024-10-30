from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import re
from configparser import ConfigParser
import ast
from functions.utils import get_dir_config, database_exists, log
from functions.bronze_ingestion import bronze_data_ingestion
from functions.silver_ingestion import silver_data_ingestion
from functions.gold_ingestion import gold_data_ingestion
from functions.get_message import process_input_with_retrieval
from database import init_db, register_user, verify_user

# Initialize the database
init_db()

app = Flask(__name__)
CORS(app)

# Load configuration
ini_config = get_dir_config()
config = ConfigParser()
config.read(ini_config, encoding="utf8")
logger = log(config)

# Check if the database exists and perform data ingestion if needed
if not database_exists(logger):
    metadata = ast.literal_eval(config["METADATA"]["TABLE_NAME"])
    for pdf_name, table_name in metadata.items():
        logger.info(f'>>> Processando a tabela {table_name}...')
        bronze_data_ingestion(pdf_name, table_name, logger)
        silver_data = silver_data_ingestion(pdf_name, table_name, logger)
        gold_data_ingestion(table_name, silver_data, logger)

# Helper function to clean HTML tags from text
def clean_html(raw_html):
    clean_text = re.sub('<[^<]+?>', '', raw_html)
    return clean_text

# Chatbot query endpoint
@app.route('/query', methods=['POST'])
def query():
    data = request.json
    user_query = data.get('query', '')

    # Process the input query using the retrieval function
    final_response = process_input_with_retrieval(user_query, logger)

    # Clean and return the response as JSON
    clean_response = clean_html(final_response)
    return jsonify({"response": clean_response})

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    if register_user(name, email, password):
        return jsonify({"message": "Usuário registrado com sucesso"}), 201
    else:
        return jsonify({"error": "Usuário já registrado com este email"}), 409

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    if verify_user(email, password):
        return jsonify({"message": "Login bem-sucedido"}), 200
    else:
        return jsonify({"error": "Email ou senha inválidos"}), 401

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
