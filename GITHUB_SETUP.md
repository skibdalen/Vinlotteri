# 📘 GitHub Setup Guide

Denne guiden forklarer hvordan du setter opp repositoriet på GitHub og gjør det klar for andres bruk.

---

## 1. Opprett GitHub Repository

### Lokalt (fra terminalen)

```bash
# Gå til prosjekt-mappen
cd Vinlotteri

# Initialisér Git
git init

# Legg til alle filer
git add .

# Første commit
git commit -m "Init: SpareBank 1 Lotteri applikasjon"

# Legg til GitHub remote (erstatt USERNAME og REPO)
git remote add origin https://github.com/USERNAME/Vinlotteri.git

# Push til GitHub
git branch -M main
git push -u origin main
```

### Via GitHub.com

1. Gå til https://github.com/new
2. Repository name: `Vinlotteri`
3. Beskrivelse: "SpareBank 1 Lottery System - with wheel animation and winner tracking"
4. Public ✓
5. Initialize with README ✗ (vi har allerede en)
6. Create repository
7. Følg instruksjonene for å pushe eksisterende repo

---

## 2. GitHub Repository Settings

### ✓ Viktige innstillinger

**About (høyre side)**
- ✅ Legg til beskrivelse
- ✅ Legg til emner: `lottery`, `sparebank`, `flask`, `python`
- ✅ Gjør README prominent

**Settings → Code and automation → Actions**
- Optional: Sett opp CI/CD tests

**Settings → Pages** (ikke relevant her, men kan være aktuelt senere)

---

## 3. Struktur for GitHub

Din GitHub mapper skal se slik ut:

```
Vinlotteri/
├── .gitignore              # Utelukk data og __pycache__
├── .github/
│   └── workflows/          # CI/CD (valgfritt)
├── README.md               # Hoveddokumentasjon
├── GITHUB_SETUP.md         # Denne filen
├── QUICK_START.md          # Rask start-guide
├── requirements.txt        # Python avhengigheter
├── run.sh                  # macOS/Linux startup
├── run.bat                 # Windows startup
├── app.py                  # Flask applikasjon
│
├── data/                   # Data-mappe (IKKE pushed til GitHub)
│   ├── lotteri_data.xlsx   # (ignorert)
│   └── lotteri_history.json# (ignorert)
│
└── venv/                   # Virtual env (IKKE pushed)
```

**NB:** `.gitignore` sørger for at `data/` og `venv/` ikke pushes!

---

## 4. Git Workflow

### Etter første push:

```bash
# Sjekk status
git status

# Se endringer
git diff

# Stage alle endringer
git add .

# Commit med beskrivelse
git commit -m "Feature: Add export to Excel"

# Push til GitHub
git push origin main
```

### Eksempel commits:

```bash
git commit -m "Fix: Correct wheel animation timing"
git commit -m "Feature: Add statistics tab"
git commit -m "Docs: Update README with examples"
git commit -m "Refactor: Simplify draw logic"
```

---

## 5. Samarbeid (Inviter andre)

1. Gå til Settings → Collaborators
2. Legg til GitHub-brukernavn
3. De kan da pushe direkte (eller bruke Pull Requests)

---

## 6. Branches (Valgfritt)

For større endringer:

```bash
# Opprett ny branch
git checkout -b feature/new-feature

# Gjør endringer og commit
git add .
git commit -m "Add new feature"

# Push branch
git push origin feature/new-feature

# Lag Pull Request på GitHub.com
# Review → Merge til main
```

---

## 7. Releases (Valgfritt)

Når du har en stabil versjon:

1. Gå til "Releases" på GitHub
2. Klikk "Create a new release"
3. Tag: `v1.0` (eller neste versjon)
4. Title: `Version 1.0 - Initial Release`
5. Description: 
   ```
   Features:
   - Animated lottery wheel
   - Sequential draws
   - Winner history tracking
   - SpareBank 1 design
   ```
6. Publish release

---

## 8. README Best Practices

Din README.md bør ha:

