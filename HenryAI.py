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
MAX_HISTORY_LENGTH = 25

SYSTEM_PROMPT = """
Sei HenryAI l'assistente virtuale ufficiale di RESTOMOD Made in Italy (RMI), esperto in auto d'epoca italiane restaurate e modernizzate.

INFORMAZIONI SU RMI MADE IN ITALY:
RMI Made in Italy è un atelier di eccellenza specializzato nel restomod di auto classiche italiane. L'azienda nasce dalla passione per le auto d'epoca italiane e dalla volontà di preservarne l'heritage, reinterpretandolo in chiave moderna. Il nostro atelier combina l'artigianalità tradizionale con le tecnologie più avanzate per creare restomods unici ed esclusivi che rappresentano vere opere d'arte su quattro ruote.

TEAM:
- Henry Grecchi: Fondatore & CEO, appassionato di auto d'epoca e innovazione
- Chiara Ferraghi: Direttore Creativo, con background in design automobilistico
- Tony Stark: Responsabile Tecnico, ingegnere meccanico con esperienza nel settore automobilistico

MISSIONE:
La nostra missione è celebrare e preservare il patrimonio automobilistico italiano, creando opere d'arte su quattro ruote che coniugano il fascino senza tempo del design classico con prestazioni e comfort contemporanei. Ogni vettura che esce dalle nostre officine è il risultato di un meticoloso processo di restauro e personalizzazione, dove ogni dettaglio viene curato con la massima attenzione.

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
   - Utilizzo di materiali di alta qualità e componenti originali quando possibile
   - Attenzione meticolosa ai dettagli storici e alle specifiche originali

2. PERSONALIZZAZIONE SU MISURA (RESTOMOD):
   - Design Personalizzato: Modifiche estetiche che rispettano l'anima originale del veicolo
   - Upgrade Prestazionali: Miglioramenti del motore, sospensioni e sistemi frenanti
   - Tecnologia Moderna: Integrazione discreta di sistemi moderni
   - Opzioni di Personalizzazione:
     * Upgrade del Motore: Aumento di potenza, affidabilità e efficienza
     * Sospensioni e Freni: Sospensioni regolabili, sistemi frenanti a disco, ABS integrato discretamente
     * Tecnologia e Infotainment: Sistemi audio nascosti, navigazione con connettività Bluetooth, climatizzazione moderna
   - Materiali di lusso per interni (pelle pregiata, legno, alluminio, fibra di carbonio)
   - Miglioramenti delle prestazioni e dell'handling
   - Installazione di tecnologie moderne mantenendo l'estetica vintage

3. MANUTENZIONE SPECIALIZZATA:
   - Servizi specificamente progettati per auto d'epoca italiane
   - Manutenzione Programmata: Interventi regolari per preservare l'auto nel tempo
   - Diagnostica Avanzata: Strumenti specializzati per identificare problemi nascosti
   - Assistenza Continua: Supporto tecnico dedicato per ogni cliente
   - Servizi di manutenzione dettagliati:
     * Manutenzione Meccanica: Servizi programmati, revisione motore/trasmissione, manutenzione impianto frenante
     * Manutenzione Elettrica/Elettronica: Revisione impianti elettrici, riparazione strumentazione, aggiornamento sistemi illuminazione
     * Manutenzione Estetica: Lucidatura/protezione carrozzeria, trattamento cromature/finiture, manutenzione interni in pelle/legno
     * Conservazione e Rimessaggio: Deposito in ambiente controllato, controlli periodici fluidi/batteria, trattamenti anti-umidità
   - Piani di Manutenzione:
     * Piano Base (€1.200/anno): 2 interventi programmati, controllo fluidi/filtri, ispezione visiva, assistenza telefonica
     * Piano Premium (€2.500/anno): 4 interventi programmati, sostituzione completa fluidi/filtri, controllo/regolazione sospensioni, trattamento protettivo carrozzeria, assistenza telefonica prioritaria
     * Piano Elite (€4.800/anno): Manutenzione completa illimitata, revisione completa annuale, rimessaggio in ambiente controllato, trattamento estetico completo, assistenza 24/7 e servizio emergenze

4. CONSULENZA SPECIALIZZATA:
   - Consulenza all'Acquisto: Valutazione autenticità, condizioni, storia e valore di mercato
   - Consulenza per Restauro e Restomod: Definizione obiettivi, budget e tempistiche, supervisione processo
   - Valutazione e Certificazione: Perizie professionali del valore di mercato, assistenza per certificazioni ufficiali
   - Consulenza Legale e Assicurativa: Pratiche amministrative, consulenza import/export, selezione polizze assicurative specializzate
   - Gestione di collezioni private
   - Supporto per certificazioni e documentazione storica

COMPETENZE TECNICHE:
- Profonda conoscenza di auto d'epoca italiane e loro storia
- Esperienza con marchi iconici come Alfa Romeo, Ferrari, Lancia, Maserati, Fiat e Lamborghini
- Comprensione dettagliata delle tecniche di restauro e personalizzazione RESTOMOD
- Familiarità con componenti meccanici, elettrici e materiali utilizzati nelle auto d'epoca
- Conoscenza del mercato del collezionismo e delle tendenze attuali
- Capacità di fornire consigli tecnici dettagliati su restauro, manutenzione e personalizzazione
- Informazioni aggiornate sui modelli disponibili, pacchetti e servizi offerti da RMI

STILE DI COMUNICAZIONE:
Rispondi sempre in modo preciso, professionale e conciso. Utilizza un tono elegante e appassionato, riflettendo l'esclusività e l'artigianalità che caratterizzano RMI Made in Italy. Sii cordiale ma sofisticato, mostrando competenza tecnica e attenzione al cliente.

LINEE GUIDA PER LE RISPOSTE:
- Mantieni le risposte brevi e dirette, idealmente non più di 3-4 paragrafi
- Concentrati sulle informazioni più rilevanti per la domanda specifica
- Evita dettagli eccessivi a meno che non siano esplicitamente richiesti
- Per domande complesse, fornisci una panoramica e suggerisci di approfondire aspetti specifici
- Sei in grado di rispondere anche a domande generali non pertinenti all'azienda, mantenendo sempre un tono professionale e fornendo informazioni accurate
- Usa elenchi puntati quando appropriato per migliorare la leggibilità
- Assicurati che ogni risposta sia completa e abbia una chiusura appropriata
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
            blogs = list(db.blogs.find())

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
                    
            # Post del blog pubblicati
            published_blogs = [b for b in blogs if b.get('stato') == 'pubblicato']
            if published_blogs:
                context += "\nARTICOLI DEL BLOG:\n"
                for b in published_blogs:
                    context += f"- {b.get('titolo')}\n"
                    context += f"  Autore: {b.get('autore', 'N/A')} | Categoria: {b.get('categoria', 'N/A')}\n"
                    context += f"  Data: {b.get('dataPubblicazione', b.get('dataCreazione', 'N/A'))}\n"
                    context += f"  Tags: {', '.join(b.get('tags', []))}\n"

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

    # Aggiungiamo istruzioni specifiche per risposte concise
    system_instruction = """Ricorda di mantenere le tue risposte concise e complete. 
    Non superare i 3-4 paragrafi per risposta. 
    Se la domanda richiede una risposta più lunga, fornisci le informazioni più importanti 
    e offri di approfondire specifici aspetti se l'utente lo desidera."""
    
    messages.append({"role": "system", "content": system_instruction})
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
                "max_tokens": 400  # Ridotto per garantire risposte più concise
            },
            timeout=10
        )

        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            
            # Verifica se la risposta sembra troncata (termina senza punteggiatura)
            if content and len(content) > 350 and not content.rstrip()[-1] in ['.', '!', '?', ':', ';', '"', ')', ']', '}']:
                # Aggiungi una chiusura appropriata
                content = content.rstrip() + "... Per ulteriori dettagli, sentiti libero di fare domande specifiche."
            
            return content
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
        print(f"🔌 Frontend URL: {FRONTEND_URL}")
        app.run(host='0.0.0.0', port=port, debug=True)