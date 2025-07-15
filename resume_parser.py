import json

import fitz  # PyMuPDF
import spacy
from spacy.matcher import PhraseMatcher
import re

with open("data/skills.json", "r") as f:
    skill_keywords = json.load(f)



# Load English spaCy model
nlp = spacy.load("en_core_web_sm")

# Build PhraseMatchers for each category
matchers = {}
for category, terms in skill_keywords.items():
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(term) for term in terms]
    matcher.add(category, patterns)
    matchers[category] = matcher

# --- Extract text from resume PDF ---
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return " ".join(page.get_text() for page in doc)


# --- NLP-based skill extraction ---
def extract_skills(text):
    doc = nlp(text)
    categorized_skills = {}

    for category, matcher in matchers.items():
        matches = matcher(doc)
        # Extract and normalize matched skill names
        skills = [doc[start:end].text.strip() for _, start, end in matches]

        # Canonicalize (e.g., make case-insensitive, then map back to original casing)
        unique_skills = {}
        for skill in skills:
            key = skill.lower()
            if key not in unique_skills:
                unique_skills[key] = skill  # Preserve original case

        if unique_skills:
            categorized_skills[category] = sorted(unique_skills.values())

    return categorized_skills