import sqlite3

with open('schema.sql') as f:
    schema = f.read()

conn = sqlite3.connect('database.db')
conn.executescript(schema)

# Login admin
conn.execute("INSERT INTO Logins (username, password) VALUES (?, ?)", ('admin', 'admin'))

# Satu bean awal
conn.execute("INSERT INTO Bean (name, description) VALUES (?, ?)", ('Arabica', 'Smooth and rich'))
conn.execute("INSERT INTO DailyBean (bean_id, sale_price) VALUES (?, ?)", (1, 5.50))

# Data bean lengkap
beans = [
    ('Colombian Supremo', 'Smooth, full-flavored coffee from Colombia.', 13.50),
    ('Pure Kona Fancy', 'Coffee from Hawaii with subtle winery tones.', 15.90),
    ('Kenyan', 'Winey, full flavor with rich aroma.', 24.00),
    ('Costa Rican', 'Lively, well-balanced coffee.', 12.30),
    ('Kona Peaberry', 'Peaberries with intense flavor.', 10.00),
    ('Sumatra', 'Dark chocolate finish, full-bodied.', 9.50),
    ('Kona Blend', '25% Kona, 50% Colombian, 25% Sumatra.', 12.15),
    ('Kona Espresso', 'Smokey, bitter-sweet espresso lovers’ favorite.', 13.00),
    ('Italian Roast', 'Bold dark roast with espresso bite.', 11.90)
]

for name, desc, price in beans:
    conn.execute("INSERT INTO Bean (name, description) VALUES (?, ?)", (name, desc))
    last_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute("INSERT INTO DailyBean (bean_id, sale_price) VALUES (?, ?)", (last_id, price))

# Data distributor sesuai soal
distributors = [
    ('Beans R Us', 'Brisbane', 'Queensland', 'Australia', '0123456789', 'beans@r-us.com'),
    ('The Buzz', 'Munich', 'Bavaria', 'Germany', '0987654321', 'buzz@coffee.de'),
    # ... tambahkan lainnya
]

for name, city, state, country, phone, email in distributors:
    conn.execute("""
        INSERT INTO Distributor (name, city, state, country, phone, email)
        VALUES (?, ?, ?, ?, ?, ?)""", (name, city, state, country, phone, email))


conn.commit()
conn.close()

print("✅ Database initialized with sample data.")
