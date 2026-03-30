# Superset Translator ITA 🇮🇹

Traduttore automatico italiano per file `.po` di Apache Superset.

## 🚀 Installazione

```bash
git clone https://github.com/FrancescoCastaldi/Superset-Translator-ITA.git
cd Superset-Translator-ITA
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
```

## 📝 Uso

```bash
# Metti il tuo file .po nella cartella
copy superset/translations/en/LC_MESSAGES/messages.po messages.po

# Traduci
python traduttore.py

# Risultato: messages_it.po (italiano, senza #fuzzy)
```

## 📁 File generati
- `messages.po` → inglese originale
- `messages_it.po` → italiano tradotto

## 🛠️ Dipendenze
- `polib` - parsing .po
- `requests` - Google Translate API gratuita

**Autore**: Francesco Castaldi  
**Licenza**: MIT