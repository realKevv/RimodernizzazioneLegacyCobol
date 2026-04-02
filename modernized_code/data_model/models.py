import sqlite3
from typing import List, Tuple, Optional

class DatabaseManager:
    def __init__(self, db_path: str = '../accounting.db'):
        self.db_path = db_path

    def connect(self):
        """Crea una connessione al database SQLite."""
        return sqlite3.connect(self.db_path)

    def initialize_database(self):
        """Inizializza il database creando le tabelle se non esistono."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.executescript(self._get_schema_sql())
            conn.commit()

    def _get_schema_sql(self) -> str:
        """Restituisce lo schema SQL per la creazione delle tabelle."""
        return """
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
        """

    def insert_products(self, products: List[Tuple[str, float, int]]) -> None:
        """Inserisce una lista di prodotti nel database."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.executemany(
                """
                INSERT INTO products (name, price, stock)
                VALUES (?, ?, ?)
                """,
                products
            )
            conn.commit()

    def insert_order(self, product_id: int, quantity: int, total_price: float) -> None:
        """Inserisce un ordine nel database."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO orders (product_id, quantity, total_price)
                VALUES (?, ?, ?)
                """,
                (product_id, quantity, total_price)
            )
            conn.commit()

    def get_product_by_name(self, name: str) -> Optional[Tuple[int, str, float, int]]:
        """Restituisce un prodotto per nome."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT product_id, name, price, stock FROM products WHERE name = ?",
                (name,)
            )
            return cursor.fetchone()

    def update_product_stock(self, product_id: int, new_stock: int) -> None:
        """Aggiorna la quantità di stock di un prodotto."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE products SET stock = ? WHERE product_id = ?",
                (new_stock, product_id)
            )
            conn.commit()

    def get_all_products(self) -> List[Tuple[int, str, float, int]]:
        """Restituisce tutti i prodotti nel database."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT product_id, name, price, stock FROM products")
            return cursor.fetchall()