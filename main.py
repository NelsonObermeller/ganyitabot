import os
import openai
import telebot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

def traducir_mensaje(mensaje, origen):
    if origen == "user":
        prompt = f"Traduce este mensaje al ruso y al inglés, con tono amistoso:\n\n" + mensaje
    else:
        prompt = f"Traduce este mensaje al español y al inglés, con tono amistoso:\n\n" + mensaje

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un traductor amistoso y preciso."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    texto = message.text
    origen = "user" if message.from_user.username != "Wolfblita" else "ella"
    traduccion = traducir_mensaje(texto, origen)
    bot.send_message(message.chat.id, traduccion)

print("🤖 Bot iniciado... esperando mensajes.")
bot.infinity_polling()
