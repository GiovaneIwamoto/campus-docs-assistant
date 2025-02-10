import os
import json
import boto3
import requests
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

lexruntime = boto3.client("lexv2-runtime")

# Função para reconhecer texto usando Lex
def recognizeTextWithLex(session_id, text):
    try:
        response = lexruntime.recognize_text(
            botId=os.getenv('LEX_BOT_ID'),
            botAliasId=os.getenv('LEX_BOT_ALIAS_ID'),
            localeId='en_US',
            sessionId=session_id,
            text=text
        )
        return response
    except Exception as e:
        print(f"[ERROR] Erro ao chamar o Lex: {e}")
        raise

# Função unificada para lidar com interações dos botões
def handle_button_interaction(callback_query, chat_id):
    try:
        callback_data = callback_query.get("data", "")
        response_text = "Pergunte algo" if callback_data == "Quero fazer uma pergunta" else callback_data
        
        lex_response = recognizeTextWithLex(chat_id, response_text)
        
        messages = mapLexToTelegram(lex_response, {
            "message": {
                "chat": {"id": chat_id}
            }
        })
        
        for message in messages:
            sendToTelegram(message)
            
    except Exception as e:
        print(f"[ERROR] Erro ao tratar a interação com botão: {e}")
        error_message = {
            "chatID": chat_id,
            "text": "Desculpe, ocorreu um erro ao processar sua solicitação."
        }
        sendToTelegram(error_message)
        raise
    
# Função para mapear respostas do Lex para o Telegram
def mapLexToTelegram(lex_response, body):
    try:
        chatID = str(body['message']['chat']['id'])
        messages = []
        
        if not isinstance(lex_response, dict):
            raise ValueError("Resposta do Lex não está no formato esperado")
            
        lex_messages = lex_response.get('messages', [])
        if not lex_messages:
            return [{
                'chatID': chatID,
                'text': 'Desculpe, não obtive uma resposta válida.'
            }]

        for lex_message in lex_messages:
            message = {
                'chatID': chatID,
                'text': lex_message.get('content', 'Desculpe, não entendi sua mensagem')
            }

            response_card = lex_message.get('imageResponseCard')
            if response_card:
                buttons = []
                for button in response_card.get('buttons', []):
                    if isinstance(button, dict) and 'text' in button and 'value' in button:
                        buttons.append(
                            InlineKeyboardButton(button['text'], callback_data=button['value'])
                        )
                
                if buttons:
                    message['reply_markup'] = InlineKeyboardMarkup([buttons])  
                    message['text'] = response_card.get('title', message['text'])

            messages.append(message)

        return messages
    except Exception as e:
        print(f"[ERROR] Erro ao mapear resposta do Lex para Telegram: {e}")
        raise

# Envia mensagens de texto para o chat do Telegram
def sendToTelegram(message):
    try:
        token = os.getenv('TELEGRAM_TOKEN')
        if not token:
            raise ValueError("TELEGRAM_TOKEN não encontrado nas variáveis de ambiente")
            
        telegram_url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {
            'chat_id': message['chatID'],
            'text': message['text']
        }

        if message.get('reply_markup'):
            payload['reply_markup'] = json.dumps(message['reply_markup'].to_dict())

        response = requests.post(telegram_url, json=payload)
        response.raise_for_status() 
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Erro na requisição ao Telegram: {e}")
        raise
    except Exception as e:
        print(f"[ERROR] Erro ao enviar mensagem ao Telegram: {e}")
        raise