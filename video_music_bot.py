from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import yt_dlp
import os

def start(update, context):
    update.message.reply_text("🎬 Salom! YouTube, TikTok yoki Instagram link yuboring.\n\n📥 Video yoki Audio yuklab beraman!")

def choose_format(update, context):
    url = update.message.text.strip()
    context.user_data['url'] = url

    keyboard = [
        [InlineKeyboardButton("🎥 Video", callback_data='video')],
        [InlineKeyboardButton("🎧 Audio", callback_data='audio')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("⬇ Qaysi formatda yuklaymiz?", reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    query.answer()
    url = context.user_data.get('url')

    if not url:
        query.edit_message_text("❌ Xatolik: URL topilmadi. Iltimos qaytadan yuboring.")
        return

    format_type = query.data
    query.edit_message_text("⏳ Yuklanmoqda...")

    try:
        if format_type == 'video':
            ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
            filename = 'video.mp4'
            send_as = 'video'
        else:
            ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'audio.mp3'}
            filename = 'audio.mp3'
            send_as = 'audio'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(filename, 'rb') as f:
            if send_as == 'video':
                query.message.reply_video(f, caption="🎬 Tayyor!")
            else:
                query.message.reply_audio(f, caption="🎧 Tayyor!")

        os.remove(filename)

    except Exception as e:
        query.message.reply_text(f"❌ Xatolik: {e}\nURLni tekshirib qayta urinib ko‘ring.")

updater = Updater("8324658572:AAGFW3RfEPL49lFFfyK3uSWECIC26-BvWSY", use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, choose_format))
dp.add_handler(CallbackQueryHandler(button))

updater.start_polling()
updater.idle()
