# ⚡ Rask Start (2 minutter)

## Windows

1. **Dobbeltklikk** → `run.bat`
2. **Vent** → "Åpne nettleseren på: http://localhost:5000"
3. **Done!** 🎉

Hjulet spinner automatisk med eksempel-data (Ole Petter, Anna, Kari, Jan, Maria)

## macOS / Linux

1. **Terminal** → `./run.sh`
2. **Vent** → "Åpne nettleseren på: http://localhost:5000"
3. **Done!** 🎉

## Første bruk

1. **Legg til deltakere:**
   - Navn (påkrevd)
   - E-post (valgfritt)
   - Antall lodd (hvor mange muligheter for å vinne)

2. **Start treningssesjon:**
   - Skriv f.eks. "3" (3 priser)
   - Klikk "Start treningssesjon"

3. **Trekk vinnere:**
   - Klikk "Trekk neste vinner" 
   - Hjulet spinner → vinner vises
   - Gjenta til alle er trukket

4. **Lagre resultatet:**
   - Klikk "💾 Lagre vinnere"
   - Historikk + statistikk lagres automatisk

## Eksempel-flow (30 sekunder)

```
5 personer registrert
↓
Skriv "2" (vil trekke 2 vinnere)
↓
Klikk "Start"
↓
Klikk "Trekk neste vinner" → Ole Petter vinner pris 1 🎉
↓
Klikk "Trekk neste vinner" → Anna vinner pris 2 🎉
↓
Klikk "💾 Lagre vinnere"
↓
✅ Done! Historikk lagret
```

## Se statistikk

1. Gå til **"Trenings-historikk"** (nederst)
2. Se **"Statistikk"** tabben
3. Hvem har vunnet hvor mange ganger?

## Prøv Excel-eksport

1. Klikk **"📥 Last ned historikk (Excel)"**
2. Fil: `data/lotteri_history.xlsx` (i samme mappe som `app.py`)

---

## Hvis noe går galt

**Feilen: "Port already in use"**
- Steng andre Firefox/Chrome vinduer
- Eller kjør med annen port: rediger `app.py` siste linje

**Feilen: "Python not found"**
- Last ned fra https://www.python.org/

**Feilen: "Module not found"**
- Kjør `run.sh` eller `run.bat` på nytt (installerer pakker)

---

## GitHub Setup

Vil du pushe til GitHub?

1. `git init`
2. `git add .`
3. `git commit -m "Initial commit"`
4. `git remote add origin https://github.com/DITT-BRUKERNAVN/Vinlotteri.git`
5. `git push -u origin main`

Se `GITHUB_SETUP.md` for detaljer.

---

**Lykke til! 🎰**
