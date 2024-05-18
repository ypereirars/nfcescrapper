from dataclasses import dataclass
import os
from telebot import TeleBot, logger
import logging
from dotenv import load_dotenv

from api.scrapers.scrapers import NfceScraper

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
            get_and_save_invoice(message.chat.id, value)
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


def get_invoice_by_url(url):
    try:
        invoice = NfceScraper().get(url)
        logger.info("Scraped invoice %s", invoice)
        return invoice
    except Exception as e:
        logger.error("Failed to scrape", e)
        return {}


def save_invoice(invoice):
    try:
        # invoice_id = save(invoice)
        return 0
    except Exception as e:
        logger.error(
            "Failed to save invoice %s: %s",
            invoice.informacoes.chave_acesso,
            str(e),
            exc_info=True,
        )
        return 0


def get_and_save_invoice(chat_id, url):

    try:
        invoice = get_invoice_by_url(url)
        access_key = invoice["informacoes"]["chave_acesso"]

        bot.send_message(
            chat_id,
            f"Ok, consegui buscar os dados da NFC-e **{access_key}**.",
            parse_mode="Markdown",
        )

        logger.info("Scraped invoice %s", invoice)
    except Exception as e:
        bot.send_message(chat_id, "Deu erro ao obter os dados da NFC-e.")
        logger.error("Failed to scrape", e)
        return

    try:
        invoice_id = save_invoice(invoice)

        if invoice_id > 0:
            bot.send_message(chat_id, "Salvei os dados da nota.")
        else:
            bot.send_message(
                chat_id, "Infelizmente não consegui salvá-la no banco de dados."
            )
    except Exception:
        bot.send_message(chat_id, "Deu erro ao salvar os dados da NFC-e.")
        logger.error("Invoice not found", exc_info=True)

    nfce_data = (
        f"*Chave de Acesso:* {access_key}\n"
        + f"*Valor Pago:* R${invoice['totais']['valor_a_pagar']:.2f}\n"
        + f"*Qtd. Itens:* {invoice['totais']['quantidade_itens']}"
    )

    text = f"*INFORMAÇÕES DA NOTA:*\n\n{nfce_data}"
    bot.send_message(chat_id, text, parse_mode="Markdown")


if __name__ == "__main__":
    bot.infinity_polling()
