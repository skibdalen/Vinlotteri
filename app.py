#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SpareBank 1 Lottery System
Lotteri-applikasjon med animert hjul, sekvensielle treninger og historikk
"""

import os
import sys
import json
import random
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

# Initialisering
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Finn mappen hvor scriptet kjører fra
SCRIPT_DIR = Path(__file__).parent.absolute()
DATA_DIR = SCRIPT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

EXCEL_FILE = DATA_DIR / "lotteri_data.xlsx"
HISTORY_FILE = DATA_DIR / "lotteri_history.json"

# Session storage for current draw
current_draw_session = {
    'participants': [],
    'wheel': [],
    'target_draws': 0,
    'draws_completed': 0,
    'winners': [],
    'used_indices': set(),
    'available_wheel': []
}

def init_excel_file():
    """Initier Excel-fil hvis den ikke finnes"""
    if not EXCEL_FILE.exists():
        wb = Workbook()
        ws = wb.active
        ws.title = "Deltakere"
        ws['A1'] = "Navn"
        ws['B1'] = "E-post"
        ws['C1'] = "Antall lodd"
        
        # Eksempel-data
        examples = [
            ("Ole Petter", "ole@example.com", 3),
            ("Anna", "anna@example.com", 2),
            ("Kari", "kari@example.com", 1),
            ("Jan", "jan@example.com", 2),
            ("Maria", "maria@example.com", 4)
        ]
        
        for idx, (name, email, tickets) in enumerate(examples, start=2):
            ws[f'A{idx}'] = name
            ws[f'B{idx}'] = email
            ws[f'C{idx}'] = tickets
        
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 25
        ws.column_dimensions['C'].width = 15
        
        wb.save(EXCEL_FILE)
        print(f"✓ Opprettet ny Excel-fil: {EXCEL_FILE}")

def init_history_file():
    """Initier historikk-fil"""
    if not HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def read_participants():
    """Les deltakere fra Excel-fil"""
    if not EXCEL_FILE.exists():
        return []
    
    try:
        wb = load_workbook(EXCEL_FILE)
        ws = wb.active
        participants = []
        
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] is None:
                continue
            name = str(row[0]).strip()
            email = str(row[1]).strip() if row[1] else ""
            tickets = int(row[2]) if row[2] else 1
            
            if name and tickets > 0:
                participants.append({
                    "name": name,
                    "email": email,
                    "tickets": tickets
                })
        
        return participants
    except Exception as e:
        print(f"Feil ved lesing av Excel: {e}")
        return []

def write_participants(participants):
    """Skriv deltakere til Excel-fil"""
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Deltakere"
        
        ws['A1'] = "Navn"
        ws['B1'] = "E-post"
        ws['C1'] = "Antall lodd"
        
        for idx, p in enumerate(participants, start=2):
            ws[f'A{idx}'] = p['name']
            ws[f'B{idx}'] = p['email']
            ws[f'C{idx}'] = p['tickets']
        
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 25
        ws.column_dimensions['C'].width = 15
        
        wb.save(EXCEL_FILE)
        return True
    except Exception as e:
        print(f"Feil ved skriving til Excel: {e}")
        return False

def create_lottery_wheel(participants):
    """Opprett lotterihjul med lodd basert på antall billetter"""
    wheel = []
    for p in participants:
        for _ in range(p['tickets']):
            wheel.append({
                'name': p['name'],
                'email': p['email']
            })
    return wheel

def read_history():
    """Les vinner-historikk"""
    if not HISTORY_FILE.exists():
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def write_history(history):
    """Skriv vinner-historikk"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Feil ved skriving av historikk: {e}")
        return False

