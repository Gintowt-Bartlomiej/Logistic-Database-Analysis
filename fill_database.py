import sqlite3
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import json
import os

fake = Faker()

conn = sqlite3.connect("logistics.db")
cursor = conn.cursor()

# Drivers
for i in range(15):
    name = fake.name()
    experience_years = random.randint(1, 10)
    salary = round(random.uniform(6000, 10000), 2)

    cursor.execute("INSERT INTO drivers (name, experience_years, salary) VALUES (?, ?, ?)",
                   (name, experience_years, salary))
    
# Vehicles
vehicle_types = ['Truck', 'Van', 'Refrigerated truck']
for i in range(15):
    v_type = random.choice(vehicle_types)
    if v_type == "Van":
        capacity_kg = random.randint(2000, 3500)
        fuel_consumption = round(random.uniform(9, 14), 2)
    else:  
        capacity_kg = random.randint(22000, 26000)
        fuel_consumption = round(random.uniform(25, 40), 2)

    cursor.execute("INSERT INTO vehicles (type, capacity_kg, fuel_consumption_l_100km) VALUES (?, ?, ?)",
                   (v_type, capacity_kg, fuel_consumption))
    

# Routes
data_dir = os.path.join(os.path.dirname(__file__), 'data')
routes_file = os.path.join(data_dir, 'route_distances.txt')
with open(routes_file, 'r') as f:
    route_distances = json.load(f)

for origin in route_distances:
    for destination, distance in route_distances[origin].items():
        cursor.execute("""
        INSERT INTO routes (origin, destination, distance_km)
        VALUES (?, ?, ?)
        """, (origin, destination, distance))


# Shipments
statuses = ['Completed', 'In Progress', 'Delayed', 'Cancelled']
start_date = datetime(2023, 1, 1)

cursor.execute("SELECT COUNT(*) FROM routes")
route_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM vehicles")
vehicle_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM drivers")
driver_count = cursor.fetchone()[0]

for _ in range(673):
    random_date = start_date + timedelta(days=random.randint(0, 800))
    route_id = random.randint(1, route_count)
    vehicle_id = random.randint(1, vehicle_count)
    driver_id = random.randint(1, driver_count)
    status = random.choice(statuses)
    
    # Get route distance for this shipment
    cursor.execute("SELECT distance_km FROM routes WHERE route_id = ?", (route_id,))
    distance = cursor.fetchone()[0]
    
    # Calculate realistic delivery time based on distance
    # Assuming average speed of 60 km/h
    base_delivery_time = round(distance / 60, 2)
    
    # Add some random variation to delivery time
    delivery_time = round(base_delivery_time * random.uniform(0.9, 1.2), 2)
    
    # Calculate delay based on status
    if status == 'Delayed':
        delay_minutes = random.randint(30, 360)
    else:
        delay_minutes = random.randint(0, 30)

    cursor.execute("""
    INSERT INTO shipments (date, route_id, vehicle_id, driver_id, status, 
                         delivery_time_hours, delay_minutes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        random_date.strftime('%Y-%m-%d'),
        route_id,
        vehicle_id,
        driver_id,
        status,
        delivery_time,
        delay_minutes
    ))
    
    # Get the last inserted shipment_id
    shipment_id = cursor.lastrowid
    
    # Calculate costs based on distance and vehicle type
    cursor.execute("SELECT type, fuel_consumption_l_100km FROM vehicles WHERE vehicle_id = ?", (vehicle_id,))
    vehicle_data = cursor.fetchone()
    vehicle_type, fuel_consumption = vehicle_data
    
    # Calculate fuel cost (assuming 6.5 PLN per liter)
    fuel_cost = round((distance * fuel_consumption / 100) * 6.5, 2)
    
    # Calculate toll cost based on distance and vehicle type
    if vehicle_type == 'Van':
        toll_rate = 0.40  # PLN per km
    else:
        toll_rate = 0.75  # PLN per km for trucks
    toll_cost = round(distance * toll_rate, 2)
    
    # Maintenance cost based on distance
    maintenance_cost = round(distance * random.uniform(0.3, 0.5), 2)
    
    # Insert costs
    cursor.execute("""
    INSERT INTO costs (shipment_id, fuel_cost, toll_cost, maintenance_cost)
    VALUES (?, ?, ?, ?)
    """, (shipment_id, fuel_cost, toll_cost, maintenance_cost))
    
    # Calculate revenue (should be higher than total costs to ensure profit)
    total_cost = fuel_cost + toll_cost + maintenance_cost
    base_profit_margin = random.uniform(1.3, 1.8)  # 30-80% profit margin
    revenue_amount = round(total_cost * base_profit_margin, 2)
    
    # Insert revenue
    cursor.execute("""
    INSERT INTO revenues (shipment_id, revenue_amount)
    VALUES (?, ?)
    """, (shipment_id, revenue_amount))

conn.commit()
conn.close()

print("Database has been filled with sample data!")