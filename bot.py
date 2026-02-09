import os
import json
import telebot
from telebot import types
from flask import Flask
from threading import Thread
import time

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
DATA_FOLDER = "user_data"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# --- WEB SERVER (FLASK - DASHBOARD) ---
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Professor Virtual Status</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .card { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; border-top: 5px solid #0088cc; max-width: 400px; width: 90%; }
            .status-dot { height: 15px; width: 15px; background-color: #2ecc71; border-radius: 50%; display: inline-block; margin-right: 5px; animation: pulse 2s infinite; }
            h1 { color: #333; margin-bottom: 10px; font-size: 1.5rem; }
            p { color: #666; font-size: 1rem; }
            .info { background: #eef9ff; padding: 10px; border-radius: 8px; color: #0088cc; font-weight: bold; margin-top: 20px; font-size: 0.9rem; }
            @keyframes pulse { 0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7); } 70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(46, 204, 113, 0); } 100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); } }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Professor Virtual 🤖</h1>
            <p><span class="status-dot"></span> Sistema Online</p>
            <div class="info">Curso Completo de Python<br>(50 Aulas Carregadas)</div>
            <p style="font-size: 0.8rem; color: #999; margin-top: 20px;">Bot rodando 24/7 via Threading</p>
        </div>
    </body>
    </html>
    """

def run_flask():
    # Roda o servidor na porta 8080 (padrão Replit)
    app.run(host='0.0.0.0', port=8080)

# --- CURRÍCULO COMPLETO (50 AULAS) ---
AULAS = [
    # MÓDULO 1: O BÁSICO
    {"titulo": "01. Bem-vindo ao Python", "conteudo": "Python é uma linguagem poderosa e fácil de ler. Programar é dar ordens ao computador.", "exemplo": "print('Olá, Mundo!')", "resumo": "print() mostra mensagens na tela."},
    {"titulo": "02. Variáveis (Gavetas)", "conteudo": "Variáveis guardam dados na memória. É como dar um nome a um valor.", "exemplo": "nome = 'Ana'\nidade = 25", "resumo": "Variáveis armazenam valores."},
    {"titulo": "03. Tipos de Dados: Texto", "conteudo": "Textos são chamados de 'Strings' e sempre usam aspas.", "exemplo": "frase = 'Eu gosto de Python'", "resumo": "String (str) = Texto."},
    {"titulo": "04. Tipos de Dados: Inteiros", "conteudo": "Números inteiros não têm vírgula ou ponto.", "exemplo": "ano = 2024", "resumo": "Integer (int) = Número inteiro."},
    {"titulo": "05. Tipos de Dados: Flutuantes", "conteudo": "Números com ponto decimal são chamados de 'floats'.", "exemplo": "preco = 19.99", "resumo": "Float = Número quebrado."},
    {"titulo": "06. Tipos de Dados: Booleanos", "conteudo": "Só existem dois valores: True (Verdadeiro) e False (Falso).", "exemplo": "ligado = True", "resumo": "Bool = Lógica binária."},
    {"titulo": "07. Comentários", "conteudo": "O Python ignora tudo que vem depois de #. Serve para anotar o código.", "exemplo": "# Isso não roda\nprint('Isso roda')", "resumo": "# cria anotações."},
    {"titulo": "08. Matemática Básica", "conteudo": "Python faz contas: soma (+), subtração (-), multiplicação (*) e divisão (/).", "exemplo": "resultado = 10 * 2", "resumo": "Python é uma calculadora."},
    {"titulo": "09. Potência e Resto", "conteudo": "** é potência e % é o resto da divisão.", "exemplo": "qua = 5 ** 2  # 25\nresto = 10 % 3  # 1", "resumo": "** eleva, % pega a sobra."},
    {"titulo": "10. Entrada de Dados", "conteudo": "input() pausa o programa e espera o usuário digitar algo.", "exemplo": "nome = input('Seu nome: ')", "resumo": "input() recebe dados."},
    
    # MÓDULO 2: CONTROLE DE FLUXO
    {"titulo": "11. Convertendo Tipos", "conteudo": "O input sempre devolve texto. Para contas, converta com int() ou float().", "exemplo": "idade = int(input('Idade: '))", "resumo": "Converta strings para calcular."},
    {"titulo": "12. Condicional IF", "conteudo": "O 'if' executa um bloco APENAS se a condição for verdadeira.", "exemplo": "if sol:\n    print('Praia!')", "resumo": "if = Se..."},
    {"titulo": "13. Indentação", "conteudo": "Em Python, os espaços no início da linha definem o que está dentro do 'if'.", "exemplo": "if True:\n    print('Dentro')\nprint('Fora')", "resumo": "Use 4 espaços (TAB)."},
    {"titulo": "14. Condicional ELSE", "conteudo": "O 'else' roda se o 'if' falhar.", "exemplo": "if rico:\n    compra()\nelse:\n    trabalha()", "resumo": "else = Senão..."},
    {"titulo": "15. Condicional ELIF", "conteudo": "Use 'elif' para testar várias condições em sequência.", "exemplo": "if a > b:\n    ...\nelif a == b:\n    ...\nelse:\n    ...", "resumo": "elif = Senão se..."},
    {"titulo": "16. Comparadores", "conteudo": "Maior (>), Menor (<), Igual (==), Diferente (!=).", "exemplo": "if senha == '123':\n    entrar()", "resumo": "== compara igualdade."},
    {"titulo": "17. Operador AND", "conteudo": "Retorna True apenas se AS DUAS coisas forem verdadeiras.", "exemplo": "if sol and dinheiro:\n    viajar()", "resumo": "and = E exigente."},
    {"titulo": "18. Operador OR", "conteudo": "Retorna True se PELO MENOS UMA coisa for verdadeira.", "exemplo": "if feriado or domingo:\n    descansar()", "resumo": "or = Ou flexível."},
    {"titulo": "19. Operador NOT", "conteudo": "Inverte o valor. True vira False e vice-versa.", "exemplo": "if not chuva:\n    sair()", "resumo": "not = Inversão."},
    
    # MÓDULO 3: ESTRUTURAS DE DADOS
    {"titulo": "20. Listas (Arrays)", "conteudo": "Listas guardam vários itens ordenados entre colchetes [].", "exemplo": "frutas = ['maçã', 'uva']", "resumo": "Lista = Coleção ordenada."},
    {"titulo": "21. Acessando Listas", "conteudo": "O primeiro item é o índice 0.", "exemplo": "print(frutas[0]) # maçã", "resumo": "Contagem começa no 0."},
    {"titulo": "22. Adicionando na Lista", "conteudo": ".append() coloca um item no final da lista.", "exemplo": "lista.append('Novo')", "resumo": "append() adiciona."},
    {"titulo": "23. Removendo da Lista", "conteudo": ".pop() remove o último item ou um índice específico.", "exemplo": "lista.pop()", "resumo": "pop() remove."},
    {"titulo": "24. Tamanho da Lista", "conteudo": "len() conta quantos itens existem.", "exemplo": "total = len(lista)", "resumo": "len() mede tamanho."},
    {"titulo": "25. Tuplas", "conteudo": "Parecidas com listas, mas usam parênteses () e NÃO podem mudar.", "exemplo": "cores = ('red', 'blue')", "resumo": "Tuplas são imutáveis."},
    {"titulo": "26. Sets (Conjuntos)", "conteudo": "Usam chaves {}, não têm ordem e não aceitam repetidos.", "exemplo": "unicos = {1, 2, 2, 3} # vira {1, 2, 3}", "resumo": "Sets eliminam duplicatas."},
    {"titulo": "27. Dicionários", "conteudo": "Guardam pares Chave:Valor entre chaves {}.", "exemplo": "user = {'nome': 'Leo', 'idade': 30}", "resumo": "Dicionário = Mapa de dados."},
    {"titulo": "28. Acessando Dicionários", "conteudo": "Acesse o valor usando a chave.", "exemplo": "print(user['nome'])", "resumo": "Chave busca Valor."},
    
    # MÓDULO 4: LAÇOS DE REPETIÇÃO
    {"titulo": "29. Loop WHILE", "conteudo": "Repete enquanto a condição for verdadeira. Cuidado com loops infinitos!", "exemplo": "x = 0\nwhile x < 5:\n    print(x)\n    x += 1", "resumo": "While = Repetição condicional."},
    {"titulo": "30. Loop FOR (Listas)", "conteudo": "Percorre cada item de uma coleção.", "exemplo": "for fruta in frutas:\n    print(fruta)", "resumo": "For varre coleções."},
    {"titulo": "31. Função RANGE", "conteudo": "Gera uma sequência de números.", "exemplo": "for i in range(5):\n    print(i) # 0 a 4", "resumo": "range(n) cria contadores."},
    {"titulo": "32. Break", "conteudo": "Para o loop imediatamente.", "exemplo": "if x == 5:\n    break", "resumo": "break quebra o loop."},
    {"titulo": "33. Continue", "conteudo": "Pula a volta atual e vai para a próxima.", "exemplo": "if x == 2:\n    continue", "resumo": "continue pula etapa."},
    
    # MÓDULO 5: FUNÇÕES E MÉTODOS
    {"titulo": "34. Criando Funções", "conteudo": "def cria um bloco de código reutilizável.", "exemplo": "def oi():\n    print('Oi')", "resumo": "def define função."},
    {"titulo": "35. Parâmetros", "conteudo": "Dados que a função precisa para trabalhar.", "exemplo": "def dobro(x):\n    print(x * 2)", "resumo": "Parâmetros são inputs da função."},
    {"titulo": "36. Return", "conteudo": "Devolve um valor para quem chamou a função.", "exemplo": "def soma(a,b):\n    return a+b", "resumo": "return exporta o resultado."},
    {"titulo": "37. Métodos de String: Maiúscula", "conteudo": ".upper() deixa tudo maiúsculo.", "exemplo": "texto.upper()", "resumo": "Manipulação de texto."},
    {"titulo": "38. Métodos de String: Substituir", "conteudo": ".replace(antigo, novo) troca partes do texto.", "exemplo": "txt.replace('a', '@')", "resumo": "replace troca caracteres."},
    {"titulo": "39. Métodos de String: Fatiar", "conteudo": "Podemos pegar pedaços do texto.", "exemplo": "texto[0:3] # Pega 3 letras", "resumo": "Slicing corta strings."},
    {"titulo": "40. F-Strings", "conteudo": "O jeito moderno de formatar texto com variáveis.", "exemplo": "f'Olá {nome}'", "resumo": "f antes das aspas."},
    
    # MÓDULO 6: AVANÇADO E MÓDULOS
    {"titulo": "41. Importar Módulos", "conteudo": "Bibliotecas externas expandem o Python.", "exemplo": "import math\nprint(math.pi)", "resumo": "import traz superpoderes."},
    {"titulo": "42. Módulo Random", "conteudo": "Gera números aleatórios.", "exemplo": "import random\nprint(random.randint(1, 10))", "resumo": "Sorteios e aleatoriedade."},
    {"titulo": "43. Módulo Datetime", "conteudo": "Lida com datas e horas.", "exemplo": "from datetime import datetime\nhoje = datetime.now()", "resumo": "Controle de tempo."},
    {"titulo": "44. Try / Except", "conteudo": "Evita que o programa crashe se der erro.", "exemplo": "try:\n    x = 1/0\nexcept:\n    print('Erro')", "resumo": "Tratamento de exceções."},
    {"titulo": "45. Manipulando Arquivos (Leitura)", "conteudo": "Lendo arquivos de texto.", "exemplo": "with open('t.txt', 'r') as f:\n    ler = f.read()", "resumo": "'r' para ler (read)."},
    {"titulo": "46. Manipulando Arquivos (Escrita)", "conteudo": "Escrevendo em arquivos.", "exemplo": "with open('t.txt', 'w') as f:\n    f.write('Oi')", "resumo": "'w' para escrever (write)."},
    {"titulo": "47. Classes (OOP)", "conteudo": "O molde para criar objetos.", "exemplo": "class Carro:\n    pass", "resumo": "Classe é a planta."},
    {"titulo": "48. Objetos", "conteudo": "A coisa criada a partir da classe.", "exemplo": "meu_carro = Carro()", "resumo": "Objeto é a construção."},
    {"titulo": "49. O __init__", "conteudo": "A função construtora que roda ao criar o objeto.", "exemplo": "def __init__(self, cor):\n    self.cor = cor", "resumo": "Configuração inicial."},
    {"titulo": "50. Conclusão", "conteudo": "Parabéns! Você viu os pilares do Python. Agora é praticar projetos reais!", "exemplo": "print('Sou Programador!')", "resumo": "O fim é apenas o começo!"}
]

# --- LÓGICA DO BOT ---

def get_user_path(user_id):
    return os.path.join(DATA_FOLDER, f"{user_id}.json")

def load_progress(user_id):
    path = get_user_path(user_id)
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return data
        except:
            return {"aula_atual": 0}
    return {"aula_atual": 0}

def save_progress(user_id, data):
    path = get_user_path(user_id)
    with open(path, 'w') as f:
        json.dump(data, f)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    progress = load_progress(user_id) # Garante que arquivo existe
    save_progress(user_id, progress)
    
    bot.reply_to(message, 
        f"Olá, {message.from_user.first_name}! 🐍\n\n"
        "Eu sou seu Professor de Python Completo.\n"
        "Temos **50 Aulas** preparadas para você!\n\n"
        "Use /menu para ver os comandos."
    )

@bot.message_handler(commands=['menu'])
def send_menu(message):
    user_id = str(message.from_user.id)
    progress = load_progress(user_id)
    atual = progress.get('aula_atual', 0) + 1
    
    bot.reply_to(message, 
        f"🎓 *Menu do Aluno*\n\n"
        f"Você está na aula: {atual}/50\n\n"
        "/aula - Ler conteúdo atual\n"
        "/proxima - Avançar\n"
        "/voltar - Revisar anterior\n"
        "/resetar - Começar do zero",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['aula'])
def show_lesson(message):
    user_id = str(message.from_user.id)
    progress = load_progress(user_id)
    idx = progress.get("aula_atual", 0)

    if 0 <= idx < len(AULAS):
        aula = AULAS[idx]
        msg = (
            f"📖 *{aula['titulo']}*\n\n"
            f"{aula['conteudo']}\n\n"
            f"💻 *Exemplo:*\n`{aula['exemplo']}`\n\n"
            f"📌 *Nota:* {aula['resumo']}\n\n"
            f"Use /proxima para avançar! 🚀"
        )
        bot.reply_to(message, msg, parse_mode="Markdown")
    else:
        bot.reply_to(message, "🎉 Você concluiu o curso completo! Parabéns!")

@bot.message_handler(commands=['proxima'])
def next_lesson(message):
    user_id = str(message.from_user.id)
    progress = load_progress(user_id)
    idx = progress.get("aula_atual", 0)

    if idx < len(AULAS) - 1:
        progress["aula_atual"] = idx + 1
        save_progress(user_id, progress)
        bot.reply_to(message, "👍 Aula concluída! Carregando a próxima...")
        show_lesson(message)
    else:
        bot.reply_to(message, "🎓 Você já finalizou todas as 50 aulas! Você é incrível.")

@bot.message_handler(commands=['voltar'])
def prev_lesson(message):
    user_id = str(message.from_user.id)
    progress = load_progress(user_id)
    idx = progress.get("aula_atual", 0)

    if idx > 0:
        progress["aula_atual"] = idx - 1
        save_progress(user_id, progress)
        bot.reply_to(message, "⏪ Voltando para a aula anterior...")
        show_lesson(message)
    else:
        bot.reply_to(message, "Você já está na primeira aula! 🌱")

@bot.message_handler(commands=['resetar'])
def reset_course(message):
    user_id = str(message.from_user.id)
    save_progress(user_id, {"aula_atual": 0})
    bot.reply_to(message, "🔄 Curso reiniciado. Boa sorte no recomeço!")
    show_lesson(message)

# --- EXECUÇÃO EM PARALELO ---
if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    
    print("--- Professor Virtual Iniciado com 50 Aulas ---")
    
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Erro no polling: {e}")
            time.sleep(5)
