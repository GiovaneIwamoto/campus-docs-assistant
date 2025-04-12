import os
import json
import boto3
import requests
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

lexruntime = boto3.client("lexv2-runtime")

# Function to recognize text using Lex
def recognize_text_with_lex(session_id, text):
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
        print(f"[ERROR] Error calling Lex: {e}")
        raise

# Unified function to handle button interactions
def handle_button_interaction(callback_query, chat_id):
    try:
        callback_data = callback_query.get("data", "")
        response_text = "Ask something" if callback_data == "I want to ask a question" else callback_data
        
        lex_response = recognize_text_with_lex(chat_id, response_text)
        
        messages = map_lex_to_telegram(lex_response, {
            "message": {
                "chat": {"id": chat_id}
            }
        })
        
        for message in messages:
            send_to_telegram(message)
            
    except Exception as e:
        print(f"[ERROR] Error handling button interaction: {e}")
        error_message = {
            "chatID": chat_id,
            "text": "Sorry, an error occurred while processing your request."
        }
        send_to_telegram(error_message)
        raise
    
# Function to map Lex responses to Telegram
def map_lex_to_telegram(lex_response, body):
    try:
        chat_id = str(body['message']['chat']['id'])
        messages = []
        
        if not isinstance(lex_response, dict):
            raise ValueError("Lex response is not in the expected format")
            
        lex_messages = lex_response.get('messages', [])
        if not lex_messages:
            return [{
                'chatID': chat_id,
                'text': 'Sorry, I did not get a valid response.'
            }]

        for lex_message in lex_messages:
            message = {
                'chatID': chat_id,
                'text': lex_message.get('content', 'Sorry, I did not understand your message')
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
        print(f"[ERROR] Error mapping Lex response to Telegram: {e}")
        raise

# Sends text messages to the Telegram chat
def send_to_telegram(message):
    try:
        token = os.getenv('TELEGRAM_TOKEN')
        if not token:
            raise ValueError("TELEGRAM_TOKEN not found in environment variables")
            
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
        print(f"[ERROR] Error in Telegram request: {e}")
        raise
    except Exception as e:
        print(f"[ERROR] Error sending message to Telegram: {e}")
        raise