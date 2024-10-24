from fastapi import FastAPI, HTTPException
import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from typing import List

# Load environment variables
#load_dotenv()

# FastAPI instance
app = FastAPI()

# AWS Credentials from Environment Variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')

# Initialize DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# Your DynamoDB table name
TABLE_NAME = 'items'

@app.get("/", response_model=dict)
def home():
    return({"message": "Welcome to the FastAPI app!"})

@app.get("/items", response_model=List[dict])
async def get_items():
    try:
        # Get reference to DynamoDB table
        table = dynamodb.Table(TABLE_NAME)
        
        # Scan the table to get all items
        response = table.scan()
        items = response.get('Items', [])

        if not items:
            raise HTTPException(status_code=404, detail="No items found.")

        return items

    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="No AWS credentials found.")

    except PartialCredentialsError:
        raise HTTPException(status_code=500, detail="Incomplete AWS credentials.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))