import asyncio
import os
import logging
from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))


async def send_message(text):
    try:
        await bot.send_message(
            chat_id=os.getenv("TELEGRAM_CHAT_ID"),
            text=text,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        log.error(f"Error sending message: {e}")


async def send_summary_batch(summaries):
    await send_message("🚀 *Crypto News Update*\n_Powered by AI Summarizer_")

    for i, item in enumerate(summaries, 1):
        # support format baru (dengan sentiment) dan format lama
        if isinstance(item, dict):
            summary_text = item.get("summary", "")
            url = item.get("url", "")
            source = item.get("source", "")
        else:
            summary_text = str(item)
            url = ""
            source = ""

        source_tag = f"📡 *Sumber: {source}*\n" if source else ""
        link_tag = f"\n🔗 [Baca selengkapnya]({url})" if url else ""

        message = f"{source_tag}{summary_text}{link_tag}"

        await send_message(message)

        if i < len(summaries):
            await asyncio.sleep(1)

    await send_message(f"✅ *Selesai* — {len(summaries)} artikel dirangkum.")


def send_to_telegram(summaries):
    asyncio.run(send_summary_batch(summaries))


if __name__ == "__main__":
    test_msg = (
        "🧪 *Test koneksi berhasil!*\n\n"
        "Bot crypto news summarizer siap digunakan."
    )
    asyncio.run(send_message(test_msg))
    print("Pesan test terkirim ke Telegram.")