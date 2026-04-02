import os
import sqlite3
from typing import List, Tuple


def read_legacy_products(file_path: str) -> List[Tuple[str, float, int]]:
    """
    Legge il file legacy products.txt e restituisce una lista di prodotti nel formato:
    (nome, prezzo, stock)
    
    Args:
        file_path (str): Percorso del file legacy.
    
    Returns:
        List[Tuple[str, float, int]]: Lista di prodotti.
    """
    products = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 4:
                prezzo = float(parts[-1])
                taglia = parts[-2]
                nome = ' '.join(parts[1:-2])
                nome_finale = f'{nome} {taglia}'
                stock = 100
                products.append((nome_finale, prezzo, stock))
    return products


def initialize_database(db_path: str) -> None:
    """
    Inizializza il database SQLite con lo schema richiesto.
    
    Args:
        db_path (str): Percorso del database SQLite.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                price      REAL    NOT NULL CHECK(price >= 0),
                stock      INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0)
            );

            CREATE TABLE IF NOT EXISTS orders (
                order_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id  INTEGER NOT NULL REFERENCES products(product_id),
                quantity    INTEGER NOT NULL CHECK(quantity > 0),
                total_price REAL    NOT NULL,
                created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()


def migrate_data() -> None:
    """
    Esegue la migrazione dei dati dal file legacy al database SQLite.
    """
    # Percorsi dei file
    legacy_file_path = os.path.join('..', '..', 'legacy_code', 'products.txt')
    db_path = os.path.join('..', 'accounting.db')

    # Legge i dati legacy
    products = read_legacy_products(legacy_file_path)

    # Inizializza il database
    initialize_database(db_path)

    # Inserisce i dati nel database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT INTO products (name, price, stock)
            VALUES (?, ?, ?)
            """,
            products
        )
        conn.commit()

    print(f"Migrazione completata: {len(products)} prodotti inseriti nel database.")


if __name__ == '__main__':
    migrate_data()