#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
import os
import json
import time
import subprocess
import tempfile
import sys

# ================= CONFIG =================
TOKEN = "8225873743:AAHyaQxuZWdFf094aNLW_4KPFqJn-gRnw9U"
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

PASTA_DADOS = "dados"
PASTA_EXEC = "execucoes"

os.makedirs(PASTA_DADOS, exist_ok=True)
os.makedirs(PASTA_EXEC, exist_ok=True)

# ================= AULAS =================
AULAS = {
    1: {
        "titulo": "🐍 Introdução ao Python",
        "conteudo": (
            "Python é uma linguagem simples e poderosa.\n\n"
            "**Exemplo:**\n"
            "```python\nprint('Olá, Mundo!')\n```"
        ),
        "exercicio": "Mostre seu nome usando print().",
        "solucao": "print('Seu nome aqui')"
    },
    2: {
        "titulo": "📊 Variáveis",
        "conteudo": (
            "Variáveis armazenam dados.\n\n"
            "```python\nnome = 'Ana'\nidade = 20\nprint(nome, idade)\n```"
        ),
        "exercicio": "Crie nome e idade e mostre na tela.",
        "solucao": "nome='João'; idade=18; print(nome, idade)"
    }
}

# ================= DESAFIOS =================
DESAFIOS = {
    1: {
        "titulo": "🔢 Soma",
        "descricao": "Some dois números.",
        "dica": "Use o operador +",
        "exemplo": "a=5\nb=3\nprint(a+b)"
    }
}

# ================= PROGRESSO =================
def caminho_progresso(uid):
    return f"{PASTA_DADOS}/{uid}.json"

def carregar_progresso(uid):
    if os.path.exists(caminho_progresso(uid)):
        with open(caminho_progresso(uid), "r", encoding="utf-8") as f:
            return json.load(f)
    return {"aulas": [], "desafios": [], "pontos": 0}

def salvar_progresso(uid, dados):
    with open(caminho_progresso(uid), "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2)

# ================= EXECUTOR =================
def executar_codigo(codigo):
    bloqueados = ["import os", "import sys", "subprocess", "open(", "exec(", "eval("]
    for b in bloqueados:
        if b in codigo.lower():
            return False, f"Comando bloqueado: {b}"

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(codigo)
        nome = f.name

    try:
        res = subprocess.run(
            [sys.executable, nome],
            capture_output=True,
            text=True,
            timeout=5
        )
        return True, res.stdout or "Executado com sucesso!"
    except subprocess.TimeoutExpired:
        return False, "Tempo excedido (5s)"
    finally:
        os.remove(nome)

# ================= COMANDOS =================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "👋 Bem-vindo ao *Bot Professor de Python* 🐍\n\n"
        "Comandos:\n"
        "/aulas – Ver aulas\n"
        "/aula 1 – Ver aula\n"
        "/desafio – Ver desafios\n"
        "/executar código – Executar Python\n"
        "/progresso – Ver progresso"
    )

@bot.message_handler(commands=["aulas"])
def aulas(msg):
    texto = "*📚 Aulas Disponíveis:*\n\n"
    for n, a in AULAS.items():
        texto += f"*{n}* - {a['titulo']}\n"
    bot.send_message(msg.chat.id, texto)

@bot.message_handler(commands=["aula"])
def aula(msg):
    partes = msg.text.split()
    if len(partes) < 2 or not partes[1].isdigit():
        bot.send_message(msg.chat.id, "Use: /aula 1")
        return

    n = int(partes[1])
    if n not in AULAS:
        bot.send_message(msg.chat.id, "Aula não encontrada.")
        return

    aula = AULAS[n]
    progresso = carregar_progresso(msg.from_user.id)

    if n not in progresso["aulas"]:
        progresso["aulas"].append(n)
        progresso["pontos"] += 10
        salvar_progresso(msg.from_user.id, progresso)

    bot.send_message(
        msg.chat.id,
        f"*{aula['titulo']}*\n\n{aula['conteudo']}\n\n"
        f"📝 Exercício:\n_{aula['exercicio']}_"
    )

@bot.message_handler(commands=["desafio"])
def desafio(msg):
    texto = "*💪 Desafios:*\n\n"
    for n, d in DESAFIOS.items():
        texto += f"*{n}* - {d['titulo']}\n"
    bot.send_message(msg.chat.id, texto)

@bot.message_handler(commands=["executar"])
def executar(msg):
    codigo = msg.text.replace("/executar", "", 1).strip()
    if not codigo:
        bot.send_message(msg.chat.id, "Use: /executar print('Oi')")
        return

    ok, res = executar_codigo(codigo)
    bot.send_message(
        msg.chat.id,
        f"```python\n{codigo}\n```\n\n📤 Resultado:\n```\n{res}\n```"
    )

@bot.message_handler(commands=["progresso"])
def progresso(msg):
    p = carregar_progresso(msg.from_user.id)
    bot.send_message(
        msg.chat.id,
        f"📊 *Seu Progresso*\n\n"
        f"Aulas: {len(p['aulas'])}\n"
        f"Desafios: {len(p['desafios'])}\n"
        f"Pontos: {p['pontos']}"
    )

# ================= START BOT =================
if __name__ == "__main__":
    print("🤖 Bot Professor de Python rodando...")
    bot.polling(none_stop=True)