def export_history_to_excel():
    """Eksporter historikk til Excel-fil"""
    try:
        history = read_history()
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Vinner-historikk"
        
        # Header
        ws['A1'] = "Dato"
        ws['B1'] = "Trekning"
        ws['C1'] = "Prisnummer"
        ws['D1'] = "Vinner"
        ws['E1'] = "E-post"
        ws['F1'] = "Antall lodd"
        
        row = 2
        for entry in history:
            draw_date = entry.get('date', 'Ukjent dato')
            draw_id = entry.get('draw_id', '')
            
            for idx, winner in enumerate(entry.get('winners', []), 1):
                ws[f'A{row}'] = draw_date
                ws[f'B{row}'] = draw_id
                ws[f'C{row}'] = idx
                ws[f'D{row}'] = winner.get('name', '')
                ws[f'E{row}'] = winner.get('email', '')
                ws[f'F{row}'] = winner.get('tickets', '')
                row += 1
        
        # Justering av kolonnebredde
        ws.column_dimensions['A'].width = 19
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 12
        ws.column_dimensions['D'].width = 20
        ws.column_dimensions['E'].width = 28
        ws.column_dimensions['F'].width = 12
        
        history_file = DATA_DIR / "lotteri_history.xlsx"
        wb.save(history_file)
        return True
    except Exception as e:
        print(f"Feil ved eksport til Excel: {e}")
        return False

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/participants', methods=['GET'])
def get_participants():
    return jsonify({'participants': read_participants()})

@app.route('/api/participants/add', methods=['POST'])
def add_participant():
    data = request.json
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    tickets = data.get('tickets', 1)
    
    if not name or tickets < 1:
        return jsonify({'success': False, 'message': 'Ugyldig data'})
    
    participants_list = read_participants()
    participants_list.append({
        'name': name,
        'email': email,
        'tickets': int(tickets)
    })
    
    write_participants(participants_list)
    return jsonify({'success': True})

@app.route('/api/participants/clear', methods=['POST'])
def clear_participants():
    write_participants([])
    return jsonify({'success': True})

@app.route('/api/draw/start', methods=['POST'])
def start_draw():
    """Start en ny treningssesjon"""
    data = request.json
    target_draws = data.get('num_draws', 1)
    
    participants = read_participants()
    
    if not participants:
        return jsonify({'success': False, 'message': 'Ingen deltakere registrert'})
    
    wheel = create_lottery_wheel(participants)
    
    if len(wheel) < target_draws:
        return jsonify({
            'success': False,
            'message': f'Ikke nok lodd. Totalt {len(wheel)} lodd, men prøvde å trekke {target_draws}.'
        })
    
    # Reset session
    current_draw_session['participants'] = participants
    current_draw_session['wheel'] = wheel
    current_draw_session['target_draws'] = target_draws
    current_draw_session['draws_completed'] = 0
    current_draw_session['winners'] = []
    current_draw_session['used_indices'] = set()
    current_draw_session['available_wheel'] = wheel.copy()
    
    return jsonify({
        'success': True,
        'total_draws': target_draws,
        'draws_completed': 0,
        'wheel_size': len(wheel)
    })

@app.route('/api/draw/next', methods=['POST'])
def draw_next():
    """Trekk neste vinner"""
    session = current_draw_session
    
    if session['draws_completed'] >= session['target_draws']:
        return jsonify({
            'success': False,
            'message': 'Alle treninger er fullført'
        })
    
    if not session['available_wheel']:
        return jsonify({
            'success': False,
            'message': 'Ikke nok deltakere for flere treninger'
        })
    
    # Trekk random indeks
    idx = random.randint(0, len(session['available_wheel']) - 1)
    winner = session['available_wheel'][idx]
    
    session['draws_completed'] += 1
    session['winners'].append({
        'position': session['draws_completed'],
        'name': winner['name'],
        'email': winner['email'],
        'tickets': next(
            (p['tickets'] for p in session['participants'] if p['name'] == winner['name']),
            1
        )
    })
    
    # Fjern alle lodd for denne personen
    session['available_wheel'] = [
        w for w in session['available_wheel'] 
        if w['name'] != winner['name']
    ]
    
    return jsonify({
        'success': True,
        'winner': session['winners'][-1],
        'draws_completed': session['draws_completed'],
        'total_draws': session['target_draws']
    })

@app.route('/api/draw/status', methods=['GET'])
def draw_status():
    """Hent status på nåværende treningssesjon"""
    session = current_draw_session
    return jsonify({
        'draws_completed': session['draws_completed'],
        'total_draws': session['target_draws'],
        'winners': session['winners'],
        'is_active': session['target_draws'] > 0
    })

