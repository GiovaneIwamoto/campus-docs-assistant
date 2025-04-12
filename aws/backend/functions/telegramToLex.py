import json
import boto3
from dotenv import load_dotenv
from IntegrationFunctions.telegram_lex_integration import *  

load_dotenv()

lexruntime = boto3.client("lexv2-runtime")

# Main function that receives events from Telegram, processes the message, and interacts with Amazon Lex
def telegramToLex(event, context):
    try:
        print(f"[INFO] Event received: {event}")
        
        if not event.get('body'):
            raise ValueError("Event body is empty")
            
        try:
            body = json.loads(event['body'])
            print(f"[INFO] Request body processed: {body}")
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to decode JSON from body: {e}")
            raise
        
        # If it's a button interaction (callback_query), redirect to the corresponding function
        if 'callback_query' in body:
            return handle_callback_query(body)
        
        # If it's a text message, redirect to the corresponding function
        elif 'message' in body:
            return handle_text_message(body)
        
        else:
            raise ValueError("Unrecognized message format")
            
    except Exception as e:
        print(f"[ERROR] Error processing the event: {str(e)}")
        return create_response(400, 'Failed to process message')

# Processes button interactions on Telegram (callback_query)
def handle_callback_query(body):
    try:
        print("[INFO] Processing callback_query")
        callback_query = body['callback_query']
        chat_id = str(callback_query['message']['chat']['id']) 
        callback_data = callback_query['data'] 
        print(f"[INFO] Callback received. Chat ID: {chat_id}, Callback Data: {callback_data}")
        
        # Calls the function responsible for handling button interactions
        handle_button_interaction(callback_query, chat_id)
        
        return create_response(200, 'Successfully processed callback query')
        
    except Exception as e:
        print(f"[ERROR] Error processing callback query: {e}")
        
        # Attempts to send an error message to the user on Telegram
        try:
            error_message = {
                "chatID": chat_id,
                "text": "Sorry, an error occurred while processing your request."
            }
            sendToTelegram(error_message)
        except:
            pass  
        raise

# Processes text messages received by the bot on Telegram and sends Lex's response to the user
def handle_text_message(body):
    try:
        print("[INFO] Processing text message")
        message = body['message']
        
        if 'text' not in message:
            raise ValueError("Message does not contain text")
            
        chat_id = str(message['chat']['id'])  
        text = message['text'] 
        print(f"[INFO] Message received. Chat ID: {chat_id}, Text: {text}")
        
        # Sends the user's message to Amazon Lex and gets the response
        lex_response = recognizeTextWithLex(chat_id, text)
        print(f"[INFO] Lex response: {lex_response}")
        
        # Maps Lex's response to the format expected by Telegram
        messages_for_telegram = mapLexToTelegram(lex_response, body)
        print(f"[INFO] Messages mapped for Telegram: {messages_for_telegram}")
        
        # Sends each generated message to Telegram
        for msg in messages_for_telegram:
            sendToTelegram(msg)
        print("[INFO] Messages sent to Telegram")
        
        return create_response(200, 'Successfully processed text message')
        
    except Exception as e:
        print(f"[ERROR] Error processing text message: {e}")
        
        # Attempts to send an error message to the user on Telegram
        try:
            error_message = {
                "chatID": chat_id,
                "text": "Sorry, an error occurred while processing your message."
            }
            sendToTelegram(error_message)
        except:
            pass  
        raise

# Generates a standardized HTTP response to be returned
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
