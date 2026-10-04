import re
import json


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "cleaned_portfolio_data.txt"
OUTPUT_FILE = "portfolio_chunks.json"


# ============================================================
# PROJECTS FOUND ON THE PORTFOLIO
# ============================================================

PROJECT_TITLES = [
    "E-commerce Platform",
    "Mobile Applications",
    "Web-based Systems",
    "Embedded Systems",
    "COCIS Examination Hub",
    "Computer Networking"
]


# ============================================================
# SKILL CATEGORIES
# ============================================================

SKILL_CATEGORIES = [
    "Frontend",
    "Backend",
    "Programming Languages",
    "Frameworks & Tools",
    "Specialized Skills"
]


# ============================================================
# SOURCE URLS
# ============================================================

SOURCE_URLS = {
    "home": "https://ofwono-john-paul.github.io/portfolio/",
    "projects": "https://ofwono-john-paul.github.io/portfolio/projects.html",
    "contact": "https://ofwono-john-paul.github.io/portfolio/contact.html",
    "about": "https://ofwono-john-paul.github.io/portfolio/about.html",
    "skills": "https://ofwono-john-paul.github.io/portfolio/skills.html"
}


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_chunk_text(text):
    """
    Clean individual chunk text without destroying
    meaningful structure.
    """

    # Normalize line endings
    text = text.replace("\r", "")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    # Remove unnecessary whitespace
    text = "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

    return text.strip()


# ============================================================
# CREATE CHUNK
# ============================================================

def create_chunk(
    chunks,
    section,
    title,
    source,
    text,
    category=None
):
    """
    Create a structured chunk with metadata.
    """

    text = clean_chunk_text(text)

    if not text:
        return

    chunk = {
        "chunk_id": len(chunks) + 1,
        "section": section,
        "title": title,
        "source": source,
        "text": text
    }

    if category:
        chunk["category"] = category

    chunks.append(chunk)


# ============================================================
# EXTRACT SOURCE URL
# ============================================================

def extract_source(text):
    """
    Find the source URL inside a section.
    """

    match = re.search(
        r"Source:\s*(https?://\S+)",
        text
    )

    if match:
        return match.group(1)

    return None


# ============================================================
# EXTRACT MAIN SECTIONS
# ============================================================

def extract_sections(text):
    """
    Split the entire document into:

    HOME
    PROJECTS
    CONTACT
    ABOUT
    SKILLS
    """

    section_pattern = re.compile(
        r"(?m)^(HOME|PROJECTS|CONTACT|ABOUT|SKILLS)\s*$"
    )

    matches = list(section_pattern.finditer(text))

    sections = {}

    for i, match in enumerate(matches):

        section_name = match.group(1).lower()

        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section_text = text[start:end].strip()

        sections[section_name] = section_text

    return sections


# ============================================================
# PROCESS HOME
# ============================================================

def process_home(home_text, chunks):

    source = extract_source(home_text)

    if not source:
        source = SOURCE_URLS["home"]

    # Remove source line
    home_text = re.sub(
        r"Source:\s*https?://\S+",
        "",
        home_text
    )

    # Remove page title
    home_text = re.sub(
        r"My Portfolio\s*-\s*Home",
        "",
        home_text,
        flags=re.IGNORECASE
    )

    # Remove navigation-style buttons
    home_text = re.sub(
        r"\b(View My Work|Get In Touch)\b",
        "",
        home_text,
        flags=re.IGNORECASE
    )

    create_chunk(
        chunks=chunks,
        section="home",
        title="Introduction",
        source=source,
        text=home_text
    )


# ============================================================
# PROCESS ABOUT
# ============================================================

def process_about(about_text, chunks):

    source = extract_source(about_text)

    if not source:
        source = SOURCE_URLS["about"]

    # Remove source
    about_text = re.sub(
        r"Source:\s*https?://\S+",
        "",
        about_text
    )

    # Remove page title
    about_text = re.sub(
        r"My Portfolio\s*-\s*About",
        "",
        about_text,
        flags=re.IGNORECASE
    )

    # Remove unnecessary buttons
    about_text = re.sub(
        r"\bDownload CV\b",
        "",
        about_text,
        flags=re.IGNORECASE
    )

    create_chunk(
        chunks=chunks,
        section="about",
        title="About Me",
        source=source,
        text=about_text
    )


# ============================================================
# PROCESS CONTACT
# ============================================================

def process_contact(contact_text, chunks):

    source = extract_source(contact_text)

    if not source:
        source = SOURCE_URLS["contact"]

    contact_text = re.sub(
        r"Source:\s*https?://\S+",
        "",
        contact_text
    )

    contact_text = re.sub(
        r"My Portfolio\s*-\s*Contact",
        "",
        contact_text,
        flags=re.IGNORECASE
    )

    # Remove form status messages
    contact_text = re.sub(
        r"Oops!\s*Something went wrong\.\s*Please try again\.",
        "",
        contact_text,
        flags=re.IGNORECASE
    )

    create_chunk(
        chunks=chunks,
        section="contact",
        title="Contact Information",
        source=source,
        text=contact_text
    )


# ============================================================
# PROCESS PROJECTS
# ============================================================

