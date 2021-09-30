import urllib3
import boto3
import json

client = boto3.client('sns')

web_hook = "WEB_HOOK_SLACK"
mensagem = {"text": "A plataforma __platform__ saiu do ar."}

urls = {
    'nome_plataforma_1': 'https://www.nome_plataforma_1.com.br', 
    'nome_plataforma_2': 'https://www.nome_plataforma_2.com.br'
}

def lambda_handler(event, context):
    http = urllib3.PoolManager()
    
    for key in urls:
        try:
            http.request('GET', urls[key])
            print("HEALTH >> OK")
        except Exception:
            print("HEALTH >> FAIL")
            send_notify(http, key)
        
def send_notify(http, platformName):
    # send notify to SNS (Email and SMS)
    client.publish(
        TopicArn="arn:aws:sns:", # ARN of SNS
        Message="HEALTH >> FAIL (" + platformName + ")",
        Subject="[ALERT CHECK HEALTH]"
    )
    
    # send notify in SLACK
    mensagem["text"] = mensagem["text"].replace("__platform__", platformName)
    http.request('POST', web_hook, body=json.dumps(mensagem))
