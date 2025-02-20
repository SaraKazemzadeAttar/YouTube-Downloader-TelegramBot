import os
import telebot
import yt_dlp
from pytube import YouTube
import logging
import re

BOT_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

DOWNLOAD_DIR = "downloads/"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
telebot.logger.setLevel(logging.INFO)

def download_video(url, file_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()

        if not stream:
            return None

        stream.download(output_path=DOWNLOAD_DIR, filename="downloaded_video.mp4")
        return yt.title if os.path.exists(file_path) else None  # Return title if successful

    except Exception:
        return None  


def download_with_ytdlp(url, file_path):
    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': file_path
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info.get('title') if os.path.exists(file_path) else None  # Return title if successful

    except Exception:
        return None  


def send_video_to_user(chat_id, file_path, title , message_id):

    with open(file_path, 'rb') as vid:
        bot.send_video(chat_id, video=vid, caption=f"🎬 {title}", reply_to_message_id = message_id)

    os.remove(file_path)
    bot.send_message(chat_id, "✅ Download complete! 🎉")
    
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,"👋 Hello!\n Send me a **YouTube link**, and I'll download the video for you.🎥 ",
        parse_mode="Markdown",
    )

@bot.message_handler(func=lambda message: re.match(r"^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/", message.text))
def handle_video_request(message):
    url = message.text
    fetching_msg = bot.send_message(message.chat.id, "🔍 Fetching video details...")
    bot.delete_message(message.chat.id, fetching_msg.message_id, timeout=50)


    file_path = os.path.join(DOWNLOAD_DIR, "downloaded_video.mp4")

    try:
        title = download_video(url, file_path)
        if title:
            send_video_to_user(message.chat.id, file_path, title , message.id)
            return

        title = download_with_ytdlp(url, file_path)
        if title:
            send_video_to_user(message.chat.id, file_path, title , message.id)
            return

        bot.send_message(message.chat.id, "❌ Failed to download video.", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Unexpected error: `{e}`", parse_mode="Markdown")


bot.infinity_polling()