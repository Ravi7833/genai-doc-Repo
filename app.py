import os
import boto3
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Initialize Bedrock Runtime client in Mumbai region (ap-south-1)
bedrock_client = boto3.client('bedrock-runtime', region_name='ap-south-1')

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "GenAI Document Intelligence API"})

@app.route('/process', methods=['POST'])
def process_document():
    data = request.json or {}
    doc_text = data.get('text', 'Please analyze this document.')
    
    try:
        # Payload for Amazon Nova Micro model
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
            modelId='amazon.nova-micro-v1:0',
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
