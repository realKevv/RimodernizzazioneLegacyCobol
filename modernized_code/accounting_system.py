import sqlite3
import bcrypt
import sys

DB_PATH = 'accounting.db'
HOURLY_RATE = 500.0
ADMIN_EMAIL = 'robby@gmail.com'
_ADMIN_HASH = bcrypt.hashpw(b'robby@123', bcrypt.gensalt())


def get_connection():
    """Restituisce una connessione al database SQLite con row_factory configurato."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inizializza il database creando le tabelle se non esistono."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL CHECK (price > 0),
                stock INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                total_price REAL NOT NULL CHECK (total_price > 0),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS admin_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_hash BLOB NOT NULL
            )
        """)
        conn.commit()


def login() -> bool:
    """Gestisce l'autenticazione dell'amministratore.
    
    Ritorna True se l'autenticazione ha successo, False altrimenti.
    """
    email = input("Inserisci l'email amministratore: ").strip()
    password = input("Inserisci la password: ").strip().encode('utf-8')
    
    if email != ADMIN_EMAIL:
        print("Email errata. Accesso negato.")
        return False
    
    try:
        with get_connection() as conn:
            admin_hash = conn.execute("SELECT admin_hash FROM admin_credentials LIMIT 1").fetchone()
            if admin_hash is None:
                print("Nessun hash amministratore trovato nel database. Accesso negato.")
                return False
            stored_hash = admin_hash['admin_hash']
        
        if bcrypt.checkpw(password, stored_hash):
            print("Accesso consentito.")
            return True
        else:
            print("Password errata. Accesso negato.")
            return False
    except Exception as e:
        print(f"Errore durante l'autenticazione: {e}")
        return False


def calcola_stipendio():
    """Calcola lo stipendio orario di un impiegato."""
    try:
        nome = input("Inserisci il nome dell'impiegato: ").strip()
        ore_lavorate = float(input("Inserisci le ore lavorate: ").strip())
        
        if ore_lavorate <= 0:
            print("Le ore lavorate devono essere positive.")
            return
        
        stipendio = HOURLY_RATE * ore_lavorate
        print(f"Stipendio per {nome}: {stipendio:.2f} PHP")
    except ValueError:
        print("Input non valido. Assicurati di inserire un numero per le ore lavorate.")


def calcola_profitto():
    """Calcola il profitto dato il prezzo di vendita e il costo dei beni venduti."""
    try:
        cogs = float(input("Inserisci il costo dei beni venduti (COGS): ").strip())
        selling_price = float(input("Inserisci il prezzo di vendita: ").strip())
        
        if cogs <= 0 or selling_price <= 0:
            print("I valori devono essere positivi.")
            return
        
        profitto = selling_price - cogs
        print(f"Profitto: {profitto:.2f} PHP")
    except ValueError:
        print("Input non valido. Assicurati di inserire numeri validi.")


def stampa_prodotti():
    """Stampa tutti i prodotti disponibili nel database."""
    with get_connection() as conn:
        prodotti = conn.execute("SELECT product_id, name, price, stock FROM products").fetchall()
    
    if not prodotti:
        print("Nessun prodotto disponibile.")
        return
    
    print("\nElenco prodotti:")
    print("ID	Nome		Prezzo	Stock")
    print("-" * 50)
    for p in prodotti:
        print(f"{p['product_id']}\t{p['name']}\t{p['price']:.2f}\t{p['stock']}")
    print("-" * 50)
    print(f"Totale prodotti: {len(prodotti)}\n")


def aggiungi_prodotto():
    """Aggiunge un nuovo prodotto al database."""
    try:
        nome = input("Inserisci il nome del prodotto: ").strip()
        prezzo = float(input("Inserisci il prezzo del prodotto: ").strip())
        stock = int(input("Inserisci la quantità in stock: ").strip())
        
        if prezzo <= 0 or stock < 0:
            print("Prezzo e stock devono essere validi (prezzo > 0, stock >= 0).")
            return
        
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
                (nome, prezzo, stock)
            )
            conn.commit()
        print("Prodotto aggiunto con successo.")
    except ValueError:
        print("Input non valido. Assicurati di inserire valori numerici corretti.")


def rimuovi_prodotto():
    """Rimuove un prodotto dal database."""
    stampa_prodotti()
    try:
        product_id = int(input("Inserisci l'ID del prodotto da rimuovere: ").strip())
        
        with get_connection() as conn:
            prodotto = conn.execute(
                "SELECT product_id FROM products WHERE product_id = ?",
                (product_id,)
            ).fetchone()
            
            if prodotto is None:
                print("Prodotto non trovato.")
                return
            
            conn.execute(
                "DELETE FROM products WHERE product_id = ?",
                (product_id,)
            )
            conn.commit()
        print("Prodotto rimosso con successo.")
    except ValueError:
        print("Input non valido. Assicurati di inserire un numero intero per l'ID.")


def menu_prodotti():
    """Menu per la gestione dei prodotti."""
    while True:
        print("\n--- Menu Prodotti ---")
        print("1. Aggiungi prodotto")
        print("2. Rimuovi prodotto")
        print("3. Visualizza prodotti")
        print("4. Torna al menu principale")
        
        scelta = input("Seleziona un'opzione (1-4): ").strip()
        
        if scelta == '1':
            aggiungi_prodotto()
        elif scelta == '2':
            rimuovi_prodotto()
        elif scelta == '3':
            stampa_prodotti()
        elif scelta == '4':
            break
        else:
            print("Opzione non valida. Riprova.")


def menu_principale():
    """Menu principale del sistema amministrativo."""
    while True:
        print("\n--- Menu Principale ---")
        print("1. Calcolo Stipendio")
        print("2. Modifica Prodotti")
        print("3. Calcolo Profitto")
        print("4. Esci")
        
        scelta = input("Seleziona un'opzione (1-4): ").strip()
        
        if scelta == '1':
            calcola_stipendio()
        elif scelta == '2':
            menu_prodotti()
        elif scelta == '3':
            calcola_profitto()
        elif scelta == '4':
            print("Uscita dal sistema.")
            sys.exit(0)
        else:
            print("Opzione non valida. Riprova.")


if __name__ == '__main__':
    init_db()
    
    # Inizializza le credenziali amministratore se non esistono
    with get_connection() as conn:
        existing_hash = conn.execute("SELECT admin_hash FROM admin_credentials LIMIT 1").fetchone()
        if existing_hash is None:
            conn.execute(
                "INSERT INTO admin_credentials (admin_hash) VALUES (?)",
                (_ADMIN_HASH,)
            )
            conn.commit()
    
    if not login():
        sys.exit(1)
    
    menu_principale()