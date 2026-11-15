import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "GenAI Document Intelligence API"})

@app.route('/process', methods=['POST'])
def process_document():
    data = request.json or {}
    return jsonify({"message": "Document processed successfully", "received": data})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
