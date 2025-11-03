import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

TRENDING_URL = "https://github.com/trending"
FILES_TO_UPDATE = ["Akai-Tools.md", "README.md"]  # both files will be updated

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

def build_trending_md(repos):
    """Generate markdown section for trending repos."""
    ist_offset = timedelta(hours=5, minutes=30)
    ist_time = datetime.now(timezone.utc) + ist_offset
    updated_time = ist_time.strftime("%Y-%m-%d %H:%M IST")

    trending_md = "<!-- TRENDING-START -->\n"
    trending_md += f"**Updated:** {updated_time}\n\n"
    for i, (name, url, desc) in enumerate(repos, start=1):
        trending_md += f"{i}. **[{name}]({url})** — {desc}\n"
    trending_md += "<!-- TRENDING-END -->\n"
    return trending_md

def update_markdown_file(filename, trending_md):
    """Replace trending section inside a given markdown file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"⚠️ File not found: {filename}")
        return

    start_marker = "<!-- TRENDING-START -->"
    end_marker = "<!-- TRENDING-END -->"

    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[-1]
        new_content = before + trending_md + after
    else:
        # If markers are missing, append at the end
        new_content = content + "\n\n" + trending_md

    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Updated: {filename}")

def main():
    print("🚀 Fetching trending repositories...")
    repos = fetch_trending_repos()
    trending_md = build_trending_md(repos)

    for file in FILES_TO_UPDATE:
        update_markdown_file(file, trending_md)

    print("✅ All markdown files updated successfully (Time shown in IST)!")

if __name__ == "__main__":
    main()



