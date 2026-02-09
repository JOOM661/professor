import os
import json
import telebot
from telebot import types

# Configuração do Token via variável de ambiente
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Nome da pasta onde os progressos serão salvos
DATA_FOLDER = "user_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# --- BANCO DE DADOS DE AULAS ---
AULAS = [
    {
        "titulo": "01. O que é Programação?",
        "conteudo": "Programar é dar instruções para o computador resolver problemas. É como escrever uma receita de bolo!",
        "exemplo": "print('Olá Mundo!')",
        "resumo": "Programar = Instruções."
    },
    {
        "titulo": "02. Variáveis (Gavetas)",
        "conteudo": "Variáveis guardam informações. Imagine que cada variável é uma gaveta com um nome.",
        "exemplo": "nome = 'Alice'\nidade = 25",
        "resumo": "Variáveis armazenam dados."
    },
    {
        "titulo": "03. Números e Cálculos",
        "conteudo": "O Python é ótimo com matemática. Você pode somar (+), subtrair (-), multiplicar (*) e dividir (/).",
        "exemplo": "soma = 10 + 5",
        "resumo": "Python funciona como uma calculadora poderosa."
    },
    {
        "titulo": "04. Strings (Textos)",
        "conteudo": "Textos no código são chamados de Strings e devem estar entre aspas.",
        "exemplo": "frase = 'Eu amo programar!'",
        "resumo": "Texto = String (sempre entre aspas)."
    },
    {
        "titulo": "05. Listas",
        "conteudo": "Listas servem para guardar vários itens em um só lugar, usando colchetes [ ].",
        "exemplo": "compras = ['pão', 'leite', 'café']",
        "resumo": "Listas organizam múltiplos dados."
    },
    {
        "titulo": "06. Entrada de Dados",
        "conteudo": "O comando input() serve para o computador perguntar algo ao usuário.",
        "exemplo": "nome = input('Qual seu nome?')",
        "resumo": "input() recebe o que o usuário digita."
    },
    {
        "titulo": "07. Condicionais (Se/Então)",
        "conteudo": "O 'if' serve para o computador tomar decisões baseadas em condições.",
        "exemplo": "if idade >= 18:\n    print('Maior de idade')",
        "resumo": "if testa se algo é verdadeiro."
    },
    {
        "titulo": "08. O 'Else'",
        "conteudo": "O 'else' é o caminho alternativo caso o 'if' não seja atendido.",
        "exemplo": "if nota >= 6:\n    print('Passou')\nelse:\n    print('Recuperação')",
        "resumo": "else = 'caso contrário'."
    },
    {
        "titulo": "09. Operadores Lógicos",
        "conteudo": "Usamos 'and' (e) e 'or' (ou) para combinar várias condições.",
        "exemplo": "if sol == True and calor == True:\n    print('Praia!')",
        "resumo": "and/or combinam testes lógicos."
    },
    {
        "titulo": "10. Repetição (While)",
        "conteudo": "O 'while' repete um bloco de código enquanto uma condição for verdadeira.",
        "exemplo": "while energia > 0:\n    print('Correndo...')",
        "resumo": "while = repetição por condição."
    },
    {
        "titulo": "11. Repetição (For)",
        "conteudo": "O 'for' é usado para percorrer itens de uma lista ou uma sequência.",
        "exemplo": "for item in lista:\n    print(item)",
        "resumo": "for = repetição por coleção."
    },
    {
        "titulo": "12. Funções",
        "conteudo": "Funções são blocos de código que você cria para usar várias vezes depois.",
        "exemplo": "def saudar():\n    print('Olá!')",
        "resumo": "def cria funções reutilizáveis."
    },
    {
        "titulo": "13. Parâmetros",
        "conteudo": "Funções podem receber valores para trabalhar, chamamos de parâmetros.",
        "exemplo": "def soma(a, b):\n    return a + b",
        "resumo": "Parâmetros são os dados que a função recebe."
    },
    {
        "titulo": "14. Dicionários",
        "conteudo": "Dicionários guardam dados com um sistema de 'Chave: Valor'.",
        "exemplo": "carro = {'marca': 'Ford', 'ano': 2020}",
        "resumo": "Dicionários ligam nomes a valores."
    },
    {
        "titulo": "15. Erros e Exceções",
        "conteudo": "Erros acontecem! Usamos try/except para capturar erros e não deixar o programa travar.",
        "exemplo": "try:\n    print(10/0)\nexcept:\n    print('Erro detectado!')",
        "resumo": "Tratamento de erros evita quedas."
    },
    {
        "titulo": "16. Importando Módulos",
        "conteudo": "Podemos usar códigos prontos de outros desenvolvedores usando 'import'.",
        "exemplo": "import math\nprint(math.sqrt(16))",
        "resumo": "import traz novas ferramentas."
    },
    {
        "titulo": "17. Manipulação de Arquivos",
        "conteudo": "Python pode ler e escrever arquivos de texto no seu computador.",
        "exemplo": "open('texto.txt', 'w').write('Oi!')",
        "resumo": "Python interage com o sistema de arquivos."
    },
    {
        "titulo": "18. Comentários",
        "conteudo": "Comentários são textos que o computador ignora, servem para explicar o código aos humanos.",
        "exemplo": "# Isso é um comentário",
        "resumo": "# ajuda a documentar o código."
    },
    {
        "titulo": "19. Formatação de Strings",
        "conteudo": "As f-strings facilitam colocar variáveis dentro de frases.",
        "exemplo": "f'Olá, meu nome é {nome}'",
        "resumo": "f-strings tornam o texto dinâmico."
    },
    {
        "titulo": "20. Boas Práticas (Clean Code)",
        "conteudo": "Escrever código limpo é essencial. Use nomes claros para variáveis e mantenha a organização.",
        "exemplo": "nome_do_usuario = 'Joao' # Bom!",
        "resumo": "Código limpo = fácil manutenção."
    }
]

