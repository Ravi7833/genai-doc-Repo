import boto3
from botocore.exceptions import ClientError
import os

# Initialize Bedrock Runtime client explicitly set to Mumbai region (ap-south-1)
REGION_NAME = os.environ.get("AWS_REGION", "ap-south-1")

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=REGION_NAME
)

def generate_document_summary(prompt_text):
    # Model ID for ap-south-1 (e.g., Amazon Nova Lite or Claude 3 Haiku)
    model_id = os.environ.get("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")
    
    native_request = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt_text}]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 512,
            "temperature": 0.3
        }
    }

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=str(native_request)
        )
        return response
    except ClientError as e:
        print(f"Error invoking Bedrock in {REGION_NAME}: {e.response['Error']['Message']}")
        raise e
