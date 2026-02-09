import os
import json
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
DATA_FOLDER = "user_data"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# --- WEB SERVER (FLASK) ---
app = Flask(__name__)

@app.route('/')
def home():
    # HTML com CSS moderno para um visual "bonitão"
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Professor Virtual Status</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .card { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; border-top: 5px solid #0088cc; }
            .status-dot { height: 15px; width: 15px; background-color: #2ecc71; border-radius: 50%; display: inline-block; margin-right: 5px; animation: pulse 2s infinite; }
            h1 { color: #333; margin-bottom: 10px; }
            p { color: #666; font-size: 1.1rem; }
            .info { background: #eef9ff; padding: 10px; border-radius: 8px; color: #0088cc; font-weight: bold; margin-top: 20px; }
            @keyframes pulse { 0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7); } 70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(46, 204, 113, 0); } 100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); } }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Professor Virtual 🤖</h1>
            <p><span class="status-dot"></span> Sistema Online e Operacional</p>
            <div class="info">Conectado ao Telegram via pyTelegramBotAPI</div>
            <p style="font-size: 0.8rem; color: #999; margin-top: 20px;">O bot está processando mensagens em segundo plano.</p>
        </div>
    </body>
    </html>
    """

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- BANCO DE DADOS DE AULAS ---
AULAS = [
    {"titulo": "01. O que é Programação?", "conteudo": "Programar é dar instruções para o computador resolver problemas.", "exemplo": "print('Olá Mundo!')", "resumo": "Programar = Instruções."},
    {"titulo": "02. Variáveis", "conteudo": "Variáveis guardam informações como gavetas etiquetadas.", "exemplo": "nome = 'Alice'", "resumo": "Variáveis = Armazenamento."},
    # ... (As outras aulas seguem a mesma estrutura do código anterior)
    {"titulo": "20. Boas Práticas", "conteudo": "Escreva código limpo para que outros entendam.", "exemplo": "nome_usuario = 'Leo'", "resumo": "Organização é tudo."}
]

# --- LÓGICA DO BOT ---

def load_progress(user_id):
    path = os.path.join(DATA_FOLDER, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, 'r') as f: return json.load(f)
    return {"aula_atual": 0}

def save_progress(user_id, data):
    with open(os.path.join(DATA_FOLDER, f"{user_id}.json"), 'w') as f: json.dump(data, f)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    save_progress(user_id, load_progress(user_id))
    bot.reply_to(message, "Olá! 📘✨ Eu sou seu Professor de Python. Use /menu para começar!")

@bot.message_handler(commands=['menu'])
def send_menu(message):
    bot.reply_to(message, "🎓 *Menu:*\n/aula - Ver aula\n/proxima - Próxima aula", parse_mode="Markdown")

@bot.message_handler(commands=['aula'])
def show_lesson(message):
    user_id = str(message.from_user.id)
    progress = load_progress(user_id)
    idx = progress["aula_atual"]
    if idx < len(AULAS):
        aula = AULAS[idx]
        msg = f"📖 *{aula['titulo']}*\n\n{aula['conteudo']}\n\n💻 ` {aula['exemplo']} `\n\n📌 {aula['resumo']}"
        bot.reply_to(message, msg, parse_mode="Markdown")
    else:
        bot.reply_to(message, "🎉 Você concluiu tudo!")

@bot.message_handler(commands=['proxima'])
def next_lesson(message):
    user_id = str(message.from_user.id)
    progress = load_progress(user_id)
    if progress["aula_atual"] < len(AULAS) - 1:
        progress["aula_atual"] += 1
        save_progress(user_id, progress)
        show_lesson(message)
    else:
        bot.reply_to(message, "Fim do curso! 🎓")

# --- EXECUÇÃO EM PARALELO ---
if __name__ == "__main__":
    # Inicia o Flask em uma thread separada
    t = Thread(target=run_flask)
    t.start()
    
    print("Servidor Web e Bot iniciados!")
    bot.infinity_polling()
