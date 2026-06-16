# 🎰 SpareBank 1 Lotteri

En moderne og visuelt tiltalende lotteri-applikasjon med animert "wheel of fortune". Perfekt for å trekke vinnere på events, møter eller fagsamlinger med full historikk-logging og statistikk.

![SpareBank 1 Design](https://img.shields.io/badge/Design-SpareBank%201%20FFE-002776?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.7%2B-3776ab?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=flat-square)

---

## ✨ Funksjoner

### 🎡 Lotterihjul
- ✅ Animert spinning wheel med deltakernavn
- ✅ **Sekvensielle treninger**: Trekk en og en vinner ved å klikke en knapp
- ✅ Tredimensjonal animasjon med easing
- ✅ Sansynlighetsbasert trekning (flere lodd = flere muligheter)

### 👥 Deltakerhåndtering
- ✅ Legg til deltakere manuelt (navn, e-post, antall lodd)
- ✅ Håndter flere lodd per person
- ✅ Enkel deltaker-oversikt

### 📊 Historikk & Statistikk
- ✅ **Automatisk lagring av vinnere** med dato og tidspunkt
- ✅ Vis historikk av alle treninger
- ✅ Statistikk over hvor ofte hver deltaker vinner
- ✅ Eksport historikk til Excel-fil

### 🎨 Design
- ✅ SpareBank 1 (FFE) design system
- ✅ Moderne og responsiv UI
- ✅ Norsk grensesnitt
- ✅ Intuitiv og brukervennlig

### 💾 Data
- ✅ Lokal lagring (ingen nett-krav)
- ✅ Excel-fil med deltakere
- ✅ JSON-historikk med datoer
- ✅ Excel-export av vinner-historikk

---

## 🚀 Rask Start

### Forutsetninger
- Python 3.7 eller nyere
- (Git for kloning fra GitHub)

### 1. Clone eller last ned repositoriet

```bash
git clone https://github.com/ditt-brukernavn/Vinlotteri.git
cd Vinlotteri
```

Eller last ned som ZIP og pakk ut.

### 2. Installer avhengigheter

**Windows** (dobbeltklikk):
```
run.bat
```

**macOS/Linux** (terminal):
```bash
chmod +x run.sh
./run.sh
```

**Manuell installasjon:**
```bash
# Opprett virtuelt miljø (anbefalt)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# eller
venv\Scripts\activate  # Windows

# Installer pakker
pip install -r requirements.txt
```

### 3. Kjør applikasjonen

**Windows**: Dobbeltklikk `run.bat`

**macOS/Linux**: `./run.sh` eller `python3 app.py`

### 4. Åpne i nettleser

Gå til: **http://localhost:5000**

---

## 📖 Bruk

### Første gang: Legg til deltakere

**Alternativ 1: Manuell registrering**
1. Skriv inn navn (påkrevd)
2. E-post (valgfritt)
3. Antall lodd (standard: 1)
4. Klikk "Legg til deltaker"

**Eksempel:**
- Ole Petter - 3 lodd (3x mulighet for å vinne)
- Anna - 2 lodd (2x mulighet)
- Kari - 1 lodd (normal mulighet)

### Start treningssesjon

1. **Skriv antall gevinster** du vil trekke (f.eks. "3" for 3 priser)
2. Klikk **"Start treningssesjon"**
3. Knappene endres til "Trekk neste vinner" og "Avbryt"
4. Treningsstatus vises (f.eks. "1 / 3")

### Trekk vinnere - en og en

1. Klikk **"Trekk neste vinner"**
2. Hjulet spins i 2 sekunder
3. Vinner vises både på hjulet og i vinnerlisten
4. Status oppdateres (f.eks. "2 / 3")
5. Gjenta til alle gevinster er trukket

### Lagre treningsresultat

1. Når alle gevinster er trukket, klikk **"💾 Lagre vinnere"**
2. Treningsresultatet lagres til:
   - `data/lotteri_history.json` (lokal lagring)
   - `data/lotteri_history.xlsx` (Excel-fil)
3. Vinnerlisten tømmes automatisk

### Se historikk & statistikk

**Historikk-fanen:**
- Se alle tidligere treninger med dato og klokkeslett
- Navn på alle vinnere per treningssesjon

**Statistikk-fanen:**
- Se hvor mange ganger hver person har vunnet
- Sortert etter antall gevinster
- E-postadresser vises

**Last ned Excel:**
- Klikk "Last ned historikk (Excel)"
- Eksporterer all historikk som lesbar Excel-fil

---

## 📁 Filstruktur

```
Vinlotteri/
├── app.py                    # Hoved Flask-applikasjon
├── requirements.txt          # Python-avhengigheter
├── run.sh                    # Startup script (macOS/Linux)
├── run.bat                   # Startup script (Windows)
├── .gitignore               # Git ignore rules
├── README.md                # Denne filen
│
├── data/                    # Data-mappe (Excel og historikk)
│   ├── lotteri_data.xlsx    # Deltakerdata (opprettet automatisk)
│   └── lotteri_history.json # Historikk (opprettet automatisk)
│
├── venv/                    # Virtuelt Python-miljø (opprettet ved kjøring)
└── __pycache__/            # Python cache (ignorert av Git)
```

---

## 🎲 Hvordan lottemekanikken fungerer

### Sannsynligheter
- **1 lodd** = 1 mulighet for å bli trukket
- **3 lodd** = 3 muligheter (3x større sjanse)
- **5 lodd** = 5 muligheter (5x større sjanse)

### Eksempel: 3 personer, 2 gevinster
```
Ole Petter (3 lodd)
Anna (2 lodd)
Kari (1 lodd)
Totalt: 6 lodd i hjulet

Trekning 1:
- Hjulet har 6 lodd (OOP, OOP, OOP, A, A, K)
- Hvis OOP blir trukket → Ole Petter vinner pris 1
- Ole Petters lodd fjernes fra hjulet

Trekning 2:
- Hjulet har nå 3 lodd (A, A, K)
- Anna eller Kari blir trukket → får pris 2
```

**Viktig:** Samme person kan ikke vinne samme pris to ganger, men hvis de har mange lodd kan de vinne flere priser.

---

## 🔧 Teknisk informasjon

### Stack
- **Backend**: Python 3 + Flask 2.3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data**: Excel (openpyxl), JSON
- **Design**: SpareBank 1 FFE system

### API Endpoints

| Metode | Endpoint | Beskrivelse |
|--------|----------|-------------|
| GET | `/api/participants` | Hent alle deltakere |
| POST | `/api/participants/add` | Legg til deltaker |
| POST | `/api/participants/clear` | Slett alle deltakere |
| POST | `/api/draw/start` | Start treningssesjon |
| POST | `/api/draw/next` | Trekk neste vinner |
| POST | `/api/draw/save` | Lagre treningsresultat |
| POST | `/api/draw/cancel` | Avbryt sesjon |
| GET | `/api/history` | Hent historikk |
| POST | `/api/history/download` | Eksport til Excel |

### Dependencies
```
Flask==2.3.2          # Web framework
openpyxl==3.1.2      # Excel handling
Werkzeug==2.3.6      # WSGI utilities
```

---

## ⚙️ Feilsøking

### Python er ikke installert
**Feil:** `command not found: python3`

**Løsning:** 
- Last ned fra https://www.python.org/
- Installer med alle standardvalg
- Start terminalen på nytt

### Port 5000 er opptatt
**Feil:** `Address already in use`

**Løsning:**
- Steng annen applikasjon som bruker porten
- Eller rediger `app.py` linje sist: `app.run(port=5001)`

### Kan ikke opprett data-mappe
**Feil:** `Permission denied`

**Løsning:**
- Sjekk at mappen er skrivbar
- Kjør fra en plass du har tilgang til
- Prøv å kjøre som administrator

### Feil ved lesing av Excel
**Feil:** `openpyxl not found`

**Løsning:**
```bash
pip install openpyxl==3.1.2
```

### Nettleseren åpnes ikke automatisk
**Løsning:**
- Manuelt: Gå til http://localhost:5000
- Eller rediger `app.py` og legg til `webbrowser.open()` på slutten

---

## 🚀 Deployment

### GitHub Pages
Denne applikasjonen krever en backend, så kan ikke kjøres direkte på GitHub Pages. Men du kan:
1. Pushe koden til GitHub
2. Klone repo og kjør lokalt
3. Eller bruk Heroku/PythonAnywhere for cloud deployment

### Lokalt på en annen maskin
1. Klone repository på maskinen
2. Kjør `run.sh` eller `run.bat`
3. Åpne http://localhost:5000

### Nettverkstilgang (for andre på nettverket)
Rediger `app.py` siste linje:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```
Deretter kan andre på nettverket åpne: `http://<din-ip>:5000`

---

## 📝 Lisens

MIT License - Se LICENSE-filen

---

## 🤝 Bidrag

Forslag til forbedringer? Opprett en issue eller pull request!

---

## 📞 Support

Hvis du opplever problemer:
1. Sjekk at Python 3.7+ er installert: `python3 --version`
2. Sjekk at pakker er installert: `pip list`
3. Sjekk konsoll-feil (F12 i nettleseren)
4. Prøv å slette `venv` og kjør `run.sh`/`run.bat` på nytt

---

## 🎉 Versjonhistorikk

### v1.0 (2025)
- ✅ Initiell release
- ✅ Sekvensielle treninger
- ✅ Historikk-logging
- ✅ SpareBank 1 design
- ✅ Statistikk og eksport

---

**Laget med ❤️ for SpareBank 1**