def process_projects(projects_text, chunks):

    source = extract_source(projects_text)

    if not source:
        source = SOURCE_URLS["projects"]

    # Remove source
    projects_text = re.sub(
        r"Source:\s*https?://\S+",
        "",
        projects_text
    )

    # Remove page title
    projects_text = re.sub(
        r"My Portfolio\s*-\s*Projects",
        "",
        projects_text,
        flags=re.IGNORECASE
    )

    # Remove "My Projects"
    projects_text = re.sub(
        r"\bMy Projects\b",
        "",
        projects_text,
        flags=re.IGNORECASE
    )

    # Create pattern for project titles
    project_pattern = re.compile(
        "|".join(
            re.escape(title)
            for title in PROJECT_TITLES
        ),
        flags=re.IGNORECASE
    )

    matches = list(
        project_pattern.finditer(projects_text)
    )

    for i, match in enumerate(matches):

        project_title = match.group(0)

        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            # Stop before Skills Developed
            skills_match = re.search(
                r"\bSkills Developed\b",
                projects_text[start:],
                flags=re.IGNORECASE
            )

            if skills_match:
                end = start + skills_match.start()
            else:
                end = len(projects_text)

        project_text = projects_text[start:end]

        # Remove duplicate project title
        project_text = re.sub(
            rf"^{re.escape(project_title)}\s*",
            "",
            project_text,
            count=1,
            flags=re.IGNORECASE
        )

        # Remove UI text
        project_text = re.sub(
            r"\bView Project\b",
            "",
            project_text,
            flags=re.IGNORECASE
        )

        project_text = re.sub(
            r"\bSource Code\b",
            "",
            project_text,
            flags=re.IGNORECASE
        )

        # Clean the project text
        project_text = clean_chunk_text(project_text)

        # Add the project title explicitly
        final_text = (
            f"Project: {project_title}\n\n"
            f"{project_text}"
        )

        create_chunk(
            chunks=chunks,
            section="projects",
            title=project_title,
            source=source,
            text=final_text
        )

    # --------------------------------------------------------
    # Skills developed through projects
    # --------------------------------------------------------

    skills_match = re.search(
        r"\bSkills Developed\b(.*)",
        projects_text,
        flags=re.IGNORECASE | re.DOTALL
    )

    if skills_match:

        skills_text = skills_match.group(0)

        create_chunk(
            chunks=chunks,
            section="projects",
            title="Skills Developed Through Projects",
            source=source,
            text=skills_text
        )


# ============================================================
# PROCESS SKILLS
# ============================================================

def process_skills(skills_text, chunks):

    source = extract_source(skills_text)

    if not source:
        source = SOURCE_URLS["skills"]

    # Remove source
    skills_text = re.sub(
        r"Source:\s*https?://\S+",
        "",
        skills_text
    )

    # Remove page title
    skills_text = re.sub(
        r"My Portfolio\s*-\s*Skills",
        "",
        skills_text,
        flags=re.IGNORECASE
    )

    # Remove "My Skills"
    skills_text = re.sub(
        r"\bMy Skills\b",
        "",
        skills_text,
        flags=re.IGNORECASE
    )

    # Create each skill category separately
    category_pattern = re.compile(
        "|".join(
            re.escape(category)
            for category in SKILL_CATEGORIES
        ),
        flags=re.IGNORECASE
    )

    matches = list(
        category_pattern.finditer(skills_text)
    )

    for i, match in enumerate(matches):

        category = match.group(0)

        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(skills_text)

        category_text = skills_text[start:end]

        # Remove category title from body
        category_text = re.sub(
            rf"^{re.escape(category)}\s*",
            "",
            category_text,
            count=1,
            flags=re.IGNORECASE
        )

        category_text = clean_chunk_text(
            category_text
        )

        final_text = (
            f"Skill Category: {category}\n\n"
            f"{category_text}"
        )

        create_chunk(
            chunks=chunks,
            section="skills",
            title=category,
            category=category,
            source=source,
            text=final_text
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\nStarting portfolio chunker...\n")

    # --------------------------------------------------------
    # Read cleaned data
    # --------------------------------------------------------

    try:

        with open(
            INPUT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

    except FileNotFoundError:

        print(
            f"ERROR: Could not find {INPUT_FILE}"
        )

        return

    # --------------------------------------------------------
    # Extract sections
    # --------------------------------------------------------

    sections = extract_sections(text)

    print(
        f"Sections found: {', '.join(sections.keys())}"
    )

    # --------------------------------------------------------
    # Create chunks
    # --------------------------------------------------------

    chunks = []

    if "home" in sections:
        process_home(
            sections["home"],
            chunks
        )

    if "projects" in sections:
        process_projects(
            sections["projects"],
            chunks
        )

    if "contact" in sections:
        process_contact(
            sections["contact"],
            chunks
        )

    if "about" in sections:
        process_about(
            sections["about"],
            chunks
        )

    if "skills" in sections:
        process_skills(
            sections["skills"],
            chunks
        )

    # --------------------------------------------------------
    # Save JSON
    # --------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print(
        f"\nChunking completed successfully."
    )

    print(
        f"Total chunks created: {len(chunks)}"
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    # --------------------------------------------------------
    # Preview chunks
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("CHUNK PREVIEW")
    print("=" * 70)

    for chunk in chunks:

        print(
            f"\n[{chunk['chunk_id']}] "
            f"{chunk['section'].upper()} → "
            f"{chunk['title']}"
        )

        print("-" * 70)

        print(
            chunk["text"][:500]
        )

        if len(chunk["text"]) > 500:
            print("...")


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    main()