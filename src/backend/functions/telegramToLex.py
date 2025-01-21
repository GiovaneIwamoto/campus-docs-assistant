import json
import boto3
from dotenv import load_dotenv
from IntegrationFunctions.telegram_lex_integration import *

load_dotenv()

lexruntime = boto3.client("lexv2-runtime")

def telegramToLex(event, context):
    try:
        print(f"[INFO] Evento recebido: {event}")
        
        # Corpo da requisição
        body = json.loads(event['body'])
        print(f"[INFO] Corpo da requisição processado: {body}")
        
        # Processa mensagens recebidas através de interações com os botões do Telegram
        if 'callback_query' in body:
            print("[INFO] Processando callback_query")
            callbackQuery = body['callback_query']
            chatID = callbackQuery['message']['chat']['id']
            callbackData = callbackQuery['data']
            print(f"[INFO] Callback recebido. Chat ID: {chatID}, Callback Data: {callbackData}")
            handleCallbackQuery(callbackQuery, str(chatID), callbackData)
        
        # Processa mensagens de texto normais    
        else:
            print("[INFO] Processando mensagem de texto")
            message = body['message']
            chatID = str(message['chat']['id'])
            print(f"[INFO] Mensagem recebida. Chat ID: {chatID}, Texto: {message['text']}")
        
            # Mapeando a mensagem do Telegram para o formato do Lex
            messageForLex = mapTelegramToLex(body)
            print(f"[INFO] Mensagem mapeada para o Lex. Mapeamento: {messageForLex}")
            
            # Processando a resposta do Lex
            print(f"[INFO] Iniciando processamento da resposta do Lex")
            processLexResponse(body, messageForLex['userId'], messageForLex['inputText'])
            print("[INFO] Processamento do Lex concluído.")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully processed message')
        }

    except Exception as e:
        print(f"[ERROR] Erro ao processar o evento: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps('Failed to process message')
        }
