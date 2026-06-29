import asyncio
import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes, MessageHandler, filters
)
from scraper import get_all_headlines, get_article_content
from summarizer import summarize_all
from telegram_bot import send_summary_batch
from dotenv import load_dotenv
import os

load_dotenv()
log = logging.getLogger(__name__)

# simpan filter keyword per user (in-memory, reset kalau bot restart)
user_filters = {}

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Crypto News Bot aktif!*\n\n"
        "Commands:\n"
        "/news — ambil berita terbaru sekarang\n"
        "/filter btc eth — filter berita by keyword\n"
        "/filter clear — hapus filter\n"
        "/status — cek filter aktif",
        parse_mode="Markdown"
    )

async def cmd_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text("⏳ Mengambil berita terbaru...")

    try:
        articles = get_all_headlines(max_per_source=3)

        # apply filter kalau ada
        active_filter = user_filters.get(user_id, [])
        if active_filter:
            articles = [
                a for a in articles
                if any(kw.lower() in a["title"].lower() for kw in active_filter)
            ]
            if not articles:
                await update.message.reply_text(
                    f"Tidak ada berita untuk keyword: {', '.join(active_filter)}\n"
                    "Gunakan /filter clear untuk hapus filter."
                )
                return

        await update.message.reply_text(f"🔍 Merangkum {len(articles)} artikel...")
        summaries = summarize_all(articles)
        await send_summary_batch(summaries)

    except Exception as e:
        log.error(f"Error cmd_news: {e}", exc_info=True)
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

async def cmd_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if not args:
        await update.message.reply_text(
            "Contoh penggunaan:\n"
            "/filter btc eth solana\n"
            "/filter clear"
        )
        return

    if args[0].lower() == "clear":
        user_filters.pop(user_id, None)
        await update.message.reply_text("✅ Filter dihapus. Semua berita akan ditampilkan.")
        return

    keywords = [kw.lower() for kw in args]
    user_filters[user_id] = keywords
    await update.message.reply_text(
        f"✅ Filter aktif: *{', '.join(keywords)}*\n"
        "Ketik /news untuk ambil berita dengan filter ini.",
        parse_mode="Markdown"
    )

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    active = user_filters.get(user_id, [])
    if active:
        await update.message.reply_text(
            f"🔍 Filter aktif: *{', '.join(active)}*",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("Tidak ada filter aktif. Semua berita ditampilkan.")

def run_bot():
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("news", cmd_news))
    app.add_handler(CommandHandler("filter", cmd_filter))
    app.add_handler(CommandHandler("status", cmd_status))

    log.info("Bot commands aktif. Tekan Ctrl+C untuk stop.")
    app.run_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_bot()