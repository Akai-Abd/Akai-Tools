import requests
from bs4 import BeautifulSoup
from datetime import datetime

TRENDING_URL = "https://github.com/trending"
MD_FILE = "Akai-Tools.md"

def fetch_trending_repos():
    """Fetch top 10 trending repositories from GitHub Trending."""
    response = requests.get(TRENDING_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    repos = []
    for item in soup.select("article.Box-row")[:10]:
        title_tag = item.h2.a
        repo_name = title_tag.get_text(strip=True).replace(" / ", "/")
        repo_url = "https://github.com" + title_tag["href"]
        description_tag = item.p
        description = description_tag.get_text(strip=True) if description_tag else "No description provided"
        repos.append((repo_name, repo_url, description))
    return repos

def update_markdown(repos):
    """Update the markdown file between the TRENDING-START and TRENDING-END comments."""
    with open(MD_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- TRENDING-START -->"
    end_marker = "<!-- TRENDING-END -->"

    before = content.split(start_marker)[0]
    after = content.split(end_marker)[-1]

    updated_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Format the trending section beautifully
    trending_md = f"{start_marker}\n**Updated:** {updated_time}\n\n"
    for i, (name, url, desc) in enumerate(repos, start=1):
        trending_md += f"{i}. **[{name}]({url})** — {desc}\n"
    trending_md += f"{end_marker}\n"

    new_content = before + trending_md + after

    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    print("🚀 Fetching trending repositories...")
    repos = fetch_trending_repos()
    update_markdown(repos)
    print("✅ Akai-Tools.md updated successfully!")

if __name__ == "__main__":
    main()


