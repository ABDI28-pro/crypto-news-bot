from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarize_article(title, content):
    prompt = f"""Kamu adalah analis crypto profesional.
Analisis artikel berikut dan berikan output dalam format ini PERSIS:

SENTIMENT: [pilih salah satu: BULLISH / BEARISH / NEUTRAL]
RINGKASAN: [2-3 kalimat ringkasan dalam Bahasa Indonesia]
TAKEAWAY: [1 kalimat poin penting untuk trader]

Artikel:
Judul: {title}
Konten: {content}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300
    )

    raw = response.choices[0].message.content
    return parse_summary(raw, title)


def parse_summary(raw, title):
    lines = raw.strip().split("\n")
    sentiment = "NEUTRAL"
    ringkasan = ""
    takeaway = ""

    for line in lines:
        if line.startswith("SENTIMENT:"):
            s = line.replace("SENTIMENT:", "").strip().upper()
            if "BULLISH" in s:
                sentiment = "BULLISH"
            elif "BEARISH" in s:
                sentiment = "BEARISH"
            else:
                sentiment = "NEUTRAL"
        elif line.startswith("RINGKASAN:"):
            ringkasan = line.replace("RINGKASAN:", "").strip()
        elif line.startswith("TAKEAWAY:"):
            takeaway = line.replace("TAKEAWAY:", "").strip()

    emoji = {"BULLISH": "🟢", "BEARISH": "🔴", "NEUTRAL": "🟡"}

    return {
        "sentiment": sentiment,
        "emoji": emoji[sentiment],
        "formatted": (
            f"{emoji[sentiment]} *{sentiment}*\n\n"
            f"📰 *{title[:100]}*\n\n"
            f"📝 {ringkasan}\n\n"
            f"💡 {takeaway}"
        )
    }


def summarize_all(articles):
    results = []
    for i, article in enumerate(articles):
        print(f"Summarizing {i+1}/{len(articles)}: {article['title'][:50]}...")
        from scraper import get_article_content
        content = get_article_content(article["url"])
        parsed = summarize_article(article["title"], content)
        results.append({
            "title": article["title"],
            "url": article["url"],
            "source": article.get("source", ""),
            "sentiment": parsed["sentiment"],
            "emoji": parsed["emoji"],
            "summary": parsed["formatted"]
        })
    return results


if __name__ == "__main__":
    from scraper import get_all_headlines
    articles = get_all_headlines(max_per_source=2)

    if not articles:
        print("Tidak ada artikel ditemukan.")
    else:
        summaries = summarize_all(articles)
        for s in summaries:
            print("\n" + "="*50)
            print(f"[{s['emoji']} {s['sentiment']}] {s['title'][:60]}")
            print(s["summary"])
            print(f"Sumber: {s['source']}")