import requests
from bs4 import BeautifulSoup


def get_coindesk_headlines(max_articles=5):
    url = "https://www.coindesk.com/latest-crypto-news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching CoinDesk: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    cards = soup.find_all("a", href=True)

    seen = set()
    for card in cards:
        href = card.get("href", "")
        text = card.get_text(strip=True)

        if (
            href.startswith("/")
            and len(text) > 40
            and href not in seen
            and any(k in href for k in ["/markets/", "/tech/", "/policy/", "/business/"])
        ):
            seen.add(href)
            articles.append({
                "title": text[:200],
                "url": "https://www.coindesk.com" + href,
                "source": "CoinDesk"
            })

        if len(articles) >= max_articles:
            break

    return articles


def get_cointelegraph_headlines(max_articles=5):
    url = "https://cointelegraph.com/rss"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching CoinTelegraph: {e}")
        return []

    soup = BeautifulSoup(response.text, "xml")
    items = soup.find_all("item")

    articles = []
    for item in items[:max_articles]:
        title = item.find("title")
        link = item.find("link")
        if title and link:
            articles.append({
                "title": title.get_text(strip=True),
                "url": link.get_text(strip=True),
                "source": "CoinTelegraph"
            })

    return articles


def get_article_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error: {e}"

    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")
    content = " ".join(
        p.get_text(strip=True)
        for p in paragraphs
        if len(p.get_text(strip=True)) > 60
    )

    return content[:3000] if content else "Content not found."


def get_all_headlines(max_per_source=3):
    print("Fetching CoinDesk...")
    coindesk = get_coindesk_headlines(max_per_source)

    print("Fetching CoinTelegraph...")
    cointelegraph = get_cointelegraph_headlines(max_per_source)

    all_articles = coindesk + cointelegraph
    print(
        f"Total: {len(all_articles)} artikel dari "
        f"{len(coindesk)} CoinDesk + {len(cointelegraph)} CoinTelegraph"
    )
    return all_articles


if __name__ == "__main__":
    articles = get_all_headlines(max_per_source=3)
    for a in articles:
        print(f"\n[{a['source']}] {a['title']}")
        print(f"URL: {a['url']}")
        content = get_article_content(a["url"])
        print(f"Preview: {content[:150]}...")