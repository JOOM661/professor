# Importa a biblioteca do Telegram Bot
import telebot
import os
import time

# Configurações iniciais
# TOKEN: Chave única do seu bot (você vai conseguir no @BotFather no Telegram)
TOKEN = "SEU_TOKEN_AQUI"  # Substitua pelo seu token real

# Cria o objeto bot
bot = telebot.TeleBot(TOKEN)

# Cria a pasta de dados se não existir
if not os.path.exists('dados'):
    os.makedirs('dados')

# Função para salvar dados em arquivos
def salvar_dados(arquivo, dados, modo='a'):
    """
    Salva informações em um arquivo de texto
    arquivo: nome do arquivo
    dados: conteúdo a ser salvo
    modo: 'a' para adicionar, 'w' para sobrescrever
    """
    caminho = os.path.join('dados', arquivo)
    with open(caminho, modo, encoding='utf-8') as f:
        f.write(dados + '\n')

# Função para ler dados de arquivos
def ler_dados(arquivo):
    """
    Lê informações de um arquivo de texto
    Retorna uma lista com as linhas do arquivo
    """
    caminho = os.path.join('dados', arquivo)
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

# Dicionário para armazenar respostas dos usuários temporariamente
# Isso fica na memória enquanto o bot está rodando
respostas_usuarios = {}

print("🤖 Bot iniciado! Aguardando comandos...")
