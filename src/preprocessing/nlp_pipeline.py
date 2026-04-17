import spacy

# Load once globally (important for performance)
nlp = spacy.load("en_core_web_md")


def process_text(text: str):
    doc = nlp(text)

    tokens = [token.text for token in doc]
    pos_tags = [(token.text, token.pos_) for token in doc]
    dependencies = [(token.text, token.dep_, token.head.text) for token in doc]

    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return {
        "tokens": tokens,
        "pos_tags": pos_tags,
        "dependencies": dependencies,
        "entities": entities
    }