import os
from telebot import TeleBot, logger
from telebot.types import Message
import logging
from . import services

from .utils import get_user_from


__all__ = ["telegram_bot"]


TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
telegram_bot = TeleBot(TELEGRAM_BOT_TOKEN)
logger.setLevel(logging.INFO)


@telegram_bot.message_handler(commands=["comecar"])
def start_handler(message: Message):
    user = get_user_from(message)
    response_message = (
        f"Oi, *{user}*.\n"
        + "Eu sou o bot (não oficial) da NFC-e!\n"
        + "Me envie a URL de uma NFC-e que eu salvo para você."
    )

    logger.info("Saving user '%s'.", user)
    try:
        services.save_user(user)
    except Exception as e:
        logger.error("Failed to save user '%s'.", user, e)

    logger.info("User '%s' started using the bot", user)
    telegram_bot.reply_to(message, response_message, parse_mode="Markdown")


@telegram_bot.message_handler(commands=["ajuda"])
def help_handler(message: Message):
    help_message = (
        "Para usar o bot, me envie a URL de uma NFC-e que eu salvo para você.\n\n"
        + "Comandos disponíveis:\n"
        + "  - /comecar - Exibe a mensagem inicial do bot.\n\n"
        + "  - /ajuda - Exibe esta mensagem de ajuda.\n\n"
        + "  - /nfce <url> - Salva a NFC-e com a URL informada.\n\n"
        + "  - /nfce <chave> - Salva a NFC-e com a chave de acesso informada.\n\n"
    )
    telegram_bot.reply_to(message, help_message)


@telegram_bot.message_handler(commands=["nfce"])
def nfce_command(message: Message):
    user_bot = get_user_from(message)

    logger.info("User %s sent the command %s", user_bot, message.text)

    commands = message.text.split(" ")

    if len(commands) != 2:
        response = "Por favor, use o comando `/nfce ` seguido da <URL> ou <CHAVE>."
        telegram_bot.send_message(message.chat.id, response, parse_mode="Markdown")
        return

    _, value = commands
    data = {}
    try:
        logger.info("Scraping value '%s' from user '%s'.", value, user_bot)
        data = services.scrape_invoice(value)
        if "error" in data or not data["invoice"]:
            raise Exception(data["error"])
    except ValueError as e:
        response = "Opção inválida. Por favor, escolha entre *URL* ou *CHAVE*."
        logger.error("Invalid option", e)
        telegram_bot.send_message(message.chat.id, response, parse_mode="Markdown")
        return
    except TimeoutError as e:
        response = "Desculpe, não consegui buscar os dados da NFC-e. Tente novamente mais tarde."
        logger.error("An error happen when trying to get value from '%s'.", value, e)
        telegram_bot.send_message(message.chat.id, response)
    except Exception as e:
        response = "Desculpe, não consegui buscar os dados da NFC-e."
        logger.error("An error happen when trying to get value from '%s'.", value, e)
        telegram_bot.send_message(message.chat.id, response)
        return

    try:
        services.save_invoice(user_bot, data["invoice"])

        access_key = data["invoice"]["informacoes"]["chave_acesso"]

        response = f"Ok, consegui buscar os dados da NFC-e {access_key}."
        telegram_bot.send_message(message.chat.id, response, parse_mode="Markdown")
        logger.info("Invoice '%s' scraped successfully", access_key)
    except Exception as e:
        response = "Desculpe, não consegui salvar os dados da NFC-e."
        logger.error("An error happen when trying to save invoice", e)
        telegram_bot.send_message(message.chat.id, response)
        return