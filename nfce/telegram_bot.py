from dataclasses import dataclass
import os
from telebot import TeleBot, logger
import logging
from dotenv import load_dotenv

from .services import scrape_invoice
from .database import save

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

logger.setLevel(logging.INFO)

bot = TeleBot(TELEGRAM_BOT_TOKEN)


@dataclass
class User:
    def __init__(self, id: int, first_name: str, last_name: str, username: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self) -> str:
        return self.full_name if self.full_name else f"@{self.username}"

    @staticmethod
    def get_user(func):
        def wrapper(message):
            user = User(
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username,
            )
            return func(message, user)

        return wrapper


@bot.message_handler(commands=["start"])
@User.get_user
def start_handler(message, user=None):
    response_message = (
        f"Oi, *{user}*.\n"
        + "Eu sou o bot (não oficial) da NFC-e!\n"
        + "Me envie a URL de uma NFC-e que eu salvo para você."
    )

    logger.info("%s started using the bot", user)
    bot.reply_to(message, response_message, parse_mode="Markdown")


@bot.message_handler(commands=["help"])
def help_handler(message):
    help_message = (
        "Para usar o bot, me envie a URL de uma NFC-e que eu salvo para você.\n\n"
        + "Comandos disponíveis:\n"
        + "  - /start - Exibe a mensagem inicial do bot.\n\n"
        + "  - /help - Exibe esta mensagem de ajuda.\n\n"
        + "  - /nfce url <url> - Salva a NFC-e com a URL informada.\n\n"
        + "  - /nfce chave <chave> - Salva a NFC-e com a chave de acesso informada.\n\n"
    )
    bot.reply_to(message, help_message)


@bot.message_handler(commands=["nfce"])
@User.get_user
def nfce_command(message, user=None):
    logger.info("User %s sent the command %s", user, message.text)

    commands = message.text.split(" ")

    if len(commands) == 3:
        option = commands[1]
        value = commands[2]

        if option.lower() == "url":
            fetch_nfce_by_url(message.chat.id, value)
            return
        elif option.lower() == "chave":
            fetch_nfce_by_key(message.chat.id, value)
            return
        else:
            response_message = (
                "Opção inválida. Por favor, escolha entre *URL* ou *CHAVE*."
            )
            bot.send_message(message.chat.id, response_message, parse_mode="Markdown")
            return

    response_message = "Por favor, use o comando `/nfce url` seguido da <URL>."
    bot.send_message(message.chat.id, response_message, parse_mode="Markdown")
    return


def fetch_nfce_by_url(chat_id, url):

    try:
        invoice = scrape_invoice(url)
        logger.info("Scraped invoice %s", invoice.informacoes.chave_acesso)
    except Exception as e:
        text = f"Deu erro ao obter os dados da NFC-e."
        bot.send_message(chat_id, text)
        logger.error("Failed to scrape", e)
        return

    try:
        invoice_id = save(invoice)
    except Exception as e:
        saved = False
        logger.error(
            "Failed to save invoice %s: %s",
            invoice.informacoes.chave_acesso,
            str(e),
            exc_info=True,
        )

    if invoice_id > 0:
        msg = "*NFC-e salva com sucesso!*"
    else:
        msg = "Consegui obter os dados da nota, mas não consegui salvá-la no banco de dados."

    nfce_data = (
        f"*Chave de Acesso:* {invoice.informacoes.chave_acesso}\n"
        + f"*Valor:* R${invoice.totais.valor_total:.2f}\n"
        + f"*Emissão:* {invoice.informacoes.data_emissao}"
    )

    text = f"{msg}\n\nInformações da nota:\n\n{nfce_data}"
    bot.send_message(chat_id, text, parse_mode="Markdown")


if __name__ == "__main__":
    bot.infinity_polling()
