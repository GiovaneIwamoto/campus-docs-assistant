from functions.telegramToLex import telegramToLex

# Definição das funções para o Serverless Framework
def telegramToLex_handler(event, context):
    return telegramToLex(event, context)