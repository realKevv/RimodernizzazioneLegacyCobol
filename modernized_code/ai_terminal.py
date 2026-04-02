import os
import sys
import sqlite3
from dotenv import load_dotenv
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from langchain_mistralai import ChatMistralAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()

DB_PATH = "accounting.db"
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@tool
def get_products() -> str:
    """Visualizza l'elenco completo dei prodotti e lo stock nel magazzino."""
    try:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM products").fetchall()
            if not rows: return "Magazzino vuoto."
            return "\n".join([f"ID: {r['product_id']} | {r['name']} | €{r['price']} | Stock: {r['stock']}" for r in rows])
    except Exception as e:
        return f"Errore DB: {str(e)}"

@tool
def process_purchase(product_id: int, qty: int) -> str:
    """Esegue un ordine, calcola il totale e scala lo stock."""
    try:
        with get_db() as conn:
            p = conn.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
            if not p or p['stock'] < qty: 
                return "Errore: Prodotto non trovato o stock insufficiente."
            total = p['price'] * qty
            conn.execute("INSERT INTO orders (product_id, quantity, total_price) VALUES (?, ?, ?)", (product_id, qty, total))
            conn.execute("UPDATE products SET stock = stock - ? WHERE product_id = ?", (qty, product_id))
            conn.commit()
            return f"Successo! Venduti {qty}x {p['name']}. Totale: €{total:.2f}."
    except Exception as e:
        return f"Errore DB: {str(e)}"

print("🔄 Inizializzazione Rete Neurale Mistral in corso...")
# 1. Inizializziamo l'IA
llm = ChatMistralAI(model="mistral-small-latest", temperature=0)
tools = [get_products, process_purchase]

# 2. Parametri posizionali
agent_app = create_react_agent(llm, tools=tools, prompt="Sei un magazziniere robotico. Usa SUBITO i tool e NON chiedere mai conferme.")

print("==================================================")
print(" 🤖 WAREHOUSE AI TERMINAL ATTIVO")
print(" Scrivi 'esci' per chiudere il programma")
print("==================================================\n")

while True:
    try:
        user_input = prompt(HTML("<b><ansicyan>Tu 👤:</ansicyan></b> "))
        if user_input.lower() in ['esci', 'exit', 'quit']: break
        if not user_input.strip(): continue

        response = agent_app.invoke({"messages": [HumanMessage(content=user_input)]})

        print(f"\n🤖 AI: \033[93m{response['messages'][-1].content}\033[0m\n")
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Errore di sistema: {e}")
