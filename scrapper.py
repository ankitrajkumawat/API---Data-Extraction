import requests
from bs4 import BeautifulSoup


def scrape_url(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    # Removing extra whitespace and line breaks
    cleaned_text = ' '.join(text.split())
    return cleaned_text
