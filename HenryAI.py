
import os
import requests
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_henry_response(user_message):
    """Invia il messaggio a OpenRouter e riceve la risposta di HenryAI"""
    
    if not OPENROUTER_API_KEY:
        return "❌ Errore: OPENROUTER_API_KEY non configurata nel file .env"
    
    # System prompt per HenryAI
    system_prompt = """
    Ciao! Sono HenryAI, un web developer che sta lavorando al sito di RMI Restomod Made in Italy.
    
    Mi occupo di:
    - Sviluppare il sito web per RMI Restomod Made in Italy
    - Creare contenuti digitali per auto d'epoca restaurate e modernizzate
    - Programmare funzionalità innovative per la piattaforma
    - Gestire l'integrazione tra tradizione automotive italiana e tecnologia moderna
    - Costruire l'esperienza utente perfetta per gli appassionati di restomod
    
    Sono sempre disponibile per parlare del progetto RMI e delle auto d'epoca italiane che stiamo digitalizzando!
    Parlo sempre in prima persona come Henry, il web developer del team.
    Rispondi sempre in modo amichevole e professionale.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
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
                "max_tokens": 300
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ Errore API: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"❌ Errore di connessione: {e}"

def main():
    print("🤖 Ciao! Sono HenryAI!")
    print("👨‍💻 Sono un web developer che sta preparando il sito per RMI Restomod Made in Italy.")
    print("🚗 Mi occupo di creare una piattaforma digitale per auto d'epoca restaurate e modernizzate.")
    print("🇮🇹 Il progetto RMI unisce la tradizione automotive italiana con la tecnologia moderna.")
    print("🔧 Sto sviluppando funzionalità innovative per mostrare il meglio del restomod italiano!")
    print("\n💬 Ora puoi chattare con me! Scrivi 'exit' per uscire.\n")
    
    while True:
        user_input = input("Tu: ")
        
        if user_input.lower() in ['exit', 'quit', 'esci']:
            print("\n👋 Grazie per aver chattato con me! A presto! 😊")
            break
        
        if user_input.strip() == "":
            continue
            
        print("🤔 HenryAI sta pensando...")
        response = get_henry_response(user_input)
        print(f"\n🤖 HenryAI: {response}\n")

if __name__ == "__main__":
    main()