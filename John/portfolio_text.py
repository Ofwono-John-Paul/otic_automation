import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://ofwono-john-paul.github.io/portfolio/"

pages = {
    "HOME": BASE_URL,
    "ABOUT": urljoin(BASE_URL, "about.html"),
    "SKILLS": urljoin(BASE_URL, "skills.html"),
    "PROJECTS": urljoin(BASE_URL, "projects.html"),
    "CONTACT": urljoin(BASE_URL, "contact.html")
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

with open("portfolio_data.txt", "w", encoding="utf-8") as file:

    for page_name, url in pages.items():

        print(f"Scraping {page_name}...")

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Remove elements that don't contain useful content
            for element in soup([
                "script",
                "style",
                "noscript",
                "nav",
                "footer"
            ]):
                element.decompose()

            # Extract visible text
            text = soup.get_text(
                "\n",
                strip=True
            )

            # Write section
            file.write(f"\n\n{'=' * 60}\n")
            file.write(f"{page_name}\n")
            file.write(f"{'=' * 60}\n\n")
            file.write(text)

            print(f"{page_name} scraped successfully.")

        except requests.RequestException as error:
            print(f"Failed to scrape {page_name}: {error}")

print("\nAll portfolio data saved to portfolio_data.txt")