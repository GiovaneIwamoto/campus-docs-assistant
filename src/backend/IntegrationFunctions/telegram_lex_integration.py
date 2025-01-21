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
        print(f"[INFO] Iniciando reconhecimento de texto no Lex. Session ID: {session_id}, Texto: {text}")
        response = lexruntime.recognize_text(
            botId=os.getenv('LEX_BOT_ID'),
            botAliasId=os.getenv('LEX_BOT_ALIAS_ID'),
            localeId='en_US',
            sessionId=session_id,
            text=text
        )
        print(f"[SUCCESS] Resposta do Lex: {response}")
        return response
    except Exception as e:
        print(f"[ERROR] Erro ao chamar o Lex: {e}")
        raise

# Função para mapear mensagens de texto do Telegram para o Lex
def mapTelegramToLex(body):
    try:
        print(f"[INFO] Mapeando mensagem do Telegram para Lex. Body: {body}")
        chatID = str(body['message']['chat']['id'])
        message = body['message']['text']
        mapping = {
            'inputText': message,
            'userId': chatID,
            'sessionAttributes': {}
        }
        print(f"[INFO] Mapeamento concluído. Resultado: {mapping}")
        return mapping
    except KeyError as e:
        print(f"[ERROR] Chave ausente ao mapear mensagem do Telegram: {e}")
        raise
    except Exception as e:
        print(f"[ERROR] Erro inesperado ao mapear mensagem do Telegram: {e}")
        raise

# Função para mapear mensagens do Lex para o Telegram
def mapLexToTelegram(lex_response, body):
    try:
        print(f"[INFO] Mapeando resposta do Lex para Telegram. Lex Response: {lex_response}, Body: {body}")
        chatID = str(body['message']['chat']['id'])
        messages = []

        if 'messages' in lex_response:
            for lex_message in lex_response['messages']:
                message = {
                    'chatID': chatID,
                    'text': lex_message.get('content', 'Desculpe, não entendi sua mensagem')
                }
                response_card = lex_message.get('imageResponseCard')
                if response_card:
                    buttons = [
                        InlineKeyboardButton(button['text'], callback_data=button['value'])
                        for button in response_card.get('buttons', [])
                    ]
                    if buttons:
                        message['reply_markup'] = InlineKeyboardMarkup.from_column(buttons)
                        message['text'] = response_card.get('title', 'Menu de opções')

                messages.append(message)

        print(f"[INFO] Mapeamento concluído. Mensagens para o Telegram: {messages}")
        return messages
    except Exception as e:
        print(f"[ERROR] Erro ao mapear resposta do Lex para Telegram: {e}")
        raise

# Processa a resposta do Lex e envia para o Telegram
def processLexResponse(body, session_id, text):
    try:
        print(f"[INFO] Processando resposta do Lex. Session ID: {session_id}, Texto: {text}, Body: {body}")
        lexResponse = recognizeTextWithLex(session_id, text)
        print(f"[INFO] Resposta do Lex recebida. Iniciando mapeamento para Telegram.")
        messagesForTelegram = mapLexToTelegram(lexResponse, body)

        for message in messagesForTelegram:
            print(f"[INFO] Enviando mensagem ao Telegram: {message}")
            sendToTelegram(message)
        print(f"[SUCCESS] Todas as mensagens foram enviadas com sucesso.")
    except Exception as e:
        print(f"[ERROR] Erro ao processar resposta do Lex: {e}")
        raise

def handleCallbackQuery(callback_query, chat_id, callback_data):
    print(f"[INFO] Recebido callback query. Callback Data: {callback_data}, Chat ID: {chat_id}")
    pass

# Envia mensagens de texto para o chat do Telegram
def sendToTelegram(message):
    try:
        print(f"[INFO] Preparando para enviar mensagem ao Telegram. Mensagem: {message}")
        token = os.getenv('TELEGRAM_TOKEN')
        telegram_url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {
            'chat_id': message['chatID'],
            'text': message['text']
        }

        if message.get('reply_markup'):
            payload['reply_markup'] = json.dumps(message['reply_markup'].to_dict())

        print(f"[DEBUG] Payload a ser enviado ao Telegram: {payload}")
        response = requests.post(telegram_url, json=payload)
        print(f"[INFO] Resposta do Telegram: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"[ERROR] Erro ao enviar mensagem ao Telegram: {e}")
        raise
