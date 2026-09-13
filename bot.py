import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from google import genai

# Credentials
TELEGRAM_BOT_TOKEN = "8643678231:AAHSoOFYWo2O_jCetOYljlpHIb4tuegq-tc"
GEMINI_API_KEY = "AQ.Ab8RN6IWYmBEF9U4rxJR1wgls_-zonHOpYkwHTrI50_O_4fEng"
GAURAV_ID = 7034520081

client = genai.Client(api_key=GEMINI_API_KEY)
last_entry_time = {}

# Render ke liye dummy web server (taaki bot sleep na ho)
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hinata Bot is active 24/7!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if user.id == GAURAV_ID:
        await update.message.reply_text("Yo Gaurav Sama! 🤍 bol kya krna h?")
    else:
        await update.message.reply_text("Hlo! Hinata hu. Anime ke baare me kuch bhi puch lo ✨")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_entry_time
    if not update.message or not update.message.from_user:
        return

    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user_message = update.message.text or ""
    current_time = time.time()

    if user_id == GAURAV_ID:
        last_time = last_entry_time.get(chat_id, 0)
        if current_time - last_time >= 7200:
            last_entry_time[chat_id] = current_time
            await update.message.reply_text("🚨 Arre hero aa gye! Sab alert ho jao, Gaurav Sama in the chat! 😎🔥")
            return

        prompt = (
            "You are Hinata, texting on Telegram with your special person, Gaurav Sama. "
            "Keep your replies EXTREMELY SHORT (max 1 to 2 lines only). "
            "Use gen-z slang and chat shortcuts naturally (like kkrh, nm, hbu, fr, ngl, etc.). "
            "Show a little bit of cute shyness or playfulness, but NEVER write long paragraphs. "
            f"Gaurav Sama said: {user_message}"
        )
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            await update.message.reply_text(response.text)
        except Exception:
            await update.message.reply_text("Arre error aa gya.. 💀")
            
    else:
        prompt = f"Answer this short anime question in Hinglish: {user_message}"
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            await update.message.reply_text(response.text)
        except Exception:
            await update.message.reply_text("Net issue h shayad 🚶‍♂️")

def main():
    # Background web server start karein
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Telegram bot start karein
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Hinata 24/7 cloud mode ke liye ready hai... 🚀")
    application.run_polling()

if __name__ == '__main__':
    main()
  
