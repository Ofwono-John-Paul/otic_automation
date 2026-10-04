import requests
from bs4 import BeautifulSoup

pages = {
    "HOME": "https://ofwono-john-paul.github.io/portfolio/",
    "PROJECTS": "https://ofwono-john-paul.github.io/portfolio/projects.html",
    "CONTACT": "https://ofwono-john-paul.github.io/portfolio/contact.html",
    "ABOUT": "https://ofwono-john-paul.github.io/portfolio/about.html",
    "SKILLS": "https://ofwono-john-paul.github.io/portfolio/skills.html"
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

            # Remove unnecessary elements
            for element in soup([
                "script",
                "style",
                "noscript",
                "nav",
                "footer"
            ]):
                element.decompose()

            text = soup.get_text(
                "\n",
                strip=True
            )

            # Write section heading
            file.write("\n")
            file.write("=" * 70 + "\n")
            file.write(f"{page_name}\n")
            file.write("=" * 70 + "\n\n")

            # Write URL for future source tracking
            file.write(f"Source: {url}\n\n")

            # Write scraped content
            file.write(text)

            file.write("\n\n")

            print(f"✓ {page_name} completed")

        except requests.RequestException as error:

            print(f"✗ Failed to scrape {page_name}")
            print(error)

print("\nDone! Data saved to portfolio_data1.txt")