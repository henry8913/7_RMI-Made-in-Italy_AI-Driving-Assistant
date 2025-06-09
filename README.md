
<h1 align="center"> 
  <img src="https://readme-typing-svg.herokuapp.com/?font=Iosevka&size=30&color=d4af37&center=true&vCenter=true&width=800&height=60&lines=🤖+RMI+Made+in+Italy+-+AI+Driving+Assistant&repeat=false" alt="🤖 RMI Made in Italy - AI Driving Assistant"> 
</h1> 

**HenryAI** è un assistente virtuale intelligente specializzato nel mondo delle auto d'epoca italiane restaurate e modernizzate. Questo servizio basato su Flask fornisce un'esperienza conversazionale avanzata per supportare clienti e appassionati con informazioni dettagliate sui servizi e prodotti di RMI Made in Italy. 

<p align="center"> 
  <img src="./img/cover_a.jpg" alt="Cover" width="100%" /> 
</p> 

Questo progetto implementa un'interfaccia conversazionale basata su modelli linguistici avanzati, integrata con il database aziendale per fornire risposte accurate e personalizzate. L'assistente è progettato per offrire un'esperienza utente premium che riflette l'eccellenza e l'artigianalità del brand RMI Made in Italy. 

### Tecnologie Principali: 
- **Python**: Linguaggio di programmazione versatile e potente 
- **Flask**: Framework web leggero per API REST 
- **OpenRouter API**: Accesso a modelli linguistici avanzati 
- **MongoDB**: Database NoSQL per la persistenza delle conversazioni 
- **Flask-CORS**: Gestione delle richieste cross-origin 
- **Python-dotenv**: Gestione variabili d'ambiente 
- **Requests**: Libreria HTTP per comunicazione con API esterne 

## 🧠 Architettura AI 

<p align="center"> 
  <img src="./img/cover_b.jpg" alt="AI Architecture" width="100%" /> 
</p> 

--- 

## 📌 Funzionalità Principali 
- 💬 **Conversazione Naturale**: Interazione fluida e contestuale 
- 🚗 **Expertise Automobilistico**: Conoscenza approfondita di auto d'epoca italiane 
- 🔍 **Informazioni Dettagliate**: Dati tecnici su restauro e personalizzazione 
- 📋 **Assistenza Servizi**: Supporto per tutti i servizi offerti da RMI 
- 🧰 **Consulenza Tecnica**: Consigli su restauro, manutenzione e personalizzazione 
- 📅 **Supporto Prenotazioni**: Assistenza per test drive e appuntamenti 
- 💼 **Informazioni Aziendali**: Dettagli su team, missione e valori 
- 🌐 **Integrazione Web**: Facilmente integrabile nel sito web aziendale 
- 📱 **Responsive Design**: Funziona su desktop e dispositivi mobili 

--- 

## 🧩 Capacità e Competenze dell'Assistente

HenryAI rappresenta l'eccellenza nell'assistenza virtuale per il settore automotive di lusso, combinando intelligenza artificiale avanzata con una profonda conoscenza del patrimonio automobilistico italiano.

### 🏢 DNA Aziendale
- **Heritage & Visione**: Profonda conoscenza del DNA di RMI Made in Italy, della sua storia e dei suoi valori fondamentali
- **Expertise Premium**: Padronanza completa della gamma di servizi di restauro e restomod di alta gamma
- **Team & Competenze**: Comprensione approfondita delle specializzazioni e dell'expertise del team RMI

### 🛠️ Portfolio Servizi
- **Restauro Heritage**: Interventi specializzati su auto d'epoca di prestigio
- **Restomod Innovation**: Soluzioni personalizzate che fondono tradizione e tecnologia moderna
- **Manutenzione Elite**: Servizi di manutenzione dedicati per vetture classiche e restomod
- **Consulenza Strategica**: Supporto esperto per progetti di restauro e valorizzazione

### 🎯 Expertise Tecnico
- **Heritage Italiano**: Conoscenza approfondita della storia dell'automobile italiana
- **Marchi Leggendari**: Expertise specifica sui più prestigiosi costruttori italiani
- **Metodologie Avanzate**: Padronanza delle più moderne tecniche di restauro e customizzazione
- **Engineering**: Competenza completa su sistemi meccanici ed elettrici vintage e moderni
- **Market Intelligence**: Analisi aggiornate del mercato del collezionismo d'auto

