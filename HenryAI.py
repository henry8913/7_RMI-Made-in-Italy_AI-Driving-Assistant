import os
import requests
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BACKEND_URL = os.getenv("BACKEND_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL")

app = Flask(__name__)
# Modifica della configurazione CORS per consentire richieste da qualsiasi origine durante lo sviluppo
CORS(app, resources={r"/*": {"origins": "*"}})

conversation_history = {}
MAX_HISTORY_LENGTH = 15

SYSTEM_PROMPT = """
Sei HenryAI l'assistente virtuale ufficiale di RESTOMOD Made in Italy (RMI), esperto in auto d'epoca restaurate e modernizzate.

INFORMAZIONI SU RMI MADE IN ITALY:
RMI Made in Italy è un atelier di eccellenza specializzato nel restomod di auto classiche italiane. L'azienda nasce dalla passione per le auto d'epoca italiane e dalla volontà di preservarne l'heritage, reinterpretandolo in chiave moderna. Il nostro atelier combina l'artigianalità tradizionale con le tecnologie più avanzate per creare restomods unici ed esclusivi.

MISSIONE:
La nostra missione è mantenere vivo il patrimonio automobilistico italiano, creando opere d'arte su quattro ruote che coniugano il fascino senza tempo del design classico con prestazioni e comfort contemporanei.

VALORI FONDAMENTALI:
- Qualità: Collaboriamo solo con i migliori costruttori italiani, garantendo standard di eccellenza in ogni veicolo.
- Artigianato: Valorizziamo l'artigianato italiano, dove ogni dettaglio è curato con passione e maestria.
- Innovazione: Uniamo la tradizione con le tecnologie moderne, rispettando il passato ma guardando al futuro.

SERVIZI OFFERTI:
1. RESTAURO DI ECCELLENZA:
   - Restauro completo di auto d'epoca italiane
   - Tecniche tradizionali combinate con tecnologie moderne
   - Rispetto dell'autenticità e della storia del veicolo
   - Documentazione completa del processo di restauro

2. PERSONALIZZAZIONE SU MISURA:
   - Modifiche estetiche e funzionali personalizzate
   - Aggiornamenti di interni con materiali di lusso
   - Miglioramenti delle prestazioni e dell'handling
   - Installazione di tecnologie moderne (infotainment, climatizzazione, etc.)

3. MANUTENZIONE SPECIALIZZATA:
   - Servizi di manutenzione per auto d'epoca e restomod
   - Diagnosi avanzata e risoluzione problemi
   - Revisioni periodiche e preparazione per eventi
   - Conservazione e protezione a lungo termine

4. CONSULENZA SPECIALIZZATA:
   - Valutazione e autenticazione di auto d'epoca
   - Consulenza per acquisto e vendita
   - Gestione di collezioni private
   - Supporto per certificazioni e documentazione storica

Le tue competenze includono:
- Profonda conoscenza di auto d'epoca e restauri
- Comprensione delle modifiche e personalizzazioni RESTOMOD
- Familiarità con i costruttori italiani di eccellenza
- Capacità di fornire consigli tecnici dettagliati
- Conoscenza dei processi di restauro e modernizzazione

Rispondi sempre in modo preciso, professionale e immediato. Utilizza un tono elegante e appassionato, riflettendo l'esclusività e l'artigianalità che caratterizzano RMI Made in Italy.
"""

def update_conversation_history(session_id, role, content):
    if session_id not in conversation_history:
        conversation_history[session_id] = []    
    conversation_history[session_id].append({"role": role, "content": content})
    
    # Mantieni solo gli ultimi MAX_HISTORY_LENGTH messaggi
    if len(conversation_history[session_id]) > MAX_HISTORY_LENGTH * 2:  # *2 perché ogni scambio ha 2 messaggi
        conversation_history[session_id] = conversation_history[session_id][-MAX_HISTORY_LENGTH * 2:]

from pymongo import MongoClient

# Connessione MongoDB
mongodb_url = os.getenv("MONGODB_URL")
if not mongodb_url:
    print("⚠️ Errore: MONGODB_URL non trovato nel file .env")
    exit(1)

try:
    client = MongoClient(mongodb_url)
    db = client.get_default_database()
    print("✅ Connessione MongoDB stabilita con successo")
except Exception as e:
    print(f"❌ Errore connessione MongoDB: {e}")
    exit(1)

