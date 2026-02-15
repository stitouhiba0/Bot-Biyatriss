import telebot
import yt_dlp
import os

# ضع التوكن الخاص بك هنا
API_TOKEN = '8319679625:AAGUxw3VYdLyU0rNStQHeSL-I0n_pNRykgY'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✨ مرحباً بك في بوت التحميل الذكي! ✨\n\n"
        "👤 المالكة: المبرمجة بياترس\n"
        "🚀 الحالة: البوت جاهز للخدمة"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "http" in url:
        bot.reply_to(message, "⏳ جاري التحميل...")
        try:
            ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove('video.mp4')
        except Exception as e:
            bot.reply_to(message, "❌ خطأ في الرابط.")

bot.polling()

 
