# 🚀 Legacy-to-AI Modernization Pipeline
### Dai Sistemi COBOL anni '80 a un Ecosistema Multi-Agente Intelligente (MCP)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![LangGraph](https://img.shields.io/badge/Framework-LangGraph-orange?style=for-the-badge)
![Mistral](https://img.shields.io/badge/AI-Mistral-red?style=for-the-badge)
![MCP](https://img.shields.io/badge/Protocol-MCP-green?style=for-the-badge)

## 📌 Visione del Progetto
Questo progetto dimostra la trasformazione di un sistema gestionale legacy (scritto in **COBOL**) in un'applicazione moderna basata su micro-servizi AI. Non si tratta di una semplice traduzione di sintassi, ma di una **reingegnerizzazione cognitiva** che estrae logica di business e la rende accessibile tramite linguaggio naturale.

---

## 🏗️ Architettura del Sistema

### 1. Il Team di Agenti (Powered by LangGraph)
Il processo di migrazione è orchestrato da un grafo a stati che simula un team di sviluppo software:
* **Analyst Agent**: Estrae le regole matematiche e i vincoli dai moduli COBOL (`ACCOUNTING_SYSTEM.COB`).
* **Data Engineer**: Gestisce la bonifica dei file a larghezza fissa e la migrazione su **SQLite**.
* **Architect & Coder**: Progettano e scrivono il codice Python seguendo i principi **OOP**.
* **QA Engineer**: Esegue test iterativi per garantire la coerenza tra il vecchio e il nuovo sistema.

### 2. Protocollo MCP (Model Context Protocol)
Abbiamo implementato lo standard **MCP** per permettere a modelli linguistici (LLM) di interagire in modo sicuro e strutturato con il database locale, trasformando i dati statici in una risorsa dinamica.

---

## 📂 Struttura del Repository
* `📂 legacy_code/`: Contiene i sorgenti COBOL originali e i database testuali (`.txt`).
* `📂 modernized_code/`: Il nuovo sistema Python con database relazionale.
    * `ai_terminal.py`: Interfaccia conversazionale per la gestione del magazzino.
    * `accounting.db`: Database SQLite modernizzato.
* `📄 app.py`: Il notebook **Marimo** che gestisce l'intero grafo degli agenti.
* `📄 mlflow.db`: Tracciamento dei ragionamenti dell'IA tramite **MLflow**.

---

## 🚀 Come Iniziare

### Prerequisiti
* Python 3.10+
* Chiave API Mistral AI

### Installazione
1.  Clona il repository:
    ```bash
    git clone [https://github.com/realKevv/RimodernizzazioneLegacyCobol.git](https://github.com/realKevv/RimodernizzazioneLegacyCobol.git)
    cd RimodernizzazioneLegacyCobol
    ```
2.  Crea l'ambiente virtuale e installa le dipendenze:
    ```bash
    python -m venv venv
    ./venv/Scripts/activate
    pip install -r modernized_code/requirements_ai.txt
    ```
3.  Configura le credenziali:
    Crea un file `.env` nella cartella `modernized_code/` e aggiungi:
    ```env
    MISTRAL_API_KEY=tua_chiave_qui
    ```

### Utilizzo del Terminale AI
Per interagire con il magazzino usando l'intelligenza artificiale:
```bash
cd modernized_code
python ai_terminal.py
