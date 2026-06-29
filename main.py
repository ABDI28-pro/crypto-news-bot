import time
import schedule
import logging
from scraper import get_coindesk_headlines
from summarizer import summarize_all
from telegram_bot import send_to_telegram
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

def run_pipeline(max_articles=5):
    log.info("Pipeline dimulai")
    try:
        log.info("Scraping CoinDesk...")
        articles = get_coindesk_headlines(max_articles=max_articles)
        if not articles:
            log.warning("Tidak ada artikel ditemukan. Skip.")
            return

        log.info(f"Ditemukan {len(articles)} artikel. Summarizing...")
        summaries = summarize_all(articles)

        log.info(f"Mengirim {len(summaries)} ringkasan ke Telegram...")
        send_to_telegram(summaries)

        log.info("Pipeline selesai.")

    except Exception as e:
        log.error(f"Pipeline error: {e}", exc_info=True)
        try:
            import asyncio
            from telegram_bot import send_message as _send_err
            asyncio.run(_send_err(f"⚠️ *Pipeline Error*\n`{str(e)}`"))
        except:
            pass

def run_scheduled():
    log.info("Scheduler aktif — pipeline jalan tiap 08:00 dan 20:00")
    schedule.every().day.at("08:00").do(run_pipeline)
    schedule.every().day.at("20:00").do(run_pipeline)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--schedule":
            run_scheduled()
        elif sys.argv[1] == "--bot":
            from bot_commands import run_bot
            run_bot()
    else:
        run_pipeline(max_articles=3)