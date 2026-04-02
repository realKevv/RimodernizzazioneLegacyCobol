import sqlite3
import sys

DB_PATH = 'accounting.db'


def get_connection():
    """Restituisce una connessione al database SQLite con row_factory configurato."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inizializza il database con le tabelle necessarie."""
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
        conn.commit()


def visualizza_prodotti() -> list:
    """Restituisce la lista di tutti i prodotti disponibili nel database."""
    with get_connection() as conn:
        prodotti = conn.execute("SELECT product_id, name, price, stock FROM products").fetchall()
    return [dict(p) for p in prodotti]


def effettua_ordine(product_id: int, quantity: int) -> float:
    """
    Effettua un ordine per un prodotto specificato.
    
    Args:
        product_id: ID del prodotto da ordinare.
        quantity: Quantità da ordinare.
    
    Returns:
        Il prezzo totale dell'ordine.
    
    Raises:
        ValueError: Se il prodotto non esiste, non è disponibile o la quantità è insufficiente.
    """
    with get_connection() as conn:
        # Verifica se il prodotto esiste e ha stock sufficiente
        prodotto = conn.execute(
            "SELECT product_id, name, price, stock FROM products WHERE product_id = ?",
            (product_id,)
        ).fetchone()
        
        if not prodotto:
            raise ValueError("Prodotto non trovato.")
        
        if prodotto['stock'] < quantity:
            raise ValueError("Quantità insufficiente in magazzino.")
        
        # Calcola il prezzo totale
        total_price = prodotto['price'] * quantity
        
        # Registra l'ordine
        conn.execute(
            """
            INSERT INTO orders (product_id, quantity, total_price)
            VALUES (?, ?, ?)
            """,
            (product_id, quantity, total_price)
        )
        
        # Aggiorna lo stock del prodotto
        conn.execute(
            "UPDATE products SET stock = stock - ? WHERE product_id = ?",
            (quantity, product_id)
        )
        
        conn.commit()
        
        return total_price


def menu_principale():
    """Menu principale del modulo BuyRoutine."""
    while True:
        print("\n" + "=" * 50)
        print("MENU PRINCIPALE - ACQUISTI")
        print("=" * 50)
        print("1. Acquista Prodotti")
        print("2. Visualizza Prodotti Disponibili")
        print("3. Torna al Menu Principale")
        print("=" * 50)
        
        scelta = input("Seleziona un'opzione (1-3): ").strip()
        
        if scelta == "1":
            acquista_prodotti()
        elif scelta == "2":
            visualizza_prodotti_disponibili()
        elif scelta == "3":
            print("Torna al menu principale...")
            break
        else:
            print("Opzione non valida. Riprova.")


def visualizza_prodotti_disponibili():
    """Visualizza la lista dei prodotti disponibili."""
    prodotti = visualizza_prodotti()
    
    if not prodotti:
        print("Nessun prodotto disponibile.")
        return
    
    print("\n" + "=" * 70)
    print("PRODOTTI DISPONIBILI")
    print("=" * 70)
    print(f"{'ID':<6} {'Nome':<30} {'Prezzo':<12} {'Disponibilità':<15}")
    print("-" * 70)
    
    for p in prodotti:
        print(f"{p['product_id']:<6} {p['name'][:29]:<30} {p['price']:<12.2f} {p['stock']:<15}")
    print("=" * 70)


def acquista_prodotti():
    """Gestisce la procedura di acquisto dei prodotti."""
    prodotti = visualizza_prodotti()
    
    if not prodotti:
        print("Nessun prodotto disponibile per l'acquisto.")
        return
    
    print("\n" + "=" * 70)
    print("PROCEDURA DI ACQUISTO")
    print("=" * 70)
    
    # Selezione del numero di prodotti da acquistare
    while True:
        try:
            num_prodotti = int(input("Quanti prodotti vuoi acquistare? (1-10): ").strip())
            if 1 <= num_prodotti <= 10:
                break
            else:
                print("Inserisci un numero tra 1 e 10.")
        except ValueError:
            print("Inserisci un numero valido.")
    
    ordine = []
    totale = 0.0
    
    # Selezione dei prodotti
    for i in range(num_prodotti):
        while True:
            visualizza_prodotti_disponibili()
            try:
                product_id = int(input(f"Inserisci l'ID del prodotto {i+1}: ").strip())
                prodotto = next((p for p in prodotti if p['product_id'] == product_id), None)
                
                if not prodotto:
                    print("Prodotto non trovato. Riprova.")
                    continue
                
                # Selezione della quantità
                while True:
                    try:
                        quantity = int(input(f"Inserisci la quantità per '{prodotto['name']}': ").strip())
                        if quantity <= 0:
                            print("La quantità deve essere maggiore di zero.")
                            continue
                        if quantity > prodotto['stock']:
                            print(f"Quantità insufficiente. Disponibile: {prodotto['stock']}")
                            continue
                        break
                    except ValueError:
                        print("Inserisci un numero valido.")
                
                # Effettua l'ordine
                prezzo_totale = effettua_ordine(product_id, quantity)
                ordine.append({
                    'product_id': product_id,
                    'name': prodotto['name'],
                    'quantity': quantity,
                    'price': prodotto['price'],
                    'total': prezzo_totale
                })
                totale += prezzo_totale
                print(f"Aggiunto al carrello: {prodotto['name']} (x{quantity}) - {prezzo_totale:.2f} PHP")
                break
            except ValueError as e:
                print(f"Errore: {e}")
            except Exception as e:
                print(f"Si è verificato un errore: {e}")
    
    # Calcolo del resto
    while True:
        try:
            money_paid = float(input(f"Importo totale: {totale:.2f} PHP\nImporto pagato: ").strip())
            if money_paid < totale:
                print("Importo insufficiente. Riprova.")
                continue
            change = money_paid - totale
            break
        except ValueError:
            print("Inserisci un importo valido.")
    
    # Genera la ricevuta
    generate_receipt(ordine, totale, money_paid, change)


def generate_receipt(ordine: list, totale: float, money_paid: float, change: float):
    """Genera e stampa una ricevuta dettagliata dell'ordine."""
    print("\n" + "=" * 70)
    print("RICEVUTA DI ACQUISTO")
    print("=" * 70)
    print(f"Data: {__get_current_date()}")
    print("-" * 70)
    print(f"{'Prodotto':<30} {'Qtà':<6} {'Prezzo Unitario':<15} {'Totale':<12}")
    print("-" * 70)
    
    for item in ordine:
        print(f"{item['name'][:29]:<30} {item['quantity']:<6} {item['price']:<15.2f} {item['total']:<12.2f}")
    
    print("-" * 70)
    print(f"{'TOTALE:':<51} {totale:<12.2f}")
    print(f"{'PAGATO:':<51} {money_paid:<12.2f}")
    print(f"{'RESTO:':<51} {change:<12.2f}")
    print("=" * 70)
    print("Grazie per il tuo acquisto!")
    print("=" * 70)


def __get_current_date() -> str:
    """Restituisce la data corrente in formato testuale."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    init_db()
    menu_principale()