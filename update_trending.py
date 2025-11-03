import requests
from bs4 import BeautifulSoup
from datetime import datetime

MD_FILE = "Akai-Tools.md"

def fetch_trending():
    url = "https://github.com/trending?since=daily"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    repos = []
    for repo in soup.select("article.Box-row")[:10]:
        name = repo.h2.a.get_text(strip=True).replace(" / ", "/")
        link = "https://github.com" + repo.h2.a["href"]
        desc = repo.p.get_text(strip=True) if repo.p else "No description"
        repos.append(f"- **[{name}]({link})** — {desc}")
    return repos

def update_markdown(repos):
    with open(MD_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    start, end = "<!-- TRENDING-START -->", "<!-- TRENDING-END -->"
    before = content.split(start)[0] + start + "\n"
    after = "\n" + end + content.split(end)[1]
    today = datetime.utcnow().strftime("%Y-%m-%d")
    trending_text = f"**Updated:** {today} UTC\n\n" + "\n".join(repos)
    new_content = before + trending_text + after
    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    repos = fetch_trending()
    update_markdown(repos)

