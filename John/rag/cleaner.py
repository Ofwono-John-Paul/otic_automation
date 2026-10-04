import re


INPUT_FILE = "portfolio_data.txt"
OUTPUT_FILE = "cleaned_portfolio_data.txt"


def clean_text(text):
    # Remove carriage returns
    text = text.replace("\r", "")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    # Remove lines containing only separators
    text = re.sub(r"^[=_-]{5,}$", "", text, flags=re.MULTILINE)

    # Remove common web noise
    noise = [
        "Home",
        "Menu",
        "Navigation",
        "Back to top",
        "Cookie Policy",
        "Privacy Policy",
    ]

    for item in noise:
        text = re.sub(
            rf"^\s*{re.escape(item)}\s*$",
            "",
            text,
            flags=re.MULTILINE | re.IGNORECASE
        )

    # Clean spaces around newlines
    text = re.sub(r" *\n *", "\n", text)

    # Final blank-line cleanup
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    text = file.read()


cleaned_text = clean_text(text)


with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(cleaned_text)


print("Cleaning completed.")
print(f"Saved cleaned data to: {OUTPUT_FILE}")