✅ **Header** med titel og badges
✅ **Features list** med emoji
✅ **Quick Start** - 5 linjer max
✅ **Installation** - steg-for-steg
✅ **Usage** - eksempler
✅ **File structure** - oversikt
✅ **Troubleshooting** - vanlige problemer
✅ **License** - MIT eller tilsvarende

---

## 9. GitHub Pages (Dokumentasjon)

Hvis du vil lage dokumentasjonsnettsted:

1. Settings → Pages
2. Source: `main` branch → `root` eller `/docs`
3. Velg tema
4. Automatisk deploy til GitHub Pages

Eller lag en `docs/` mappe med statisk HTML.

---

## 10. Example GitHub README Badge

Legg til på toppen av README.md:

```markdown
![Python](https://img.shields.io/badge/Python-3.7%2B-3776ab?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-All-blue?style=flat-square)
```

Generer badges: https://shields.io/

---

## 11. Vanlige Git Kommandoer

```bash
# Klon repository
git clone https://github.com/USERNAME/Vinlotteri.git

# Se remote
git remote -v

# Se branches
git branch -a

# Synkroniser med GitHub
git fetch origin
git pull origin main

# Se commit history
git log --oneline

# Angre siste commit
git reset --soft HEAD~1

# Slett branch lokalt
git branch -d feature/old-feature

# Slett branch på GitHub
git push origin --delete feature/old-feature
```

---

## 12. Tips for GitHub Success

✅ **Commit messages:**
- Bruk preteritum: "Add feature" ikke "Added"
- First line: kort tittel
- Blank line
- Detaljer hvis nødvendig

✅ **Filnavn:**
- Norske tegn OK men unngå spesialtegn
- Bruk underscore: `lotteri_data.xlsx`

✅ **.gitignore:**
- Aldri commit hemmeligheter, API-nøkler
- Aldri commit store binærfiler
- Aldri commit persondata

✅ **File size:**
- GitHub anbefaler < 100 MB
- Hvis større: bruk Git LFS

✅ **Dokumentasjon:**
- README for setup
- Code comments for kompleks logikk
- CHANGELOG for versjonhistorikk

---

## 13. GitHub Issues & Projects

### Issues (for tracking)
1. Gå til "Issues" tabben
2. "New issue"
3. Tittel: "Add history export to CSV"
4. Description: Detaljer
5. Assign til deg selv eller andre

### Projects (for planning)
1. "Projects" tabben
2. "New project"
3. Kanban board
4. Link issues til tasks

---

## 14. Eksempel: Klone og kjør fra GitHub

For andre som vil bruke appen:

```bash
# 1. Klone
git clone https://github.com/USERNAME/Vinlotteri.git
cd Vinlotteri

# 2. Kjør
./run.sh          # macOS/Linux
# eller
run.bat           # Windows

# 3. Åpne
http://localhost:5000
```

---

## 15. Security

❌ **Aldri commit:**
- API keys eller secrets
- Passord eller tokens
- Private email
- Database URLs

✅ **Hvis du må:**
- Bruk `.env` fil (legg i `.gitignore`)
- Dokumenter i README at brukere må konfigurere
- Bruk GitHub Secrets for CI/CD

---

## 📝 Eksempel CHANGELOG

Lag en `CHANGELOG.md`:

```markdown
# Changelog

## [1.1.0] - 2025-02-15
### Added
- Export history to CSV
- Keyboard shortcuts for draw

### Fixed
- Wheel animation stutter on slow devices

## [1.0.0] - 2025-02-01
### Added
- Initial release
- Animated lottery wheel
- Sequential draws
- Winner history
- SpareBank 1 design
```

---

## 🎉 Du er ferdig!

Repositoriet ditt er nå klar for:
- ✅ Sharing på GitHub
- ✅ Samarbeid
- ✅ Open source bruk
- ✅ Feature development

Lykke til! 🚀

---

**Spørsmål?** 
- GitHub Docs: https://docs.github.com
- Git Guide: https://git-scm.com/doc