### 🔍 Capacità Distintive
- **Consulenza Personalizzata**: Analisi e raccomandazioni su misura per ogni progetto
- **Supporto Tecnico**: Assistenza dettagliata su specifiche tecniche e soluzioni
- **Gestione Progetti**: Guida attraverso l'intero processo di restauro o restomod
- **Valorizzazione**: Strategie per massimizzare il valore dell'investimento

> Per approfondimenti tecnici e dettagli sui parametri di addestramento dell'AI, consultare il codice sorgente.

--- 

## 📂 Struttura del Progetto 
``` 
├── HenryAI.py         # File principale dell'applicazione 
├── .env.example       # Template per variabili d'ambiente 
├── Procfile           # Configurazione per deployment 
├── requirements.txt   # Dipendenze Python 
└── img/               # Risorse immagini 
``` 

## ⚙️ Architettura del Sistema 

### Componenti Principali: 
- **Flask Server**: Gestisce le richieste HTTP e le risposte 
- **Conversation Handler**: Mantiene il contesto delle conversazioni 
- **AI Integration**: Comunica con l'API OpenRouter per generare risposte 
- **Knowledge Base**: Sistema di prompt engineering con informazioni specifiche 

### Flusso di Elaborazione: 
1. L'utente invia un messaggio tramite l'interfaccia web 
2. Il server Flask riceve la richiesta e recupera la cronologia della conversazione 
3. Il messaggio e il contesto vengono inviati all'API OpenRouter 
4. Il modello AI genera una risposta basata sul prompt di sistema e l'input utente 
5. La risposta viene restituita all'utente e la conversazione viene aggiornata 

--- 

## 🚀 Setup Locale 
```bash 
# Clona il repository 
git clone https://github.com/henry8913/7_RMI-Made-in-Italy_AI-Driving-Assistant.git 
cd 7_Capstone-Project_RMI-Made-in-Italy/"AI Driving Assistant" 

# Crea e attiva un ambiente virtuale (opzionale ma consigliato) 
python -m venv venv 
source venv/bin/activate  # Per Windows: venv\Scripts\activate 

# Installazione dipendenze 
pip install -r requirements.txt 

# Configurazione ambiente 
cp .env.example .env 
# Modifica il file .env con le tue configurazioni 

# Avvio server di sviluppo 
python HenryAI.py 
``` 

## 🔧 Variabili d'Ambiente Richieste 
```env 
OPENROUTER_API_KEY=your_openrouter_api_key 
BACKEND_URL=http://localhost:2025 
FRONTEND_URL=http://localhost:5173 
``` 

## 🔄 Integrazione con il Frontend 

L'assistente può essere facilmente integrato nel frontend React tramite API REST: 

```javascript 
// Esempio di integrazione nel frontend 
async function sendMessage(message) { 
  try { 
    const response = await axios.post('http://localhost:5001/chat', { 
      user_id: 'user123', 
      message: message 
    }); 
    
    return response.data.response; 
  } catch (error) { 
    console.error('Errore durante l'invio del messaggio:', error); 
    return 'Si è verificato un errore nella comunicazione con l\'assistente.'; 
  } 
} 
``` 

## ⚠️ Nota Importante 
Questo è un progetto dimostrativo. L'assistente AI è progettato per fornire informazioni sui prodotti e servizi di RMI Made in Italy, ma non sostituisce la consulenza professionale diretta. 

## 👤 Autore

Progetto creato da [Henry](https://github.com/henry8913).

## 📫 Contatti

<div align="center">

[![Website](https://img.shields.io/badge/-Website-000000?style=for-the-badge&logo=web&logoColor=white)](https://henrygdeveloper.com/)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/henry-k-grecchi-555454254)
[![Email](https://img.shields.io/badge/-Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:henry8913@hotmail.it)
[![WhatsApp](https://img.shields.io/badge/-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://api.whatsapp.com/send/?phone=393926936916&text&type=phone_number&app_absent=0)

</div>

<img src="./img/h_cover.jpg" alt="Cover" width="100%" />

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza [GNU GPLv3](LICENSE.txt).
