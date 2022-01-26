from fileinput import filename
from requests import get
from fpdf import FPDF
import json
import boto3
from botocore.client import Config


def llamada(event, context):
    response = get("https://mindicador.cl/api/uf")
    

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size = 10)

    temp_response = json.dumps(response.json(),indent=4, separators=(". ", " = "))
    temp_response = temp_response.split('\n')
    for line in temp_response:
        pdf.cell(200, 10, txt = line, ln = 1, align = 'L')
    
    
    pdf.output("Data.pdf")  
    
    
    client = boto3.client('s3', aws_access_key_id="S3RVER",
                      aws_secret_access_key="S3VER",
                      region_name="us-east-1",
                      endpoint_url="http://localhost:4569")
    nombre_archivo = "Data.pdf"
    with open(nombre_archivo, 'rb') as archivo:
        client.put_object(
            ACL='public-read',
            Body=archivo,
            Bucket='local-bucket',
            Key=nombre_archivo
        )

    
    
    response = {"statusCode": 200, "body": response.text}
    
    return response

