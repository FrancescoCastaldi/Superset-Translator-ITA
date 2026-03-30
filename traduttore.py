import polib
import requests
import time
import re

TECHNICAL_TERMS = [
    "API", "REST", "HTTP", "HTTPS", "URL", "JSON", "XML", "HTML", "CSS",
    "JavaScript", "Python", "SQL", "database", "backend", "frontend",
    "framework", "middleware", "endpoint", "token", "OAuth", "JWT",
    "webhook", "payload", "request", "response", "server", "client",
    "cache", "cookie", "session", "login", "logout", "email", "username",
    "password", "hash", "debug", "log", "error", "warning", "info",
    "status", "config", "deploy", "build", "test", "staging", "production",
]

def protect_technical_terms(text):
    placeholders = {}
    protected = text
    for i, term in enumerate(TECHNICAL_TERMS):
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        placeholder = f"__TECH_{i}__"
        if pattern.search(protected):
            placeholders[placeholder] = term
            protected = pattern.sub(placeholder, protected)
    return protected, placeholders

def restore_technical_terms(text, placeholders):
    restored = text
    for placeholder, term in placeholders.items():
        restored = restored.replace(placeholder, term)
    return restored

def capitalize_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    capitalized = []
    for sentence in sentences:
        if sentence:
            sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
            capitalized.append(sentence)
    result = ' '.join(capitalized)
    if result:
        result = result[0].upper() + result[1:]
    return result

def translate_google(text):
    protected_text, placeholders = protect_technical_terms(text)

    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        'client': 'gtx',
        'sl': 'en',
        'tl': 'it',
        'dt': 't',
        'q': protected_text
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        result = resp.json()
        translated = result[0][0][0]
        translated = restore_technical_terms(translated, placeholders)
        translated = capitalize_sentences(translated)
        return translated
    except:
        return text

def translate_entry(entry, count, total):
    """Gestisce sia entry singole che plurali (bulk)."""
    
    # Entry con plurali (msgid_plural presente)
    if entry.msgid_plural:
        forms_to_translate = {
            0: entry.msgid,         # forma singolare
            1: entry.msgid_plural,  # forma plurale
        }
        # Aggiungi eventuali forme plurali extra già presenti
        for idx in entry.msgstr_plural:
            if idx > 1:
                forms_to_translate[idx] = entry.msgstr_plural[idx]

        needs_translation = (
            not entry.msgstr_plural
            or any(not v for v in entry.msgstr_plural.values())
            or 'fuzzy' in entry.flags
        )

        if needs_translation:
            for idx, source_text in forms_to_translate.items():
                if not entry.msgstr_plural.get(idx) or 'fuzzy' in entry.flags:
                    translated = translate_google(source_text)
                    entry.msgstr_plural[idx] = translated
                    label = "singolare" if idx == 0 else f"plurale[{idx}]"
                    msgid_preview = source_text[:50] + "..." if len(source_text) > 50 else source_text
                    print(f"  ↳ [{label}] '{msgid_preview}' → '{translated[:50]}'")
                    time.sleep(0.1)

            if 'fuzzy' in entry.flags:
                entry.flags.remove('fuzzy')

            print(f"✓ {count}/{total} - [PLURAL] '{entry.msgid[:50]}'")
        else:
            print(f"- {count}/{total} - Già tradotto (plural)")

    # Entry singola normale
    else:
        if not entry.msgstr or 'fuzzy' in entry.flags:
            msgid_preview = entry.msgid[:50] + "..." if len(entry.msgid) > 50 else entry.msgid
            translated = translate_google(entry.msgid)
            entry.msgstr = translated
            if 'fuzzy' in entry.flags:
                entry.flags.remove('fuzzy')
            print(f"✓ {count}/{total} - '{msgid_preview}'")
            time.sleep(0.1)
        else:
            print(f"- {count}/{total} - Già tradotto")

def translate_po_file(input_file, output_file):
    po = polib.pofile(input_file)

    total = len(po)
    count = 0

    for entry in po:
        count += 1
        try:
            translate_entry(entry, count, total)
        except Exception as e:
            print(f"✗ Errore: {entry.msgid[:50]}... ({e})")

    print(f"\nSalvando {output_file}...")
    po.save(output_file)
    print("✅ Fatto!")

if __name__ == "__main__":
    translate_po_file('messages.po', 'messages_it.po')