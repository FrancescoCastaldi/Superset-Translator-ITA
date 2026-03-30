import polib
import requests
import time

def translate_google(text):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        'client': 'gtx',
        'sl': 'en',
        'tl': 'it',
        'dt': 't',
        'q': text
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        result = resp.json()
        return result[0][0][0]
    except:
        return text

def translate_po_file(input_file, output_file):
    po = polib.pofile(input_file)
    
    total = len(po)
    count = 0
    
    for entry in po:
        if not entry.msgstr or 'fuzzy' in entry.flags:
            try:
                msgid = entry.msgid[:50] + "..." if len(entry.msgid) > 50 else entry.msgid
                translated = translate_google(entry.msgid)
                entry.msgstr = translated
                if 'fuzzy' in entry.flags:
                    entry.flags.remove('fuzzy')
                count += 1
                print(f"✓ {count}/{total} - '{msgid}'")
                time.sleep(0.1)
            except Exception as e:
                print(f"✗ Errore: {entry.msgid[:50]}...")
        else:
            count += 1
            print(f"- {count}/{total} - Già tradotto")
                
    print(f"\nSalvando {output_file}...")
    po.save(output_file)
    print("✅ Fatto!")

if __name__ == "__main__":
    translate_po_file('messages.po', 'messages_it.po')