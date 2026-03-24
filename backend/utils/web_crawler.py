# utils/web_crawler.py


import requests
from bs4 import BeautifulSoup

def fetch_all(endpoint):
    results = []
    page = 1

    while True:
        url = f"{endpoint}?page={page}"

        try:
            res = requests.get(url, timeout=10)
        except:
            break

        if res.status_code != 200:
            break

        data = res.json()

        if not data:
            break

        results.extend(data)
        page += 1

    return results


def extract_text_with_links(html):
    soup = BeautifulSoup(html, "html.parser")

    text_parts = []

    for tag in soup.find_all(["p", "li", "h1", "h2", "h3"]):
        line = tag.get_text()

        if tag.find("a"):
            link = tag.find("a").get("href")
            if link:
                line += f" (Link: {link})"

        text_parts.append(line)

    return "\n".join(text_parts)


def fetch_wordpress_data(base_url):
    all_docs = []

    page_api = base_url.rstrip("/") + "/wp-json/wp/v2/pages"
    post_api = base_url.rstrip("/") + "/wp-json/wp/v2/posts"

    page_data = fetch_all(page_api)
    post_data = fetch_all(post_api)

    # Pages
    for page in page_data:
        html_content = page["content"]["rendered"]
        text = extract_text_with_links(html_content)

        metadata = {
            "title": page["title"]["rendered"],
            "url": page["link"],
            "type": "page"
        }

        all_docs.append((text, metadata))

    for post in post_data:
        html_content = post["content"]["rendered"]
        text = extract_text_with_links(html_content)

        metadata = {
            "title": post["title"]["rendered"],
            "url": post["link"],
            "type": "post"
        }

        all_docs.append((text, metadata))

    return all_docs
