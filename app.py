import os
import boto3
import json
import io
from flask import Flask, jsonify, request, render_template
from pypdf import PdfReader

app = Flask(__name__)

# Initialize Bedrock Runtime client in Mumbai region (ap-south-1)
bedrock_client = boto3.client('bedrock-runtime', region_name='ap-south-1')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "GenAI Document Intelligence API"})

@app.route('/process', methods=['POST'])
def process_document():
    doc_text = ""
    
    # Check if a PDF file was uploaded
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename.endswith('.pdf'):
            try:
                pdf_stream = io.BytesIO(file.read())
                reader = PdfReader(pdf_stream)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        doc_text += text + "\n"
            except Exception as e:
                return jsonify({"status": "error", "message": f"Failed to parse PDF: {str(e)}"}), 400

    # If no file or text extracted from file, check JSON body
    if not doc_text.strip():
        data = request.json or {}
        doc_text = data.get('text', '')

    if not doc_text.strip():
        return jsonify({"status": "error", "message": "No text provided or PDF file is empty."}), 400
    
    try:
        # Payload for Amazon Nova Micro model using APAC inference profile
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": f"Analyze and summarize the following document text: {doc_text}"
                        }
                    ]
                }
            ],
            "inferenceConfig": {
                "max_new_tokens": 500
            }
        }
        
        response = bedrock_client.invoke_model(
            modelId='apac.amazon.nova-micro-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps(payload)
        )
        
        response_body = json.loads(response['body'].read())
        ai_output = response_body.get('output', {}).get('message', {}).get('content', [{}])[0].get('text', 'No response generated')
        
        return jsonify({
            "status": "success",
            "document_analysis": ai_output
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
