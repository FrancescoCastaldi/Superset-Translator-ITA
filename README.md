# Superset Translator ITA

Traduttore automatico per file `.po` di Apache Superset in lingua italiana.

## Panoramica

Progetto per tradurre automaticamente i file di traduzione (`.po`) di Apache Superset dall'inglese all'italiano utilizzando l'API gratuita di Google Translate. Rimuove automaticamente le marcature `# fuzzy` dalle stringhe tradotte.

## Requisiti

- Python 3.8+
- File `.po` di Superset (inglese)

## Installazione

```bash
git clone https://github.com/FrancescoCastaldi/Superset-Translator-ITA.git
cd Superset-Translator-ITA

# Crea ambiente virtuale
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Utilizzo

1. Copia il file `.po` da tradurre nella cartella del progetto:
   ```bash
   copy "percorso/superset/translations/en/LC_MESSAGES/messages.po" messages.po
   ```

2. Esegui la traduzione:
   ```bash
   python traduttore.py
   ```

3. Risultato: `messages_it.po` con traduzioni italiane complete (senza `# fuzzy`)

## Output atteso
✓ 1/1250 - 'Dashboard title'
✓ 2/1250 - 'Save dashboard'
...
✅ Fatto!


## File del progetto

| File | Descrizione |
|------|-------------|
| `traduttore.py` | Script principale di traduzione |
| `messages.po` | File sorgente inglese (esempio) |
| `messages_it.po` | File destinazione italiano (generato) |
| `requirements.txt` | Dipendenze Python |

## Dipendenze

- `polib` - Parsing file `.po`
- `requests` - Client HTTP per Google Translate API

## Limitazioni

- Rate limiting di Google Translate (1 richiesta/0.1s)
- File `.po` grandi (>10k stringhe) richiedono tempo
- Traduzioni automatiche: rivedere manualmente per qualità professionale

## Contributo

1. Fork del repository
2. Crea branch `feature/xyz`
3. Commit e push
4. Crea Pull Request

## Autore

**Francesco Castaldi**  
Ingegnere Informatico | Healthcare Business Consultant  
[LinkedIn](https://linkedin.com/in/francescocastaldi) | [GitHub](https://github.com/FrancescoCastaldi)

## Licenza

MIT License - vedi [LICENSE](LICENSE) per dettagli.