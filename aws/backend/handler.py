from functions.telegramToLex import telegramToLex

# Define functions for Serverless framework
def telegramToLex_handler(event, context):
    return telegramToLex(event, context)