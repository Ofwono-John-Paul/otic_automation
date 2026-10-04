import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://ofwono-john-paul.github.io/portfolio/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

for link in soup.find_all("a", href=True):

    href = urljoin(url, link["href"])

    print(link.get_text(" ", strip=True), "→", href)