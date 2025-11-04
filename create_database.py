import sqlite3

conn = sqlite3.connect("logistics.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    experience_years INTEGER,
    salary REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    capacity_kg INTEGER,
    fuel_consumption_l_100km REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS routes (
    route_id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT,
    destination TEXT,
    distance_km REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS shipments (
    shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    route_id INTEGER,
    vehicle_id INTEGER,
    driver_id INTEGER,
    status TEXT,
    delivery_time_hours REAL,
    delay_minutes INTEGER,
    FOREIGN KEY (route_id) REFERENCES routes(route_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS costs (
    cost_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INTEGER,
    fuel_cost REAL,
    toll_cost REAL,
    maintenance_cost REAL,
    admin_fee REAL,
    FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS revenues (
    revenue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INTEGER,
    revenue_amount REAL,
    FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
);
""")

conn.commit()
conn.close()

print("Baza danych 'logistics.db' została utworzona!")