# --- FUNÇÕES DE PERSISTÊNCIA ---

def get_user_path(user_id):
    return os.path.join(DATA_FOLDER, f"{user_id}.json")

def load_progress(user_id):
    path = get_user_path(user_id)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {"aula_atual": 0}

def save_progress(user_id, data):
    path = get_user_path(user_id)
    with open(path, 'w') as f:
        json.dump(data, f)

# --- COMANDOS DO BOT ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    # Garante que os dados existem sem KeyErrors
    progress = load_progress(user_id)
    save_progress(user_id, progress)

    welcome_text = (
        f"Olá, {message.from_user.first_name}! 📘✨\n\n"
        "Eu sou seu Professor Virtual de Programação. "
        "Estou aqui para te ensinar Python do zero, de um jeito simples e prático.\n\n"
        "Use /menu para ver o que posso fazer!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['menu'])
def send_menu(message):
    menu_text = (
        "🎓 *Menu do Aluno:*\n\n"
        "/aula - Ver minha aula atual\n"
        "/proxima - Ir para o próximo tópico\n"
        "/ajuda - Suporte do professor"
    )
    bot.reply_to(message, menu_text, parse_mode="Markdown")

@bot.message_handler(commands=['aula'])
def show_lesson(message):
    user_id = str(message.from_user.id)
    progress = load_progress(user_id)
    idx = progress.get("aula_atual", 0)

    if idx < len(AULAS):
        aula = AULAS[idx]
        texto_aula = (
            f"📖 *{aula['titulo']}*\n\n"
            f"{aula['conteudo']}\n\n"
            f"💻 *Exemplo Prático:*\n`{aula['exemplo']}`\n\n"
            f"📌 *Resumo:* {aula['resumo']}\n\n"
            "Digite /proxima para continuar sua jornada! 🚀"
        )
        bot.reply_to(message, texto_aula, parse_mode="Markdown")
    else:
        bot.reply_to(message, "🎉 Parabéns! Você concluiu todas as aulas do curso básico!")

@bot.message_handler(commands=['proxima'])
def next_lesson(message):
    user_id = str(message.from_user.id)
    progress = load_progress(user_id)
    idx = progress.get("aula_atual", 0)

    if idx < len(AULAS) - 1:
        progress["aula_atual"] = idx + 1
        save_progress(user_id, progress)
        bot.reply_to(message, "Excelente progresso! 🌟 Vamos para a próxima aula.")
        show_lesson(message)
    else:
        bot.reply_to(message, "Você já chegou ao fim do curso! Que tal revisar o que aprendeu? 😊")

@bot.message_handler(commands=['ajuda'])
def help_command(message):
    bot.reply_to(message, "Eu explico conceitos de programação de forma simples. Se tiver dúvidas, tente reler o exemplo prático da aula!")

# Fallback para mensagens de texto comuns
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.reply_to(message, "Não entendi... 😅 Tente usar /menu para ver os comandos disponíveis.")

# --- INICIALIZAÇÃO ---
if __name__ == "__main__":
    print("Professor Virtual está online... (Aguardando conexões)")
    # Non-stop polling para o bot não parar em caso de erro de conexão
    bot.infinity_polling()
