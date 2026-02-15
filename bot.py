import os
import yt_dlp
import uuid
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

TOKEN = "8319679625:AAGUxw3VYdLyU0rNStQHeSL-I0n_pNRykgY"

# إضافة خادم ويب صغير لإبقاء السيرفر مستيقظاً
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_check():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" in url:
        status_msg = await update.message.reply_text("⌛ جاري التحميل يا بياترس... انتظريني")
        unique_filename = f"video_{uuid.uuid4().hex}.mp4"
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': unique_filename,
                'no_warnings': True,
                'quiet': True,
            }
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
            with open(unique_filename, 'rb') as video:
                await update.message.reply_video(video, caption="✅ تم التحميل بنجاح!")
            await status_msg.delete()
            os.remove(unique_filename)
        except Exception as e:
            await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")
            if os.path.exists(unique_filename): os.remove(unique_filename)

if __name__ == '__main__':
    # تشغيل خادم الصحة في خلفية الكود
    threading.Thread(target=run_health_check, daemon=True).start()
    
    app = Application.builder().token(TOKEN).read_timeout(100).write_timeout(100).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("🚀 البوت انطلق في السحاب!")
    app.run_polling()