@app.route('/api/draw/save', methods=['POST'])
def save_draw():
    """Lagre treningsresultat til historikk"""
    session = current_draw_session
    
    if not session['winners']:
        return jsonify({
            'success': False,
            'message': 'Ingen vinnere å lagre'
        })
    
    # Les eksisterende historikk
    history = read_history()
    
    # Lag unik ID for denne treningen
    draw_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Legg til ny trening
    history_entry = {
        'date': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        'draw_id': draw_id,
        'winners': session['winners']
    }
    
    history.append(history_entry)
    
    # Lagre til JSON
    write_history(history)
    
    # Eksporter til Excel
    export_history_to_excel()
    
    # Reset session
    current_draw_session['target_draws'] = 0
    current_draw_session['draws_completed'] = 0
    current_draw_session['winners'] = []
    current_draw_session['available_wheel'] = []
    
    return jsonify({
        'success': True,
        'message': f'Lagret {len(session["winners"])} vinner(e) til historikk'
    })

@app.route('/api/draw/cancel', methods=['POST'])
def cancel_draw():
    """Avbryt nåværende treningssesjon"""
    current_draw_session['target_draws'] = 0
    current_draw_session['draws_completed'] = 0
    current_draw_session['winners'] = []
    current_draw_session['available_wheel'] = []
    
    return jsonify({'success': True})

@app.route('/api/history', methods=['GET'])
def get_history():
    """Hent hele historikken"""
    history = read_history()
    
    # Aggreger statistikk
    stats = {}
    for entry in history:
        for winner in entry.get('winners', []):
            name = winner['name']
            if name not in stats:
                stats[name] = {'wins': 0, 'emails': []}
            stats[name]['wins'] += 1
            if winner['email'] and winner['email'] not in stats[name]['emails']:
                stats[name]['emails'].append(winner['email'])
    
    return jsonify({
        'history': history,
        'stats': stats
    })

@app.route('/api/history/download', methods=['GET'])
def download_history():
    """Download historikk som Excel-fil"""
    export_history_to_excel()
    return jsonify({
        'success': True,
        'message': 'Historikk eksportert til lotteri_history.xlsx'
    })

