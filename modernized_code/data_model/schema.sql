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