def get_enriched_context():
    try:
        context = "\nDati aggiornati dal database:\n"

        try:
            # Recupero completo dei dati da MongoDB
            modelli = list(db.restomods.find())
            costruttori = list(db.brands.find())
            packages = list(db.packages.find())
            testdrives = list(db.testdrives.find())
            jobs = list(db.jobs.find())

            # Aggiungo informazioni dettagliate sui modelli disponibili
            available_models = [m for m in modelli if m.get('stato') == 'available']
            if available_models:
                context += "\nMODELLI DISPONIBILI:\n"
                for m in available_models:
                    context += f"- {m.get('nome')} ({m.get('anno')})\n"
                    context += f"  Prezzo: €{m.get('prezzo', 'N/A'):,} | Stato: {m.get('stato', 'N/A')}\n"
                    if 'specifiche' in m:
                        specs = m['specifiche']
                        context += f"  Motore: {specs.get('motore', 'N/A')} | Potenza: {specs.get('potenza', 'N/A')}\n"
                    context += f"  Caratteristiche: {', '.join(m.get('caratteristiche', []))}\n"

            # Informazioni sui costruttori
            if costruttori:
                context += "\nCOSTRUTTORI:\n"
                for c in costruttori:
                    context += f"- {c.get('nome')} | Fondazione: {c.get('annoFondazione', 'N/A')}\n"
                    context += f"  Sede: {c.get('sede', 'N/A')}\n"

            # Pacchetti disponibili
            if packages:
                context += "\nPACCHETTI DISPONIBILI:\n"
                for p in packages:
                    context += f"- {p.get('nome')}: €{p.get('prezzo', 'N/A'):,}\n"

            # Posizioni lavorative aperte
            active_jobs = [j for j in jobs if j.get('attivo', True)]
            if active_jobs:
                context += "\nPOSIZIONI APERTE:\n"
                for j in active_jobs:
                    context += f"- {j.get('titolo')} ({j.get('tipo')}) | {j.get('luogo')}\n"

        except Exception as e:
            print(f"Errore recupero dati MongoDB: {e}")
            return "Mi dispiace, al momento non riesco ad accedere alle informazioni del database."

        return context
    except Exception as e:
        print(f"Errore recupero dati: {e}")
        return ""

def ask_openrouter(prompt, session_id):
    context = get_enriched_context()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if session_id in conversation_history:
        messages.extend(conversation_history[session_id])

    messages.append({"role": "user", "content": f"{prompt}\n\n{context}"})

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-3-haiku",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=10
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "Mi dispiace, al momento non riesco a rispondere. Riprova più tardi."

    except Exception as e:
        print(f"Errore API: {e}")
        return "Mi dispiace, c'è stato un problema nella comunicazione. Riprova tra poco."

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('message', '')
    session_id = data.get('session_id', 'default')

    if not prompt:
        return jsonify({"status": "error", "message": "Messaggio vuoto"}), 400

    response = ask_openrouter(prompt, session_id)

    update_conversation_history(session_id, "user", prompt)
    update_conversation_history(session_id, "assistant", response)

    return jsonify({"status": "success", "answer": response})

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "status": "online",
        "message": "RMI AI Assistant è attivo e pronto a rispondere",
        "backend_url": BACKEND_URL
    })

@app.route('/api/test', methods=['POST'])
def test_chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Missing message"}), 400

    message = data['message']
    session_id = data.get('session_id', 'test_session')

    response = ask_openrouter(message, session_id)

    update_conversation_history(session_id, "user", message)
    update_conversation_history(session_id, "assistant", response)

    return jsonify({
        "status": "success",
        "answer": response,
        "session_id": session_id
    })

def run_test_mode():
    print("\n🤖 RMI AI Assistant Test Mode")
    print("🔌 Connessione al backend:", os.getenv("BACKEND_URL", "http://0.0.0.0:2025"))
    print("Scrivi 'exit' per uscire\n")

    session_id = 'test_session'

    # Test connessione backend
    try:
        context = get_enriched_context()
        if context:
            print("✅ Backend connesso e dati recuperati")
        else:
            print("⚠️ Backend connesso ma nessun dato recuperato")
    except Exception as e:
        print(f"❌ Errore connessione backend: {e}")

    while True:
        user_input = input("\nTu: ")
        if user_input.lower() == 'exit':
            break

        response = ask_openrouter(user_input, session_id)
        print("\nAssistant:", response)

        update_conversation_history(session_id, "user", user_input)
        update_conversation_history(session_id, "assistant", response)

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_test_mode()
    else:
        port = int(os.environ.get("PORT", 5001))
        print(f"\n🤖 RMI AI Assistant è online sulla porta {port}!")
        print(f"🔌 Backend URL: {BACKEND_URL}")
        app.run(host='0.0.0.0', port=port, debug=True)