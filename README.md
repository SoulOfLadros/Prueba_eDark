# Prueba eDarkstore

#### Autor: Sebastian Araya Torres


**Para ejecutar este proyecto se necesita tener previamente instalado ciertas librerias de python3:**

    - datetime
    - boto3
    - fpdf
    - requests
    - filename

Todas ellas se logran instalarse con el comando: 
   
    $ python -m pip install "nombre_libreria"

### Luego en la carpeta del repositorio "Main_end", se deben correr los siguientes comandos en orden para que el proyecto se pueda ejecutar.


    npm install -g serverless 

Luego de instalar serverless, se agregar los plugins

    npm install serverless-offline --save-dev

    npm install serverless-s3-local --save-dev

    npm install --save serverless-dynamodb-local

Para lograr trabajar con dynamodb, es necesario tener instalado java.

    sls dynamodb install
    sls dynamodb start --migrate 

**Un detalle, luego de correr el ultimo comando, se debe cancelar el proceso con ctr+C**

Luego finalmente ejecutamos el comando para abrir el servidor de serverless, puede que se necesite una cuenta de serverless para evitar problemas con sls login.

    sls offline start

## Comandos solicitados

En la prueba se realizo el endpoint (POST) para guardar en un pdf el valor de la "UF" a traves del tiempo, luego de generar el pdf se sube a la capeta "buckets/local-bucket", siendo el s3.

Esto se ejecuta en:

    http://localhost:3000/dev/Llamada

Para la otra instrucción se creo un cron cada 5 minutos que obtiene el valor actual del dolar y lo guarda en la tabla de dynamodb "DolarDia", para ver el contenido de la tabla mientra se ejecuta el servidor, se pueden ver los valores en un json en el metodo GET.

Se obtiene en la url: 

    http://localhost:3000:dev/ListaTabla