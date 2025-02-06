import json
import boto3
from dotenv import load_dotenv
from IntegrationFunctions.telegram_lex_integration import *  

load_dotenv()

lexruntime = boto3.client("lexv2-runtime")

# Função principal que recebe eventos do Telegram, processa a mensagem e interage com o Amazon Lex
def telegramToLex(event, context):
    try:
        print(f"[INFO] Evento recebido: {event}")
        
        if not event.get('body'):
            raise ValueError("Corpo do evento está vazio")
            
        try:
            body = json.loads(event['body'])
            print(f"[INFO] Corpo da requisição processado: {body}")
        except json.JSONDecodeError as e:
            print(f"[ERROR] Falha ao decodificar JSON do corpo: {e}")
            raise
        
        # Se for uma interação de botão (callback_query), redireciona para a função correspondente
        if 'callback_query' in body:
            return handle_callback_query(body)
        
        # Se for uma mensagem de texto, redireciona para a função correspondente
        elif 'message' in body:
            return handle_text_message(body)
        
        else:
            raise ValueError("Formato de mensagem não reconhecido")
            
    except Exception as e:
        print(f"[ERROR] Erro ao processar o evento: {str(e)}")
        return create_response(400, 'Failed to process message')

# Processa interações de botões no Telegram (callback_query)
def handle_callback_query(body):
    try:
        print("[INFO] Processando callback_query")
        callback_query = body['callback_query']
        chat_id = str(callback_query['message']['chat']['id']) 
        callback_data = callback_query['data'] 
        print(f"[INFO] Callback recebido. Chat ID: {chat_id}, Callback Data: {callback_data}")
        
        # Chama a função responsável por tratar interações de botões
        handle_button_interaction(callback_query, chat_id)
        
        return create_response(200, 'Successfully processed callback query')
        
    except Exception as e:
        print(f"[ERROR] Erro ao processar callback query: {e}")
        
        # Tenta enviar uma mensagem de erro ao usuário no Telegram
        try:
            error_message = {
                "chatID": chat_id,
                "text": "Desculpe, ocorreu um erro ao processar sua solicitação."
            }
            sendToTelegram(error_message)
        except:
            pass  
        raise

# Processa mensagens de texto recebidas pelo bot no Telegram e envia a resposta do Lex ao usuário
def handle_text_message(body):
    try:
        print("[INFO] Processando mensagem de texto")
        message = body['message']
        
        if 'text' not in message:
            raise ValueError("Mensagem não contém texto")
            
        chat_id = str(message['chat']['id'])  
        text = message['text'] 
        print(f"[INFO] Mensagem recebida. Chat ID: {chat_id}, Texto: {text}")
        
        # Envia a mensagem do usuário para o Amazon Lex e obtém a resposta
        lex_response = recognizeTextWithLex(chat_id, text)
        print(f"[INFO] Resposta do Lex: {lex_response}")
        
        # Mapeia a resposta do Lex para o formato esperado pelo Telegram
        messages_for_telegram = mapLexToTelegram(lex_response, body)
        print(f"[INFO] Mensagens mapeadas para o Telegram: {messages_for_telegram}")
        
        # Envia cada mensagem gerada para o Telegram
        for msg in messages_for_telegram:
            sendToTelegram(msg)
        print("[INFO] Mensagens enviadas para o Telegram")
        
        return create_response(200, 'Successfully processed text message')
        
    except Exception as e:
        print(f"[ERROR] Erro ao processar mensagem de texto: {e}")
        
        # Tenta enviar uma mensagem de erro ao usuário no Telegram
        try:
            error_message = {
                "chatID": chat_id,
                "text": "Desculpe, ocorreu um erro ao processar sua mensagem."
            }
            sendToTelegram(error_message)
        except:
            pass  
        raise

# Gera uma resposta HTTP padronizada para ser retornada
def create_response(status_code, message):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  
        },
        'body': json.dumps({
            'message': message
        })
    }
