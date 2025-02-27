import telebot
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

CHANNEL_ID = "-1002319708853"
CHANNEL_LINK = "https://t.me/PyroProxy"

def is_member(bot , message):
    if not bot:
        return False

    user_info = bot.get_chat_member(CHANNEL_ID, message.from_user.id)
    if user_info.status not in ["administrator", "creator", "member"]:
        bot.send_message(
            message.chat.id,
            f"⚠️ Please subscribe to our channel to use this bot: [Join Channel]({CHANNEL_LINK})",
            parse_mode="Markdown",
        )
        return False
    return True

def check_member(message):
    bot.reply_to(message, "✅ You are verified!")
