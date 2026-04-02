# Sistema di Gestione Acquisti e Contabilità

## Descrizione del Sistema
Questo sistema è una **riprogettazione moderna** di un sistema COBOL legacy, sviluppato in Python con un'architettura basata su classi e un database SQLite. Il sistema è composto da due moduli principali:
1. **`accounting_system.py`**: Gestisce le operazioni amministrative (autenticazione, gestione prodotti, calcoli contabili).
2. **`buyroutine.py`**: Gestisce la logica degli ordini e dei calcoli finanziari (selezione prodotti, totale, resto).

Il sistema rispetta i **vincoli originali** del COBOL, ma introduce miglioramenti come:
- **Gestione centralizzata dei dati** tramite database SQLite.
- **Validazione dei dati** per evitare errori di input.
- **Crittografia delle password** per l'autenticazione amministratore.
- **Generazione automatica delle ricevute** in formato testuale.

---

## Struttura Modulare

### 1. `accounting_system.py`
**Ruolo**: Modulo amministrativo che gestisce:
- Autenticazione dell'amministratore.
- Aggiunta, eliminazione e visualizzazione dei prodotti.
- Calcolo del salario orario (tariffa fissa: 500 PHP).
- Calcolo del profitto (prezzo di vendita - costo dei beni).

**Classi Principali**:
- **`AccountingSystem`**:
  - **Metodi**:
    - `authenticate_admin()`: Verifica le credenziali dell'amministratore (email: `robby@gmail.com`, password crittografata).
    - `add_product()`: Aggiunge un nuovo prodotto al database (validando `product_id`, `name`, `price`).
    - `delete_product()`: Elimina un prodotto dal database.
    - `calculate_salary()`: Calcola il salario orario (`salary = 500 * hours_worked`).
    - `calculate_profit()`: Calcola il profitto (`profit = selling_price - cogs`).
  - **Menu Testuale**:
    - Opzioni: Calcolo Salario, Modifica Prodotti, Calcolo Profitto, Torna al Menu Principale.

---

### 2. `buyroutine.py`
**Ruolo**: Modulo per la gestione degli ordini e dei calcoli finanziari.
- Selezione dei prodotti da parte dell'utente.
- Calcolo del totale dell'ordine.
- Calcolo del resto (differenza tra importo pagato e totale).
- Generazione di una ricevuta testuale.

**Classi Principali**:
- **`BuyRoutine`**:
  - **Metodi**:
    - `select_products()`: Gestisce la selezione dei prodotti (numero di prodotti, codice prodotto, quantità).
    - `calculate_total()`: Calcola il totale dell'ordine (`total = sum(price * quantity)`).
    - `calculate_change()`: Calcola il resto (`change = money_paid - total`).
    - `generate_receipt()`: Genera una ricevuta con i dettagli dell'ordine (prodotti, totale, resto, data).
  - **Menu Testuale**:
    - Opzioni: Acquista Prodotti, Torna al Menu Principale.

---

### 3. `data_model/`
**Ruolo**: Modulo per la gestione del database SQLite.
- **`migrate_data.py`**: Script per inizializzare il database e applicare lo schema.
- **`schema.sql`**: Schema del database con le tabelle `products` e `orders`.

**Schema del Database**: