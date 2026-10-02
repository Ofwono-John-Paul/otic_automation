import requests
from bs4 import BeautifulSoup

url = "https://ofwono-john-paul.github.io/portfolio/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

text = soup.get_text(" ", strip=True)

# Save scraped text to database.txt
with open("database.txt", "w", encoding="utf-8") as file:
    file.write(text)

print("Scraped data saved to database.txt")