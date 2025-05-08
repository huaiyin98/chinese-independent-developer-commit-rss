import os, requests
from feedgen.feed import FeedGenerator

OWNER = "1c7"
REPO = "chinese-independent-developer"

COMMITS_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/commits"
HEADERS = {"Accept": "application/vnd.github.v3+json"}

r = requests.get(COMMITS_URL, headers=HEADERS)
commits = r.json()

fg = FeedGenerator()
fg.title(f'Commits from {OWNER}/{REPO} with Diffs')
fg.link(href=f"https://github.com/{OWNER}/{REPO}")
fg.description('GitHub commit history with file-level diffs')

for commit in commits[:10]:
    sha = commit['sha']
    detail = requests.get(f"{COMMITS_URL}/{sha}", headers=HEADERS).json()
    msg = detail['commit']['message']
    author = detail['commit']['author']['name']
    diff = "<br>".join(
        f"<b>{f['filename']}</b><br><pre>{f.get('patch', '(binary file)')}</pre>"
        for f in detail.get('files', [])
    )

    e = fg.add_entry()
    e.title(msg)
    e.link(href=commit['html_url'])
    e.author(name=author)
    e.content(diff, type='html')

os.makedirs("public", exist_ok=True)
fg.rss_file("public/feed.xml")
