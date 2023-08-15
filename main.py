import telebot
import openai
import traceback
import time

# Configurar a chave da API da OpenAI
openai.api_key = 'TOKEN_OPENAI'

# Configurar o token do seu bot do Telegram
telegram_token = 'TOKEN_TELEGRAM_BOT'

# Lista de IDs de usuário autorizados (whitelist)
authorized_user_ids = [1002372394, 1233147394, 937292394]  # Adicione IDs de usuário permitidos aqui separados por virgula

# Inicializar o bot
bot = telebot.TeleBot(telegram_token)

# Verificar se o usuário está autorizado
def is_authorized_user(user_id):
    return user_id in authorized_user_ids

# Comando para iniciar o bot
@bot.message_handler(commands=['start'])
def start(message):
    if is_authorized_user(message.from_user.id):
        bot.reply_to(
            message,
            'Olá! Como posso ajudar?')
    else:
        bot.reply_to(
            message,
            'Desculpe, você não tem permissão para acessar este bot.')

# Responder às mensagens do usuário
@bot.message_handler(func=lambda message: is_authorized_user(message.from_user.id))
def respond_to_message(message):
    try:
        user_message = message.text
        response = openai.Completion.create(
            engine="text-davinci-003",  # Usar o mecanismo GPT-3
            prompt=user_message,
            max_tokens=2049  # Definir o número de tokens na resposta gerada
        )
        bot_response = response.choices[0].text.strip()
        bot.reply_to(message, bot_response)
    except Exception as e:
        error_message = f"Desculpe, algo deu errado. O erro foi: {str(e)}"
        bot.reply_to(message, error_message)
        traceback.print_exc()

while True:
    try:
        # Iniciar o bot
        bot.polling()

    except Exception as e:
        # Imprimir o erro e reiniciar após 1 segundos
        print("Erro encontrado:", e)
        traceback.print_exc()
        time.sleep(1)  # Aguardar 1 segundos antes de reiniciar