# HTML-template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpareBank 1 Lotteri</title>
    <link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --ffe-farge-fjell: #002776;
            --ffe-farge-vann: #005aa4;
            --ffe-farge-sand: #f8e9dd;
            --ffe-farge-skog: #00754e;
            --ffe-farge-baer: #db3335;
            --ffe-farge-sol: #dc8000;
            --ffe-farge-koksgraa: #323232;
            --ffe-color-background-page: #f4f7fa;
            --radius-md: 4px;
            --spacing-base: 8px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Source Sans 3', sans-serif;
            background: var(--ffe-color-background-page);
            color: var(--ffe-farge-koksgraa);
            padding: 24px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: white;
            border-radius: var(--radius-md);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        }

        h1 {
            color: var(--ffe-farge-fjell);
            font-size: 36px;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #666;
            font-size: 16px;
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1.2fr 1fr;
            gap: 24px;
            margin-bottom: 40px;
        }

        .card {
            background: white;
            border-radius: var(--radius-md);
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        }

        .card h2 {
            color: var(--ffe-farge-fjell);
            font-size: 20px;
            margin-bottom: 20px;
            font-weight: 600;
        }

        .form-group {
            margin-bottom: 16px;
        }

        label {
            display: block;
            font-weight: 500;
            margin-bottom: 6px;
            font-size: 14px;
            color: var(--ffe-farge-koksgraa);
        }

        input, select {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #d0d5dd;
            border-radius: var(--radius-md);
            font-family: 'Source Sans 3', sans-serif;
            font-size: 14px;
            transition: border-color 200ms ease;
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--ffe-farge-vann);
            box-shadow: 0 0 0 3px rgba(0, 90, 164, 0.1);
        }

        .button {
            background: var(--ffe-farge-vann);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: background 200ms ease;
            font-family: 'Source Sans 3', sans-serif;
            width: 100%;
            margin-top: 8px;
        }

        .button:hover:not(:disabled) {
            background: #00437a;
        }

        .button.secondary {
            background: white;
            color: var(--ffe-farge-vann);
            border: 1px solid var(--ffe-farge-vann);
        }

        .button.secondary:hover:not(:disabled) {
            background: #f8fafc;
        }

        .button.primary {
            background: var(--ffe-farge-fjell);
        }

        .button.primary:hover:not(:disabled) {
            background: #001a47;
        }

        .button.success {
            background: var(--ffe-farge-skog);
        }

        .button.success:hover:not(:disabled) {
            background: #005a3a;
        }

        .button.danger {
            background: var(--ffe-farge-baer);
        }

        .button.danger:hover:not(:disabled) {
            background: #b82b2d;
        }

        .button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .participants-list {
            max-height: 400px;
            overflow-y: auto;
        }

        .participant-item {
            padding: 12px;
            background: #f9fafb;
            border-radius: var(--radius-md);
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
        }

        .participant-name {
            font-weight: 600;
            color: var(--ffe-farge-fjell);
        }

        .participant-tickets {
            background: var(--ffe-farge-sand);
            color: var(--ffe-farge-fjell);
            padding: 4px 8px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
        }

        .wheel-container {
            text-align: center;
            position: relative;
            min-height: 500px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        canvas {
            max-width: 100%;
            height: auto;
            filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.1));
        }

        .wheel-pointer {
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-top: 25px solid var(--ffe-farge-fjell);
            z-index: 10;
        }

        .controls {
            display: flex;
            gap: 12px;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        .controls input {
            width: 100px;
        }

        .control-buttons {
            display: flex;
            gap: 12px;
            width: 100%;
            margin-top: 8px;
        }

        .control-buttons .button {
            flex: 1;
        }

        .draw-status {
            background: #f0f4f8;
            padding: 16px;
            border-radius: var(--radius-md);
            margin-top: 16px;
            text-align: center;
        }

        .draw-status-text {
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }

        .draw-progress {
            font-size: 18px;
            font-weight: 600;
            color: var(--ffe-farge-vann);
        }

        .winners-section {
            background: var(--ffe-farge-skog);
            color: white;
            padding: 24px;
            border-radius: var(--radius-md);
            margin-top: 30px;
        }

        .winners-section h3 {
            font-size: 18px;
            margin-bottom: 16px;
            font-weight: 600;
        }

        .winner-item {
            padding: 12px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: var(--radius-md);
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .winner-position {
            font-weight: 700;
            font-size: 18px;
            min-width: 40px;
        }

        .winner-info {
            text-align: left;
            flex: 1;
            margin-left: 16px;
        }

        .winner-name {
            font-weight: 600;
        }

        .winner-email {
            font-size: 12px;
            opacity: 0.9;
        }

        .empty-state {
            color: #999;
            text-align: center;
            padding: 20px;
        }

        .error {
            color: var(--ffe-farge-baer);
            background: #fff5f5;
            padding: 12px;
            border-radius: var(--radius-md);
            margin: 12px 0;
            border-left: 4px solid var(--ffe-farge-baer);
        }

        .success {
            color: var(--ffe-farge-skog);
            background: #f0fdf4;
            padding: 12px;
            border-radius: var(--radius-md);
            margin: 12px 0;
            border-left: 4px solid var(--ffe-farge-skog);
        }

        .info {
            color: var(--ffe-farge-vann);
            background: #f0f7ff;
            padding: 12px;
            border-radius: var(--radius-md);
            margin: 12px 0;
            border-left: 4px solid var(--ffe-farge-vann);
        }

        @media (max-width: 1200px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }

        .tab-buttons {
            display: flex;
            gap: 8px;
            margin-bottom: 20px;
        }

        .tab-button {
            flex: 1;
            padding: 10px;
            border: 1px solid #d0d5dd;
            background: white;
            cursor: pointer;
            border-radius: var(--radius-md);
            font-weight: 600;
            color: var(--ffe-farge-koksgraa);
            transition: all 200ms ease;
        }

        .tab-button.active {
            background: var(--ffe-farge-vann);
            color: white;
            border-color: var(--ffe-farge-vann);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .history-entry {
            background: #f9fafb;
            padding: 12px;
            border-radius: var(--radius-md);
            margin-bottom: 12px;
            border-left: 4px solid var(--ffe-farge-vann);
        }

        .history-date {
            font-weight: 600;
            color: var(--ffe-farge-fjell);
            font-size: 13px;
            margin-bottom: 8px;
        }

        .history-winners {
            font-size: 13px;
            color: #666;
        }

        .stat-item {
            padding: 12px;
            background: #f9fafb;
            border-radius: var(--radius-md);
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .stat-name {
            font-weight: 600;
            color: var(--ffe-farge-fjell);
        }

        .stat-wins {
            background: var(--ffe-farge-sand);
            padding: 4px 8px;
            border-radius: 9999px;
            font-weight: 700;
            color: var(--ffe-farge-fjell);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎰 SpareBank 1 Lotteri</h1>
            <p class="subtitle">Trekk vinnerne en og en med animert lotterihjul</p>
        </header>

        <div class="main-content">
            <!-- Venstre: Deltaker-håndtering -->
            <div class="card">
                <h2>Deltakere</h2>
                
                <div class="tab-buttons">
                    <button class="tab-button active" onclick="switchTab('add-manual')">Legg til</button>
                    <button class="tab-button" onclick="switchTab('stats')">Statistikk</button>
                </div>

                <div id="add-manual" class="tab-content active">
                    <div class="form-group">
                        <label for="name">Navn *</label>
                        <input type="text" id="name" placeholder="Navn på deltaker">
                    </div>
                    <div class="form-group">
                        <label for="email">E-post</label>
                        <input type="email" id="email" placeholder="epost@example.com">
                    </div>
                    <div class="form-group">
                        <label for="tickets">Antall lodd *</label>
                        <input type="number" id="tickets" min="1" value="1">
                    </div>
                    <button class="button primary" onclick="addParticipant()">Legg til deltaker</button>
                </div>

                <div id="stats" class="tab-content">
                    <div style="max-height: 500px; overflow-y: auto;" id="statsContainer">
                        <p class="empty-state">Ingen historikk ennå</p>
                    </div>
                </div>

                <h3 style="margin-top: 24px; margin-bottom: 12px;">Nåværende deltakere</h3>
                <div class="participants-list" id="participantsList">
                    <p class="empty-state">Ingen deltakere ennå</p>
                </div>

                <button class="button secondary" style="margin-top: 16px;" onclick="clearAllParticipants()">Slett alle</button>
            </div>

            <!-- Senter: Lotterihjul -->
            <div class="card">
                <h2>Lotterihjul</h2>
                <div class="wheel-container">
                    <div class="wheel-pointer"></div>
                    <canvas id="wheelCanvas" width="400" height="400"></canvas>
                </div>

                <div class="controls">
                    <input type="number" id="numDraws" min="1" value="1" placeholder="Ant. gevinster" id="numdrawsInput">
                </div>

                <div id="drawMessage"></div>

                <div class="draw-status" id="drawStatus" style="display: none;">
                    <div class="draw-status-text">Treningsstatus</div>
                    <div class="draw-progress"><span id="drawProgress">0</span> / <span id="drawTotal">1</span></div>
                </div>

                <div class="control-buttons" id="controlButtonsReady">
                    <button class="button primary" onclick="startDraw()">Start treningssesjon</button>
                </div>

                <div class="control-buttons" id="controlButtonsActive" style="display: none;">
                    <button class="button primary" onclick="drawNextWinner()">Trekk neste vinner</button>
                    <button class="button secondary" onclick="cancelDraw()">Avbryt</button>
                </div>

                <div class="control-buttons" id="controlButtonsComplete" style="display: none;">
                    <button class="button success" onclick="saveDraw()">💾 Lagre vinnere</button>
                    <button class="button secondary" onclick="startNewDraw()">Ny treningssesjon</button>
                </div>
            </div>

            <!-- Høyre: Vinnerliste -->
            <div class="card">
                <h2>Vinnere</h2>
                <div id="winnersList" style="min-height: 400px;">
                    <p class="empty-state">Ingen vinnere ennå</p>
                </div>
            </div>
        </div>

        <!-- Historikk -->
        <div class="card">
            <h2>Trenings-historikk</h2>
            
            <div class="tab-buttons">
                <button class="tab-button active" onclick="switchTab('history-list')">Historikk</button>
                <button class="tab-button" onclick="switchTab('history-stats')">Statistikk</button>
            </div>

            <div id="history-list" class="tab-content active">
                <div id="historyContainer" style="max-height: 600px; overflow-y: auto;">
                    <p class="empty-state">Ingen treninger lagret ennå</p>
                </div>
                <button class="button secondary" style="margin-top: 16px; width: 100%;" onclick="downloadHistory()">
                    📥 Last ned historikk (Excel)
                </button>
            </div>

            <div id="history-stats" class="tab-content">
                <div id="historyStatsContainer" style="max-height: 600px; overflow-y: auto;">
                    <p class="empty-state">Ingen data ennå</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let participants = [];
        let currentDrawSession = null;
        let wheelRotation = 0;

        // Last data ved oppstart
        function loadParticipants() {
            fetch('/api/participants')
                .then(r => r.json())
                .then(data => {
                    participants = data.participants || [];
                    renderParticipants();
                    drawWheel();
                    updateStats();
                });
        }

        function loadHistory() {
            fetch('/api/history')
                .then(r => r.json())
                .then(data => {
                    renderHistory(data.history);
                    renderHistoryStats(data.stats);
                });
        }

        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');

            if (tabName === 'stats') updateStats();
            if (tabName === 'history-stats') loadHistory();
        }

        function addParticipant() {
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const tickets = parseInt(document.getElementById('tickets').value) || 1;

            if (!name) {
                showMessage('drawMessage', 'Skriv inn navn på deltaker', 'error');
                return;
            }

            if (tickets < 1) {
                showMessage('drawMessage', 'Antall lodd må være minst 1', 'error');
                return;
            }

            fetch('/api/participants/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, tickets })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('name').value = '';
                    document.getElementById('email').value = '';
                    document.getElementById('tickets').value = '1';
                    loadParticipants();
                    showMessage('drawMessage', '✓ Deltaker lagt til!', 'success');
                }
            });
        }

        function renderParticipants() {
            const list = document.getElementById('participantsList');
            
            if (participants.length === 0) {
                list.innerHTML = '<p class="empty-state">Ingen deltakere ennå</p>';
                return;
            }

            list.innerHTML = participants.map(p => \`
                <div class="participant-item">
                    <div>
                        <div class="participant-name">\${p.name}</div>
                        <div style="font-size: 12px; color: #666;">\${p.email || 'Ingen e-post'}</div>
                    </div>
                    <div class="participant-tickets">\${p.tickets} lodd</div>
                </div>
            \`).join('');
        }

        function clearAllParticipants() {
            if (confirm('Slett alle deltakere? Denne handlingen kan ikke gjøres om.')) {
                fetch('/api/participants/clear', { method: 'POST' })
                    .then(r => r.json())
                    .then(data => {
                        if (data.success) {
                            loadParticipants();
                            showMessage('drawMessage', '✓ Alle deltakere slettet', 'success');
                        }
                    });
            }
        }

        function drawWheel() {
            const canvas = document.getElementById('wheelCanvas');
            const ctx = canvas.getContext('2d');
            const radius = canvas.width / 2 - 10;
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (participants.length === 0) {
                ctx.font = '16px "Source Sans 3"';
                ctx.fillStyle = '#999';
                ctx.textAlign = 'center';
                ctx.fillText('Legg til deltakere', centerX, centerY);
                return;
            }

            const sliceAngle = (2 * Math.PI) / participants.length;
            const colors = ['#005aa4', '#002776', '#00754e', '#f8e9dd', '#dc8000', '#db3335'];

            participants.forEach((p, i) => {
                const startAngle = i * sliceAngle + wheelRotation;
                const endAngle = startAngle + sliceAngle;

                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, startAngle, endAngle);
                ctx.closePath();
                ctx.fillStyle = colors[i % colors.length];
                ctx.fill();

                ctx.strokeStyle = 'white';
                ctx.lineWidth = 2;
                ctx.stroke();

                const textAngle = startAngle + sliceAngle / 2;
                const textX = centerX + Math.cos(textAngle) * (radius * 0.7);
                const textY = centerY + Math.sin(textAngle) * (radius * 0.7);

                ctx.save();
                ctx.translate(textX, textY);
                ctx.rotate(textAngle + Math.PI / 2);
                ctx.font = 'bold 12px "Source Sans 3"';
                ctx.fillStyle = 'white';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'bottom';
                ctx.fillText(p.name, 0, -10);
                ctx.restore();
            });

            ctx.beginPath();
            ctx.arc(centerX, centerY, 30, 0, 2 * Math.PI);
            ctx.fillStyle = 'white';
            ctx.fill();
            ctx.strokeStyle = '#005aa4';
            ctx.lineWidth = 3;
            ctx.stroke();
        }

        function startDraw() {
            const numDraws = parseInt(document.getElementById('numDraws').value) || 1;
            
            if (participants.length === 0) {
                showMessage('drawMessage', 'Legg til minst en deltaker', 'error');
                return;
            }

            fetch('/api/draw/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ num_draws: numDraws })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    currentDrawSession = data;
                    updateDrawUI();
                    document.getElementById('drawMessage').innerHTML = \`<div class="info">📋 Trekningssesjon startet. Totalt \${numDraws} gevinst(er) å trekke.</div>\`;
                } else {
                    showMessage('drawMessage', data.message, 'error');
                }
            });
        }

        function drawNextWinner() {
            if (!currentDrawSession) return;

            fetch('/api/draw/next', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    const winner = data.winner;
                    
                    // Animasjon: Spinn hjulet
                    animateSpin(winner);
                    
                    // Oppdater UI
                    updateDrawStatus(data.draws_completed, data.total_draws);
                    
                    if (data.draws_completed >= data.total_draws) {
                        updateDrawUI('complete');
                        showMessage('drawMessage', \`✅ Alle \${data.total_draws} gevinst(er) trukket!\`, 'success');
                    }
                } else {
                    showMessage('drawMessage', data.message, 'error');
                }
            });
        }

        function animateSpin(winner) {
            let currentRotation = 0;
            const targetRotation = Math.random() * 360 + 720;
            const duration = 2000;
            const startTime = Date.now();

            function animate() {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const easeProgress = 1 - Math.pow(1 - progress, 3);
                
                wheelRotation = (targetRotation * easeProgress) * (Math.PI / 180);
                drawWheel();

                if (progress < 1) {
                    requestAnimationFrame(animate);
                }
            }

            animate();
        }

        function updateDrawStatus(completed, total) {
            document.getElementById('drawProgress').textContent = completed;
            document.getElementById('drawTotal').textContent = total;
        }

        function updateDrawUI(state = 'active') {
            const statusEl = document.getElementById('drawStatus');
            const readyBtns = document.getElementById('controlButtonsReady');
            const activeBtns = document.getElementById('controlButtonsActive');
            const completeBtns = document.getElementById('controlButtonsComplete');

            if (state === 'active') {
                statusEl.style.display = 'block';
                readyBtns.style.display = 'none';
                activeBtns.style.display = 'flex';
                completeBtns.style.display = 'none';
            } else if (state === 'complete') {
                statusEl.style.display = 'block';
                readyBtns.style.display = 'none';
                activeBtns.style.display = 'none';
                completeBtns.style.display = 'flex';
            } else {
                statusEl.style.display = 'none';
                readyBtns.style.display = 'flex';
                activeBtns.style.display = 'none';
                completeBtns.style.display = 'none';
                wheelRotation = 0;
                drawWheel();
            }
        }

        function cancelDraw() {
            if (confirm('Avbryt treningssesjon? Vinnere som er trukket vil ikke bli lagret.')) {
                fetch('/api/draw/cancel', { method: 'POST' })
                    .then(r => r.json())
                    .then(() => {
                        currentDrawSession = null;
                        updateDrawUI('idle');
                        document.getElementById('winnersList').innerHTML = '<p class="empty-state">Ingen vinnere</p>';
                        showMessage('drawMessage', 'Treningssesjon avbrutt', 'info');
                    });
            }
        }

        function saveDraw() {
            fetch('/api/draw/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    currentDrawSession = null;
                    updateDrawUI('idle');
                    loadHistory();
                    showMessage('drawMessage', '✅ ' + data.message, 'success');
                    document.getElementById('winnersList').innerHTML = '<p class="empty-state">Ingen vinnere</p>';
                }
            });
        }

        function startNewDraw() {
            currentDrawSession = null;
            updateDrawUI('idle');
            document.getElementById('winnersList').innerHTML = '<p class="empty-state">Ingen vinnere</p>';
            document.getElementById('drawMessage').innerHTML = '';
        }

        function renderHistory(history) {
            const container = document.getElementById('historyContainer');
            
            if (!history || history.length === 0) {
                container.innerHTML = '<p class="empty-state">Ingen treninger lagret ennå</p>';
                return;
            }

            container.innerHTML = history.reverse().map(entry => \`
                <div class="history-entry">
                    <div class="history-date">📅 \${entry.date}</div>
                    <div class="history-winners">
                        \${entry.winners.map((w, i) => \`
                            <div style="padding: 4px 0;">Pris \${i + 1}: <strong>\${w.name}</strong> (\${w.tickets} lodd)</div>
                        \`).join('')}
                    </div>
                </div>
            \`).join('');
        }

        function renderHistoryStats(stats) {
            const container = document.getElementById('historyStatsContainer');
            
            if (!stats || Object.keys(stats).length === 0) {
                container.innerHTML = '<p class="empty-state">Ingen statistikk ennå</p>';
                return;
            }

            const sorted = Object.entries(stats).sort((a, b) => b[1].wins - a[1].wins);

            container.innerHTML = sorted.map(([name, data]) => \`
                <div class="stat-item">
                    <div>
                        <div class="stat-name">\${name}</div>
                        <div style="font-size: 12px; color: #999;">\${data.emails.join(', ') || 'Ingen e-post'}</div>
                    </div>
                    <div class="stat-wins">\${data.wins} gevinst(er)</div>
                </div>
            \`).join('');
        }

        function updateStats() {
            loadHistory();
        }

        function downloadHistory() {
            fetch('/api/history/download')
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        showMessage('drawMessage', '✓ ' + data.message, 'success');
                    }
                });
        }

        function showMessage(elementId, message, type) {
            const el = document.getElementById(elementId);
            el.innerHTML = \`<div class="\${type}">\${message}</div>\`;
            setTimeout(() => { 
                if (el.innerHTML.includes(type)) el.innerHTML = ''; 
            }, 5000);
        }

        // Hent status ved oppstart
        fetch('/api/draw/status')
            .then(r => r.json())
            .then(data => {
                if (data.is_active) {
                    currentDrawSession = data;
                    document.getElementById('winnersList').innerHTML = data.winners.length > 0 ? 
                        '<div class="winners-section"><h3>🎉 Aktuelle vinnere:</h3>' +
                        data.winners.map(w => \`
                            <div class="winner-item">
                                <span class="winner-position">Pris \${w.position}</span>
                                <div class="winner-info">
                                    <div class="winner-name">\${w.name}</div>
                                    <div class="winner-email">\${w.email || 'Ingen e-post'}</div>
                                </div>
                            </div>
                        \`).join('') + '</div>' : '<p class="empty-state">Ingen vinnere</p>';
                    updateDrawUI(data.draws_completed >= data.total_draws ? 'complete' : 'active');
                    updateDrawStatus(data.draws_completed, data.total_draws);
                }
            });

        // Last data
        loadParticipants();
        loadHistory();

        // Oppdater historikk hvert 30. sekund
        setInterval(loadHistory, 30000);
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    init_excel_file()
    init_history_file()
    
    print("\n" + "="*60)
    print("  🎰 SpareBank 1 Lotteri - Starter applikasjonen")
    print("="*60)
    print(f"\n📁 Mappe: {SCRIPT_DIR}")
    print(f"📊 Excel-fil: {EXCEL_FILE.name}")
    print(f"📈 Historikk: {HISTORY_FILE.name}")
    print(f"\n🌐 Åpne nettleseren på: http://localhost:5000")
    print(f"\n✓ Applikasjonen kjører. Trykk CTRL+C for å stoppe.\n")
    
    app.run(debug=True, use_reloader=False, host='localhost', port=5000)
