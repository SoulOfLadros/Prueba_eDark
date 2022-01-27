from fileinput import filename
from requests import get
from fpdf import FPDF
import json
import boto3
from botocore.client import Config
import datetime


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


def NuevoDolar(event,context):
    client = boto3.resource('dynamodb', aws_access_key_id="S3RVER",aws_secret_access_key="S3VER",endpoint_url='http://localhost:8000')
    
    #check if table exist

    lista_tablas = [table.name for table in client.tables.all()]
    
    if 'DolarDia' not in lista_tablas:
        tabla = client.create_table(
        TableName='DolarDia',
        KeySchema=[
            {
                'AttributeName': 'fecha',
                'KeyType': 'HASH'  
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'fecha',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    
    tabla = client.Table('DolarDia')

    dia_actual = datetime.datetime.today().strftime('%d-%m-%Y')
    hora_actual = datetime.datetime.today().strftime('%H:%M')

    valores = get("https://mindicador.cl/api/dolar/"+dia_actual)
    dic_valores = json.loads(valores.text)

    val_dolar = str(dic_valores['serie'][0]['valor'])

    response = tabla.put_item(Item = { 'fecha':dia_actual+hora_actual,'valor': val_dolar })

    response = {"statusCode": 200, "body": valores.text}
    
    return response

def TestingData (event,context):
    client = boto3.client('dynamodb', aws_access_key_id="S3RVER",aws_secret_access_key="S3VER",endpoint_url='http://localhost:8000')
    
    response = client.scan(TableName='DolarDia')


    response = {"statusCode": 200, "body": json.dumps(response)}
    
    return response