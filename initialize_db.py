# initialize_db.py

import sqlite3

def create_and_seed_database():
    conn = sqlite3.connect("car_booking.db")
    cursor = conn.cursor()

    # Drop existing tables if reinitializing
    cursor.execute("DROP TABLE IF EXISTS cars")
    cursor.execute("DROP TABLE IF EXISTS customers")
    cursor.execute("DROP TABLE IF EXISTS bookings")

    # Create tables
    cursor.execute("""
    CREATE TABLE cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        brand TEXT,
        cc INTEGER,
        bhp INTEGER,
        torque TEXT,
        transmission TEXT,
        top_speed INTEGER,
        mileage REAL,
        tank_capacity REAL,
        seats INTEGER,
        price REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        car_id INTEGER,
        booking_date TEXT,
        delivery_date TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id),
        FOREIGN KEY(car_id) REFERENCES cars(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cancellations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        car_id INTEGER,
        booking_date TEXT,
        cancellation_date TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (car_id) REFERENCES cars(id)
    )
    """)


    # Car data to insert (10 models per brand)
    cars_data = [
        # Audi
        ("A3", "Audi", 1500, 148, "250 Nm", "Automatic", 210, 18.0, 50, 5, 32000),
        ("A4", "Audi", 2000, 190, "320 Nm", "Automatic", 240, 17.5, 54, 5, 40000),
        ("Q3", "Audi", 2000, 190, "350 Nm", "Automatic", 220, 16.0, 60, 5, 43000),
        ("Q5", "Audi", 2000, 252, "370 Nm", "Automatic", 240, 15.0, 70, 5, 50000),
        ("Q7", "Audi", 3000, 335, "500 Nm", "Automatic", 250, 12.0, 75, 7, 75000),
        ("RS5", "Audi", 2900, 450, "600 Nm", "Automatic", 280, 11.0, 58, 4, 85000),
        ("A6", "Audi", 2000, 245, "370 Nm", "Automatic", 250, 14.0, 65, 5, 60000),
        ("A8", "Audi", 3000, 335, "500 Nm", "Automatic", 250, 10.0, 72, 5, 95000),
        ("TT", "Audi", 2000, 230, "370 Nm", "Manual", 250, 13.0, 50, 4, 55000),
        ("E-Tron", "Audi", 0, 355, "561 Nm", "Automatic", 200, 0, 95, 5, 70000),

        # Honda
        ("Civic", "Honda", 1500, 180, "240 Nm", "Automatic", 220, 18.4, 47, 5, 25000),
        ("Accord", "Honda", 1500, 192, "260 Nm", "Automatic", 220, 16.5, 56, 5, 30000),
        ("CR-V", "Honda", 2000, 190, "280 Nm", "Automatic", 210, 15.5, 57, 5, 33000),
        ("City", "Honda", 1500, 121, "145 Nm", "Manual", 180, 17.8, 40, 5, 20000),
        ("Jazz", "Honda", 1200, 90, "110 Nm", "Manual", 170, 19.0, 42, 5, 18000),
        ("HR-V", "Honda", 1500, 143, "179 Nm", "CVT", 190, 16.2, 45, 5, 27000),
        ("WR-V", "Honda", 1200, 89, "110 Nm", "Manual", 170, 18.1, 40, 5, 19000),
        ("Brio", "Honda", 1200, 88, "109 Nm", "Manual", 160, 19.4, 35, 5, 17000),
        ("Pilot", "Honda", 3500, 280, "355 Nm", "Automatic", 200, 12.5, 70, 7, 40000),
        ("Odyssey", "Honda", 3500, 280, "355 Nm", "Automatic", 195, 11.5, 75, 7, 42000),
        # Toyota
        ("Corolla", "Toyota", 1800, 139, "171 Nm", "CVT", 180, 16.5, 50, 5, 23000),
        ("Camry", "Toyota", 2500, 203, "250 Nm", "Automatic", 210, 15.0, 60, 5, 32000),
        ("Fortuner", "Toyota", 2755, 204, "500 Nm", "Automatic", 190, 14.2, 80, 7, 38000),
        ("Innova", "Toyota", 2400, 150, "343 Nm", "Manual", 165, 13.0, 65, 7, 30000),
        ("Yaris", "Toyota", 1500, 107, "140 Nm", "Manual", 170, 17.1, 42, 5, 21000),
        ("RAV4", "Toyota", 2500, 203, "243 Nm", "CVT", 195, 14.5, 55, 5, 29000),
        ("Highlander", "Toyota", 3500, 295, "357 Nm", "Automatic", 210, 12.5, 68, 7, 40000),
        ("Supra", "Toyota", 3000, 382, "500 Nm", "Automatic", 250, 11.0, 52, 2, 52000),
        ("Land Cruiser", "Toyota", 4500, 350, "700 Nm", "Automatic", 210, 9.0, 93, 7, 85000),
        ("Hilux", "Toyota", 2800, 204, "500 Nm", "Manual", 180, 14.0, 80, 5, 37000),

        # Lamborghini
        ("Huracan EVO", "Lamborghini", 5204, 631, "600 Nm", "Automatic", 325, 7.1, 80, 2, 240000),
        ("Aventador S", "Lamborghini", 6498, 730, "690 Nm", "Automatic", 350, 6.2, 85, 2, 420000),
        ("Urus", "Lamborghini", 3996, 641, "850 Nm", "Automatic", 305, 8.0, 85, 5, 220000),
        ("Gallardo", "Lamborghini", 5200, 552, "540 Nm", "Manual", 325, 6.5, 80, 2, 200000),
        ("Murcielago", "Lamborghini", 6496, 661, "660 Nm", "Manual", 342, 5.7, 100, 2, 340000),
        ("Reventon", "Lamborghini", 6496, 650, "660 Nm", "Automatic", 340, 5.0, 90, 2, 1500000),
        ("Sian", "Lamborghini", 6498, 819, "720 Nm", "Automatic", 350, 4.8, 85, 2, 3600000),
        ("Centenario", "Lamborghini", 6498, 770, "690 Nm", "Automatic", 350, 5.2, 85, 2, 2600000),
        ("Veneno", "Lamborghini", 6498, 750, "690 Nm", "Automatic", 355, 6.8, 90, 2, 4500000),
        ("Countach LPI 800-4", "Lamborghini", 6498, 803, "720 Nm", "Automatic", 355, 5.0, 90, 2, 2600000),

        # Bugatti
        ("Veyron", "Bugatti", 7993, 1001, "1250 Nm", "Automatic", 407, 4.5, 100, 2, 1500000),
        ("Chiron", "Bugatti", 7993, 1500, "1600 Nm", "Automatic", 420, 4.0, 100, 2, 3000000),
        ("Divo", "Bugatti", 7993, 1500, "1600 Nm", "Automatic", 380, 4.5, 100, 2, 5500000),
        ("Bolide", "Bugatti", 7993, 1850, "1850 Nm", "Automatic", 500, 3.5, 100, 2, 7000000),
        ("La Voiture Noire", "Bugatti", 7993, 1500, "1600 Nm", "Automatic", 420, 4.0, 100, 2, 19000000),
        ("EB110", "Bugatti", 3499, 603, "650 Nm", "Manual", 343, 6.0, 120, 2, 800000),
        ("Centodieci", "Bugatti", 7993, 1600, "1600 Nm", "Automatic", 380, 4.4, 100, 2, 9000000),
        ("Super Sport 300+", "Bugatti", 7993, 1600, "1600 Nm", "Automatic", 490, 3.7, 100, 2, 3900000),
        ("Type 57", "Bugatti", 3257, 135, "200 Nm", "Manual", 160, 12.0, 80, 2, 2000000),
        ("Type 41 Royale", "Bugatti", 12763, 300, "400 Nm", "Manual", 200, 5.0, 150, 5, 10000000),

        # Pagani
        ("Zonda F", "Pagani", 7291, 602, "760 Nm", "Manual", 345, 5.0, 85, 2, 1700000),
        ("Zonda R", "Pagani", 5987, 750, "710 Nm", "Manual", 375, 4.5, 100, 2, 2500000),
        ("Huayra", "Pagani", 5980, 720, "1000 Nm", "Automatic", 370, 5.4, 85, 2, 3000000),
        ("Huayra BC", "Pagani", 5980, 800, "1050 Nm", "Automatic", 380, 5.1, 85, 2, 3200000),
        ("Zonda Cinque", "Pagani", 7291, 678, "780 Nm", "Manual", 355, 4.7, 85, 2, 2000000),
        ("Zonda HP Barchetta", "Pagani", 7291, 789, "850 Nm", "Manual", 355, 4.0, 85, 2, 17000000),
        ("Imola", "Pagani", 5980, 827, "1100 Nm", "Automatic", 360, 4.8, 90, 2, 5000000),
        ("Utopia", "Pagani", 5980, 864, "1100 Nm", "Manual", 350, 5.2, 90, 2, 3400000),
        ("C12", "Pagani", 5987, 450, "520 Nm", "Manual", 330, 6.0, 85, 2, 1200000),
        ("Zonda Tricolore", "Pagani", 7291, 670, "780 Nm", "Manual", 350, 4.9, 85, 2, 2100000),

        # Volkswagen
        ("Polo", "Volkswagen", 1000, 95, "175 Nm", "Manual", 180, 18.0, 45, 5, 17000),
        ("Vento", "Volkswagen", 1500, 110, "250 Nm", "Manual", 190, 17.0, 55, 5, 22000),
        ("Virtus", "Volkswagen", 1000, 115, "178 Nm", "Automatic", 195, 16.2, 55, 5, 24000),
        ("Taigun", "Volkswagen", 1500, 150, "250 Nm", "Automatic", 200, 16.5, 55, 5, 28000),
        ("Tiguan", "Volkswagen", 2000, 187, "320 Nm", "Automatic", 210, 14.0, 60, 5, 35000),
        ("Passat", "Volkswagen", 2000, 174, "280 Nm", "Automatic", 210, 15.0, 66, 5, 31000),
        ("Arteon", "Volkswagen", 2000, 268, "350 Nm", "Automatic", 250, 13.0, 66, 5, 43000),
        ("Golf", "Volkswagen", 2000, 241, "370 Nm", "Manual", 250, 15.0, 50, 5, 29000),
        ("T-Cross", "Volkswagen", 1000, 115, "200 Nm", "Automatic", 180, 18.2, 50, 5, 23000),
        ("Touareg", "Volkswagen", 3000, 282, "600 Nm", "Automatic", 235, 12.5, 75, 5, 50000),

        # Toyota (10 models), Lamborghini, Bugatti, Pagani, Volkswagen to be added similarly
    ]

    # Add more brands: Toyota, Lamborghini, Bugatti, Pagani, Volkswagen
    # Can continue if you approve the format

    cursor.executemany("""
    INSERT INTO cars (
        model, brand, cc, bhp, torque, transmission, top_speed,
        mileage, tank_capacity, seats, price
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cars_data)

    conn.commit()
    conn.close()
    print("Database initialized and car data inserted.")

if __name__ == "__main__":
    create_and_seed_database()
